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
# Remover "PaginatedResponse" - não está definido em aluno.py