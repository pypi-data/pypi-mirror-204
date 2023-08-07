import numpy
from pyFAI.containers import Integrate1dResult


def get_yerror(result: Integrate1dResult) -> numpy.ndarray:
    if result.sigma is None:
        return numpy.full_like(result.intensity, numpy.nan)

    return result.sigma
