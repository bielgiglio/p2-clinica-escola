from datetime import datetime

class Session:
    def __init__(self, therapist_id: str, patient_id: str, start: datetime, end: datetime):
        self.therapist_id = therapist_id
        self.patient_id = patient_id
        self.start = start
        self.end = end