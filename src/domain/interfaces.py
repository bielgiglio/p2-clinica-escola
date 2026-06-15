from abc import ABC, abstractmethod
from .entities import Session
from datetime import datetime

class SessionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, session: Session) -> None:
        pass

    @abstractmethod
    def find_overlapping(self, therapist_id: str, start: datetime, end: datetime) -> list[Session]:
        pass

    @abstractmethod
    def get_all(self) -> list[Session]:
        pass