from src.domain.entities import Session
from src.domain.interfaces import SessionRepositoryInterface
from datetime import datetime

class DatabaseConnection:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.sessions = []
        return cls._instance

class InMemorySessionRepository(SessionRepositoryInterface):
    def __init__(self):
        self.db = DatabaseConnection()

    def save(self, session: Session) -> None:
        self.db.sessions.append(session)

    def find_overlapping(self, therapist_id: str, start: datetime, end: datetime) -> list[Session]:
        return [
            s for s in self.db.sessions 
            if s.therapist_id == therapist_id and (start < s.end) and (end > s.start)
        ]

    def get_all(self) -> list[Session]:
        return self.db.sessions