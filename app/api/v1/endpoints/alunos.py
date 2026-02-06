from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_db
from app.crud.aluno import aluno as crud_aluno
from app.schemas.aluno import AlunoResponse, AlunoListResponse, AlunoFull
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/", response_model=AlunoListResponse)
async def read_alunos(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(50, ge=1, le=100, description="Tamanho da página"),
    search: Optional[str] = Query(None, description="Buscar por nome ou matrícula"),
    curso: Optional[str] = Query(None, description="Filtrar por curso"),
    serie: Optional[int] = Query(None, ge=1, le=10, description="Filtrar por série"),
    order_by: Optional[str] = Query(
        None,
        description="Ordenar por campo (prefixo '-' para descendente)"
    ),
):
    """
    Listar alunos com paginação e filtros
    
    - **page**: Número da página (padrão: 1)
    - **size**: Tamanho da página (padrão: 50, máximo: 100)
    - **search**: Buscar por nome, matrícula ou email
    - **curso**: Filtrar por curso
    - **serie**: Filtrar por série
    - **order_by**: Campo para ordenação (ex: 'nome', '-curso', 'serie')
    """
    try:
        result = await crud_aluno.get_paginated(
            db=db,
            page=page,
            size=size,
            search=search,
            curso=curso,
            serie=serie,
            order_by=order_by,
        )
        return result
    except Exception as e:
        logger.error(f"Erro ao listar alunos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao listar alunos"
        )


@router.get("/{aluno_id}", response_model=AlunoFull)
async def read_aluno(
    aluno_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Obter detalhes de um aluno específico
    
    - **aluno_id**: Matrícula do aluno
    """
    aluno = await crud_aluno.get(db, aluno_id=aluno_id)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return aluno


@router.get("/{aluno_id}/exists")
async def check_aluno_exists(
    aluno_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Verificar se um aluno existe
    
    - **aluno_id**: Matrícula do aluno
    """
    aluno = await crud_aluno.get(db, aluno_id=aluno_id)
    return {"exists": aluno is not None}


@router.get("/stats/summary", response_model=dict)
async def get_alunos_stats(
    db: AsyncSession = Depends(get_db),
):
    """Obter estatísticas dos alunos"""
    try:
        stats = await crud_aluno.get_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao obter estatísticas"
        )


@router.get("/curso/{curso_name}", response_model=List[AlunoResponse])
async def read_alunos_by_curso(
    curso_name: str,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
):
    """
    Listar alunos por curso
    
    - **curso_name**: Nome do curso
    - **skip**: Número de registros para pular (padrão: 0)
    - **limit**: Número máximo de registros (padrão: 100, máximo: 500)
    """
    alunos = await crud_aluno.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters={"curso": curso_name},
        order_by="nome_compl"
    )
    return alunos


@router.get("/serie/{serie_number}", response_model=List[AlunoResponse])
async def read_alunos_by_serie(
    serie_number: int,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(100, ge=1, le=500, description="Número máximo de registros"),
):
    """
    Listar alunos por série
    
    - **serie_number**: Número da série
    - **skip**: Número de registros para pular (padrão: 0)
    - **limit**: Número máximo de registros (padrão: 100, máximo: 500)
    """
    alunos = await crud_aluno.get_multi(
        db,
        skip=skip,
        limit=limit,
        filters={"serie": serie_number},
        order_by="nome_compl"
    )
    return alunos