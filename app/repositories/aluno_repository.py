# app/repositories/aluno_repository.py
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.aluno import Aluno
from app.schemas.aluno import AlunoCreate, AlunoUpdate


def get_by_id(db: Session, aluno_id: int) -> Optional[Aluno]:
    return db.query(Aluno).filter(Aluno.id == aluno_id).first()


def get_by_matricula(db: Session, matricula: str) -> Optional[Aluno]:
    return db.query(Aluno).filter(Aluno.matricula == matricula).first()


def list_all(db: Session, skip: int = 0, limit: int = 100) -> List[Aluno]:
    return db.query(Aluno).offset(skip).limit(limit).all()


def create(db: Session, obj_in: AlunoCreate) -> Aluno:
    db_obj = Aluno(
        matricula=obj_in.matricula,
        nome=obj_in.nome,
        ativo=obj_in.ativo,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def update(db: Session, db_obj: Aluno, obj_in: AlunoUpdate) -> Aluno:
    data = obj_in.dict(exclude_unset=True)
    for field, value in data.items():
        setattr(db_obj, field, value)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


def delete(db: Session, db_obj: Aluno) -> None:
    db.delete(db_obj)
    db.commit()