#!/usr/bin/env python3
"""
Script para inicialização do banco de dados com dados de exemplo.
"""
import sys
from pathlib import Path
from datetime import date

# Adicionar src ao path
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy.orm import Session
from src.core.database import engine, Base, SessionLocal
from src.models.aluno import Aluno
from src.models.instituicao import Instituicao, TipoInstituicao

def init_db():
    """Cria todas as tabelas no banco de dados."""
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

def seed_data():
    """Insere dados de exemplo para teste."""
    db = SessionLocal()
    
    try:
        # Verificar se já existem dados
        if db.query(Instituicao).count() > 0:
            print("Dados já existem, pulando seed...")
            return
        
        # Criar instituições de exemplo
        instituicoes = [
            Instituicao(
                nome="Universidade Federal de Minas Gerais",
                codigo_inep="12345678",
                tipo=TipoInstituicao.FEDERAL,
                endereco="Av. Antônio Carlos, 6627",
                cidade="Belo Horizonte",
                estado="MG",
                telefone="(31) 3409-5000",
                email="contato@ufmg.br"
            ),
            Instituicao(
                nome="Pontifícia Universidade Católica de Minas Gerais",
                codigo_inep="87654321",
                tipo=TipoInstituicao.PRIVADA,
                endereco="Av. Dom José Gaspar, 500",
                cidade="Belo Horizonte",
                estado="MG",
                telefone="(31) 3319-4444",
                email="puc@pucminas.br"
            )
        ]
        
        for instituicao in instituicoes:
            db.add(instituicao)
        
        db.commit()
        
        # Criar alunos de exemplo
        alunos = [
            Aluno(
                nome="João Silva",
                email="joao.silva@email.com",
                cpf="123.456.789-09",
                data_nascimento=date(2000, 5, 15),
                telefone="(31) 99999-8888",
                endereco="Rua das Flores, 123",
                matricula="20230001",
                ativo=True,
                instituicao_id=1
            ),
            Aluno(
                nome="Maria Santos",
                email="maria.santos@email.com",
                cpf="987.654.321-00",
                data_nascimento=date(2001, 8, 22),
                telefone="(31) 97777-6666",
                endereco="Av. Paulista, 456",
                matricula="20230002",
                ativo=True,
                instituicao_id=1
            ),
            Aluno(
                nome="Carlos Oliveira",
                email="carlos.oliveira@email.com",
                cpf="456.789.123-45",
                data_nascimento=date(1999, 3, 10),
                telefone="(31) 95555-4444",
                endereco="Rua das Acácias, 789",
                matricula="20230003",
                ativo=False,
                instituicao_id=2
            )
        ]
        
        for aluno in alunos:
            db.add(aluno)
        
        db.commit()
        print("Dados de exemplo inseridos com sucesso!")
        
    except Exception as e:
        print(f"Erro ao inserir dados: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
    seed_data()