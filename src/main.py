from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
import os

from src.domain.entities import Session
from src.domain.strategies import TriagemStrategy, PsicoterapiaStrategy
from src.domain.factories import SessionFactory
# 1. AQUI ESTÁ A CORREÇÃO: Importamos apenas o SQLite agora
from src.infrastructure.repositories import SQLiteSessionRepository
from src.application.use_cases import CreateSessionUseCase

app = FastAPI(title="Clínica-Escola API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 2. AQUI ESTÁ A SEGUNDA CORREÇÃO: Instanciamos o banco real
repo = SQLiteSessionRepository()
use_case = CreateSessionUseCase(repo)

class SessionRequest(BaseModel):
    therapist_id: str
    patient_id: str
    start: datetime
    modality: str

@app.get("/", include_in_schema=False)
def root():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    html_path = os.path.join(base_dir, "frontend", "index.html")
    return FileResponse(html_path)

@app.post("/sessions/")
def create_session(request: SessionRequest):
    if request.modality == "triagem":
        strategy = TriagemStrategy()
    elif request.modality == "psicoterapia":
        strategy = PsicoterapiaStrategy()
    else:
        raise HTTPException(status_code=400, detail="Modalidade inválida")

    try:
        session = SessionFactory.create(
            request.therapist_id, 
            request.patient_id, 
            request.start, 
            strategy
        )
        created_session = use_case.execute(session)
        return {"message": "Sessão agendada com sucesso", "therapist": created_session.therapist_id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sessions/list")
def list_sessions():
    sessions = repo.get_all()
    return [
        {
            "id": s.id,
            "therapist_id": s.therapist_id,
            "patient_id": s.patient_id,
            "start": s.start.isoformat(),
            "end": s.end.isoformat(),
            "status": s.status
        }
        for s in sessions
    ]

@app.patch("/sessions/{session_id}/status")
def update_status(session_id: str, status: str):
    session = repo.get_by_id(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Sessão não encontrada")
    
    try:
        # Padrão State agindo na troca de status
        if status == "CONCLUIDA":
            session.complete()
        elif status == "CANCELADA":
            session.cancel()
        else:
            raise HTTPException(status_code=400, detail="Status inválido")
        
        repo.update(session)
        return {"message": "Status atualizado com sucesso"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))