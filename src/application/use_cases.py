from src.domain.entities import Session
from src.domain.interfaces import SessionRepositoryInterface

class CreateSessionUseCase:
    def __init__(self, repository: SessionRepositoryInterface):
        self.repository = repository

    def execute(self, session: Session) -> Session:
        overlapping = self.repository.find_overlapping(session.therapist_id, session.start, session.end)
        
        if overlapping:
            raise ValueError("Schedule conflict")
            
        self.repository.save(session)
        return session