# app/crud/__init__.py
from .base import CRUDBase
from .aluno import aluno, CRUDAluno

__all__ = [
    "CRUDBase",
    "CRUDAluno",
    "aluno",
]