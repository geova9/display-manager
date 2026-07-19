from abc import ABC, abstractmethod
from typing import Sequence

from monitor import Monitor
from profile import MonitorProfile


class DisplayBackend(ABC):
    """Backend abstraction for compositor-specific monitor control."""

    @abstractmethod
    def list_monitors(self) -> Sequence[Monitor]:
        raise NotImplementedError

    @abstractmethod
    def apply_profile(self, profile: MonitorProfile) -> bool:
        raise NotImplementedError
