from datetime import datetime
import uuid
from .states import ScheduledState, State

class Session:
    def __init__(self, therapist_id: str, patient_id: str, start: datetime, end: datetime, session_id: str = None, status: str = "AGENDADA", state: State = None):
        self.id = session_id or str(uuid.uuid4())
        self.therapist_id = therapist_id
        self.patient_id = patient_id
        self.start = start
        self.end = end
        self.status = status
        self.state = state or ScheduledState()

    def cancel(self):
        self.state.cancel(self)

    def complete(self):
        self.state.complete(self)