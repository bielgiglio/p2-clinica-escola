from abc import ABC, abstractmethod

class State(ABC):
    @abstractmethod
    def cancel(self, session): pass
    
    @abstractmethod
    def complete(self, session): pass

class ScheduledState(State):
    def cancel(self, session):
        session.status = "CANCELADA"
        session.state = CanceledState()

    def complete(self, session):
        session.status = "CONCLUIDA"
        session.state = CompletedState()

class CanceledState(State):
    def cancel(self, session):
        raise ValueError("A sessão já está cancelada.")
    def complete(self, session):
        raise ValueError("Não é possível concluir uma sessão cancelada.")

class CompletedState(State):
    def cancel(self, session):
        raise ValueError("Não é possível cancelar uma sessão já concluída.")
    def complete(self, session):
        raise ValueError("A sessão já está concluída.")