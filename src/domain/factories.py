from datetime import datetime, timedelta
from .entities import Session
from .strategies import DurationStrategy

class SessionFactory:
    @staticmethod
    def create(therapist_id: str, patient_id: str, start: datetime, strategy: DurationStrategy) -> Session:
        brazil_now = datetime.utcnow() - timedelta(hours=3)
        
        if start < brazil_now:
            raise ValueError("Past date not allowed")
            
        end = start + strategy.get_duration()
        return Session(therapist_id, patient_id, start, end)