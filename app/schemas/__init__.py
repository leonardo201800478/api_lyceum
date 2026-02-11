# app/schemas/__init__.py
from .aluno import (
    AlunoBase,
    AlunoCreate,
    AlunoUpdate,
    AlunoInDB,
    AlunoResponse,
    AlunoFull,
    AlunoListResponse,
)

__all__ = [
    "AlunoBase",
    "AlunoCreate",
    "AlunoUpdate",
    "AlunoInDB",
    "AlunoResponse",
    "AlunoFull",
    "AlunoListResponse",
]