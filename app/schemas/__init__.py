# Corrigir o __init__.py de schemas:
from .aluno import (
    AlunoBase,
    AlunoCreate,
    AlunoUpdate,
    AlunoInDB,
    AlunoResponse,
    AlunoFull,
)

__all__ = [
    "AlunoBase",
    "AlunoCreate",
    "AlunoUpdate",
    "AlunoInDB",
    "AlunoResponse",
    "AlunoFull",
]
# Remover "PaginatedResponse" - nao esta definido em aluno.py