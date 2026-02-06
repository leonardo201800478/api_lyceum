from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.repositories.aluno_repository import AlunoRepository
from src.schemas.aluno import Aluno

router = APIRouter()

@router.get(
    "/alunos",
    response_model=List[Aluno],
    summary="Listar alunos",
    description="Retorna uma lista paginada de alunos com filtros opcionais."
)
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
    
    Retorna:
    - Lista de objetos Aluno com os dados completos
    """
    repository = AlunoRepository(db)
    
    # Calcular skip para paginação
    skip = (pagina - 1) * limite
    
    # Aplicar filtros
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

@router.get(
    "/alunos/{aluno_id}",
    response_model=Aluno,
    summary="Obter aluno por ID",
    description="Retorna os dados completos de um aluno específico."
)
async def obter_aluno_por_id(
    aluno_id: int,
    db: Session = Depends(get_db)
):
    """
    Obtém um aluno específico pelo seu ID.
    
    Parâmetros:
    - aluno_id: ID único do aluno
    
    Retorna:
    - Objeto Aluno completo ou 404 se não encontrado
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_id(aluno_id)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com ID {aluno_id} não encontrado"
        )
    
    return aluno

@router.get(
    "/alunos/cpf/{cpf}",
    response_model=Aluno,
    summary="Obter aluno por CPF",
    description="Retorna os dados de um aluno pelo CPF."
)
async def obter_aluno_por_cpf(
    cpf: str,
    db: Session = Depends(get_db)
):
    """
    Obtém um aluno pelo CPF.
    
    Parâmetros:
    - cpf: CPF do aluno (formatado ou não)
    
    Retorna:
    - Objeto Aluno completo ou 404 se não encontrado
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_cpf(cpf)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com CPF {cpf} não encontrado"
        )
    
    return aluno

@router.get(
    "/alunos/matricula/{matricula}",
    response_model=Aluno,
    summary="Obter aluno por matrícula",
    description="Retorna os dados de um aluno pelo número de matrícula."
)
async def obter_aluno_por_matricula(
    matricula: str,
    db: Session = Depends(get_db)
):
    """
    Obtém um aluno pelo número de matrícula.
    
    Parâmetros:
    - matricula: Número de matrícula do aluno
    
    Retorna:
    - Objeto Aluno completo ou 404 se não encontrado
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_matricula(matricula)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com matrícula {matricula} não encontrado"
        )
    
    return aluno

@router.get(
    "/alunos/email/{email}",
    response_model=Aluno,
    summary="Obter aluno por email",
    description="Retorna os dados de um aluno pelo email."
)
async def obter_aluno_por_email(
    email: str,
    db: Session = Depends(get_db)
):
    """
    Obtém um aluno pelo email.
    
    Parâmetros:
    - email: Endereço de email do aluno
    
    Retorna:
    - Objeto Aluno completo ou 404 se não encontrado
    """
    repository = AlunoRepository(db)
    aluno = repository.get_by_email(email)
    
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Aluno com email {email} não encontrado"
        )
    
    return aluno