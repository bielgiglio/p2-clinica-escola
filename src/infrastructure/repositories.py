from src.domain.entities import Session
from src.domain.interfaces import SessionRepositoryInterface
from src.domain.states import ScheduledState, CompletedState, CanceledState
from datetime import datetime
import sqlite3

def get_state_from_string(status: str):
    if status == "CONCLUIDA": return CompletedState()
    if status == "CANCELADA": return CanceledState()
    return ScheduledState()

class SQLiteSessionRepository(SessionRepositoryInterface):
    def __init__(self, db_path="clinica.db"):
        self.db_path = db_path
        self._create_table()

    def _create_table(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    therapist_id TEXT,
                    patient_id TEXT,
                    start_time TEXT,
                    end_time TEXT,
                    status TEXT
                )
            ''')
            conn.commit()

    def save(self, session: Session) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO sessions (id, therapist_id, patient_id, start_time, end_time, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (session.id, session.therapist_id, session.patient_id, session.start.isoformat(), session.end.isoformat(), session.status))
            conn.commit()

    def update(self, session: Session) -> None:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('UPDATE sessions SET status = ? WHERE id = ?', (session.status, session.id))
            conn.commit()

    def find_overlapping(self, therapist_id: str, start: datetime, end: datetime) -> list[Session]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            # Ignora as sessões canceladas na busca por conflitos
            cursor.execute("SELECT id, therapist_id, patient_id, start_time, end_time, status FROM sessions WHERE therapist_id = ? AND status != 'CANCELADA'", (therapist_id,))
            rows = cursor.fetchall()
        
        overlapping = []
        for row in rows:
            s_start = datetime.fromisoformat(row[3])
            s_end = datetime.fromisoformat(row[4])
            if (start < s_end) and (end > s_start):
                overlapping.append(Session(row[1], row[2], s_start, s_end, row[0], row[5], get_state_from_string(row[5])))
        return overlapping

    def get_all(self) -> list[Session]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, therapist_id, patient_id, start_time, end_time, status FROM sessions')
            rows = cursor.fetchall()
        
        return [Session(row[1], row[2], datetime.fromisoformat(row[3]), datetime.fromisoformat(row[4]), row[0], row[5], get_state_from_string(row[5])) for row in rows]
        
    def get_by_id(self, session_id: str) -> Session:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, therapist_id, patient_id, start_time, end_time, status FROM sessions WHERE id = ?', (session_id,))
            row = cursor.fetchone()
            if row:
                return Session(row[1], row[2], datetime.fromisoformat(row[3]), datetime.fromisoformat(row[4]), row[0], row[5], get_state_from_string(row[5]))
            return None