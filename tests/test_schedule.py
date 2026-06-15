import unittest
from datetime import datetime
from src.domain.factories import SessionFactory
from src.domain.strategies import PsicoterapiaStrategy
from src.infrastructure.repositories import InMemorySessionRepository, DatabaseConnection
from src.application.use_cases import CreateSessionUseCase

class TestSchedule(unittest.TestCase):
    def setUp(self):
        db = DatabaseConnection()
        db.sessions = []
        
        self.repo = InMemorySessionRepository()
        self.use_case = CreateSessionUseCase(self.repo)
        self.strategy = PsicoterapiaStrategy()

    def test_irregular_schedule(self):
        start = datetime(2026, 8, 15, 14, 15)
        
        session = SessionFactory.create("t1", "p1", start, self.strategy)
        
        result = self.use_case.execute(session)
        self.assertEqual(result.therapist_id, "t1")

    def test_conflict(self):
        start = datetime(2026, 8, 15, 14, 15)
        
        session1 = SessionFactory.create("t1", "p1", start, self.strategy)
        self.use_case.execute(session1)
        
        with self.assertRaises(ValueError):
            session2 = SessionFactory.create("t1", "p2", start, self.strategy)
            self.use_case.execute(session2)