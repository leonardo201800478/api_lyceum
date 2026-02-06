from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.repositories.aluno_repository import AlunoRepository
from src.schemas.aluno import Aluno

router = APIRouter()

@router.get("/alunos", response_model=List[Aluno])
async def listar_alunos(
    pagina: int = Query(1, ge=1, description="Número da página"),
    limite: int = Query(50, ge=1, le=200, description="Itens por página"),
    ativo: Optional[bool] = Query(None, description="Filtrar por status ativo/inativo"),
    cpf: Optional[str] = Query(None, description="Filtrar por CPF (exato)"),
    matricula: Optional[str] = Query(None, description="Filtrar por matrícula (exato)"),
    nome: Optional[str] = Query(None, description="Buscar por nome (parcial)"),
    email: Optional[str] = Query(None, description="Filtrar por email (exato)"),
    instituicao_id: Optional[int] = Query(None, description="Filtrar por ID da instituição"),
    db: Session = Depends(get_db)
):
    """
    Lista alunos com suporte a paginação e múltiplos filtros.
    """
    repository = AlunoRepository(db)
    
    skip = (pagina - 1) * limite
    
    filtros = {}
    if ativo is not None:
        filtros['ativo'] = ativo
    if cpf:
        filtros['cpf'] = cpf
    if matricula:
        filtros['matricula'] = matricula
    if email:
        filtros['email'] = email
    if instituicao_id:
        filtros['instituicao_id'] = instituicao_id
    
    alunos = repository.get_all(
        skip=skip,
        limit=limite,
        nome=nome,
        **filtros
    )
    
    return alunos

@router.get("/alunos/{aluno_id}", response_model=Aluno)
async def obter_aluno_por_id(aluno_id: int, db: Session = Depends(get_db)):
    """
    Obtém um aluno específico pelo seu ID.
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_id(aluno_id)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com ID {aluno_id} não encontrado"
        )
    
    return aluno

@router.get("/alunos/cpf/{cpf}", response_model=Aluno)
async def obter_aluno_por_cpf(cpf: str, db: Session = Depends(get_db)):
    """
    Obtém um aluno pelo CPF.
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_cpf(cpf)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com CPF {cpf} não encontrado"
        )
    
    return aluno

@router.get("/alunos/matricula/{matricula}", response_model=Aluno)
async def obter_aluno_por_matricula(matricula: str, db: Session = Depends(get_db)):
    """
    Obtém um aluno pelo número de matrícula.
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_matricula(matricula)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com matrícula {matricula} não encontrado"
        )
    
    return aluno

@router.get("/alunos/email/{email}", response_model=Aluno)
async def obter_aluno_por_email(email: str, db: Session = Depends(get_db)):
    """
    Obtém um aluno pelo email.
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_email(email)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com email {email} não encontrado"
        )
    
    return aluno
