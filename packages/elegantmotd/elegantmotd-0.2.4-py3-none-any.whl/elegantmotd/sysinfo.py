from abc import ABC, abstractmethod
from typing import Dict

from rich.console import RenderableType


class SysInfo(ABC):
    @abstractmethod
    def _get_infos(self) -> Dict[RenderableType, RenderableType]:
        pass

    @property
    def infos(self) -> Dict[RenderableType, RenderableType]:
        return self._get_infos()
