# app/api/v1/endpoints/alunos.py
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_async_session
from app.crud.aluno import aluno as crud_aluno
from app.schemas.aluno import AlunoResponse, AlunoListResponse, AlunoFull
from app.services.sync_aluno import sync_alunos
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/", response_model=AlunoListResponse)
async def listar_alunos(
    db: AsyncSession = Depends(get_async_session),
    page: int = Query(0, ge=0, description="Número da página"),
    size: int = Query(50, ge=1, le=100, description="Itens por página"),
    search: Optional[str] = Query(None, description="Buscar por nome, matrícula ou e-mail"),
    curso: Optional[str] = Query(None, description="Filtrar por curso"),
    serie: Optional[int] = Query(None, ge=1, le=10, description="Filtrar por série"),
    order_by: Optional[str] = Query(
        None,
        description="Ordenar por campo (prefixo '-' para descendente)"
    ),
):
    """Lista alunos com paginação, filtros e ordenação."""
    try:
        result = await crud_aluno.get_paginated(
            db=db,
            page=page,
            size=size,
            search=search,
            search_fields=["nome_compl", "nome_abrev", "aluno", "e_mail_interno"],
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

@router.get("/{aluno_id}", response_model=AlunoResponse)
async def obter_aluno(
    aluno_id: str,
    db: AsyncSession = Depends(get_async_session),
):
    """Obtém detalhes de um aluno específico pela matrícula."""
    aluno = await crud_aluno.get(db, aluno_id=aluno_id)
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado"
        )
    return aluno

@router.get("/stats/summary", response_model=dict)
async def estatisticas_alunos(
    db: AsyncSession = Depends(get_async_session),
):
    """Retorna estatísticas gerais dos alunos (total, por curso, por série)."""
    try:
        stats = await crud_aluno.get_stats(db)
        return stats
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno ao obter estatísticas"
        )

@router.post("/sync", response_model=dict)
async def sincronizar_alunos(
    background_tasks: BackgroundTasks,
    incremental: bool = False,
    db: AsyncSession = Depends(get_async_session),
):
    """
    Inicia a sincronização completa dos alunos com a API Lyceum.
    A execução ocorre em background.
    """
    async def task():
        stats = await sync_alunos(db, incremental=incremental)
        logger.info(f"Sincronização de alunos concluída: {stats}")

    background_tasks.add_task(task)
    return {
        "message": "Sincronização de alunos iniciada em background",
        "incremental": incremental,
        "status": "processing"
    }

# Inclua outros endpoints conforme necessidade (ex: por curso, por série, etc.)