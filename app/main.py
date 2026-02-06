# app/main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.config import get_settings
from app.db.session import get_db
from app.schemas.aluno import AlunoOut, AlunoCreate, AlunoUpdate
from app.repositories import aluno_repository

settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/alunos", response_model=List[AlunoOut])
def listar_alunos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return aluno_repository.list_all(db, skip=skip, limit=limit)


@app.get("/alunos/{aluno_id}", response_model=AlunoOut)
def obter_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = aluno_repository.get_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


@app.post("/alunos", response_model=AlunoOut, status_code=201)
def criar_aluno(aluno_in: AlunoCreate, db: Session = Depends(get_db)):
    existente = aluno_repository.get_by_matricula(db, aluno_in.matricula)
    if existente:
        raise HTTPException(status_code=400, detail="Matrícula já cadastrada")
    return aluno_repository.create(db, aluno_in)


@app.put("/alunos/{aluno_id}", response_model=AlunoOut)
def atualizar_aluno(aluno_id: int, aluno_in: AlunoUpdate, db: Session = Depends(get_db)):
    aluno = aluno_repository.get_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno_repository.update(db, aluno, aluno_in)


@app.delete("/alunos/{aluno_id}", status_code=204)
def remover_aluno(aluno_id: int, db: Session = Depends(get_db)):
    aluno = aluno_repository.get_by_id(db, aluno_id)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    aluno_repository.delete(db, aluno)
    return None