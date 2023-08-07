import logging
from contextlib import contextmanager
from collections import OrderedDict
from typing import Iterable, Dict, Mapping, Tuple, Optional
from ewokscore.hashing import uhash

import numpy
import pyFAI
import pyFAI.worker

_WORKER_POOL = None


logger = logging.getLogger(__name__)


class WorkerPool:
    """Pool with one worker per configuration up to a maximum number of workers."""

    def __init__(self, nworkers: int = 1) -> None:
        self._workers: Dict[int, pyFAI.worker.Worker] = OrderedDict()
        self.nworkers = nworkers

    @staticmethod
    def _worker_id(*args):
        return uhash(args)

    @property
    def nworkers(self):
        return self._nworkers

    @nworkers.setter
    def nworkers(self, value: int):
        self._nworkers = value
        self._check_pool_size()

    def _check_pool_size(self):
        while self._workers and len(self._workers) > self.nworkers:
            self._workers.popitem(last=False)

    @contextmanager
    def worker(self, options: Mapping) -> Iterable[pyFAI.worker.Worker]:
        # TODO: deal with threads and subprocesses
        worker_options, integration_options = self._split_options(options)
        logger.info("Pyfai worker options: %s", worker_options)
        logger.info("Pyfai integration options: %s", integration_options)
        worker_id = self._worker_id(worker_options, integration_options)
        worker = self._workers.pop(worker_id, None)
        if worker is None:
            logger.info("Creating a new pyfai worker")
            worker = self._create_worker(worker_options, integration_options)
        self._workers[worker_id] = worker
        self._check_pool_size()
        logger.info("Pyfai integration method: %s", worker._method)
        yield worker

    def _split_options(self, options: Mapping) -> Tuple[dict, dict]:
        integration_options = dict(options)
        worker_keys = "integrator_name", "extra_options"
        worker_options = {
            k: integration_options.pop(k)
            for k in worker_keys
            if k in integration_options
        }
        nbpt_rad = integration_options.get("nbpt_rad", None)
        if nbpt_rad:
            nbpt_azim = integration_options.get("nbpt_azim", 1)
            worker_options.setdefault("shapeOut", (nbpt_azim, nbpt_rad))
        unit = integration_options.get("unit")
        if unit:
            worker_options["unit"] = unit
        return worker_options, integration_options

    @staticmethod
    def _create_worker(
        worker_options: Mapping, integration_options: Mapping
    ) -> pyFAI.worker.Worker:
        worker = pyFAI.worker.Worker(**worker_options)
        worker.output = "raw"

        integration_options = dict(integration_options)
        mask = _extract_mask(integration_options)
        provided = set(integration_options)
        worker.set_config(integration_options, consume_keys=True)

        unused = {k: v for k, v in integration_options.items() if k in provided}
        if unused:
            logger.warning("Unused pyfai integration options: %s", unused)

        if mask is not None:
            worker.ai.set_mask(mask)

        return worker


def _get_global_pool() -> WorkerPool:
    global _WORKER_POOL
    if _WORKER_POOL is None:
        _WORKER_POOL = WorkerPool()
    return _WORKER_POOL


def set_maximum_persistent_workers(nworkers: int) -> None:
    pool = _get_global_pool()
    pool.nworkers = nworkers


@contextmanager
def persistent_worker(integration_options: Mapping) -> Iterable[pyFAI.worker.Worker]:
    """Get a worker for a particular configuration that stays in memory."""
    pool = _get_global_pool()
    with pool.worker(integration_options) as worker:
        yield worker


def _extract_mask(integration_options: dict) -> Optional[numpy.ndarray]:
    """Integration options related to the mask:

    * mask_file: URL or None
    * do_mask: use mask_file or not
    * mask: URL, array or None (overwrites mask_file and do_mask when not None)
    """
    mask = integration_options.pop("mask", None)
    mask_file = integration_options.get("mask_file", None)
    do_mask = integration_options.get("do_mask", None)
    if not do_mask:
        mask_file = None
    if isinstance(mask, str):
        mask_file = mask
        mask = None
        do_mask = True
    integration_options["mask_file"] = mask_file
    integration_options["do_mask"] = do_mask
    return mask
