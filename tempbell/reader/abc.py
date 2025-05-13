from abc import ABC, abstractmethod
from logging import getLogger

from ..model import TempSlice
#
class Reader(ABC):
    # default limits
    _limits = {
        'cpu_max': 0,
        'gpu_max': 0,
        'hdd_max': 0,
        'cassis_max': 0,
        'battery_max': 0
    }
    #
    def __init__(self):
        # importent mark in logs 
        # exsactly reader class
        self.logger = getLogger(self.__class__.__name__)
    #
    @abstractmethod
    def _read(self) -> dict:
        pass
    #
    def read(self) -> TempSlice:
        params = self._read()

        return TempSlice(**params, **self._limits)
