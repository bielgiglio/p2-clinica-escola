from abc import ABC, abstractmethod
from datetime import timedelta

class DurationStrategy(ABC):
    @abstractmethod
    def get_duration(self) -> timedelta:
        pass

class TriagemStrategy(DurationStrategy):
    def get_duration(self) -> timedelta:
        return timedelta(minutes=30)

class PsicoterapiaStrategy(DurationStrategy):
    def get_duration(self) -> timedelta:
        return timedelta(minutes=50)