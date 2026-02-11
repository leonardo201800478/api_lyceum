# app/services/sync_aluno.py
from typing import Dict
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.ly_aluno import LYAluno
from app.services.base_sync import BaseSyncService

class SyncAlunoService(BaseSyncService):
    MODEL = LYAluno
    API_ENDPOINT_METHOD = "get_all_alunos"
    UNIQUE_FIELD = "aluno"

    async def normalize_data(self, raw_data: Dict) -> Dict:
        """Converte os campos da API para o modelo LYAluno."""
        normalized = {}

        # Mapeamento completo (todos os campos do modelo)
        field_map = {
            "aluno": ("aluno", self._safe_str),
            "ano_ingresso": ("ano_ingresso", self._safe_int),
            "anoconcl2g": ("anoconcl2g", self._safe_int),
            "areacnpq": ("areacnpq", self._safe_str),
            "candidato": ("candidato", self._safe_str),
            "cidade2g": ("cidade2g", self._safe_str),
            "classif_aluno": ("classif_aluno", self._safe_str),
            "cod_cartao": ("cod_cartao", self._safe_str),
            "concurso": ("concurso", self._safe_str),
            "cred_educativo": ("cred_educativo", self._safe_str),
            "creditos": ("creditos", self._safe_int),
            "curriculo": ("curriculo", self._safe_str),
            "curso": ("curso", self._safe_str),
            "curso_ant": ("curso_ant", self._safe_str),
            "discipoutraserie": ("discipoutraserie", self._safe_str),
            "dist_aluno_unidade": ("dist_aluno_unidade", self._safe_int),
            "dt_ingresso": ("dt_ingresso", self._parse_datetime),
            "e_mail_interno": ("e_mail_interno", self._safe_str),
            "faculdade_conveniada": ("faculdade_conveniada", self._safe_str),
            "grupo": ("grupo", self._safe_str),
            "instituicao": ("instituicao", self._safe_str),
            "nome_abrev": ("nome_abrev", self._safe_str),
            "nome_compl": ("nome_compl", self._safe_str),
            "nome_conjuge": ("nome_conjuge", self._safe_str),
            "nome_social": ("nome_social", self._safe_str),
            "num_chamada": ("num_chamada", self._safe_int),
            "obs_aluno_finan": ("obs_aluno_finan", self._safe_str),
            "obs_tel_com": ("obs_tel_com", self._safe_str),
            "obs_tel_res": ("obs_tel_res", self._safe_str),
            "outra_faculdade": ("outra_faculdade", self._safe_str),
            "pais2g": ("pais2g", self._safe_str),
            "pessoa": ("pessoa", self._safe_int),
            "ref_aluno_ant": ("ref_aluno_ant", self._safe_str),
            "representante_turma": ("representante_turma", self._safe_representante),
            "sem_ingresso": ("sem_ingresso", self._safe_int),
            "serie": ("serie", self._safe_int),
            "sit_aluno": ("sit_aluno", self._safe_str),
            "sit_aprov": ("sit_aprov", self._safe_str),
            "stamp_atualizacao": ("stamp_atualizacao", self._safe_str),
            "tipo_aluno": ("tipo_aluno", self._safe_str),
            "tipo_escola": ("tipo_escola", self._safe_str),
            "tipo_ingresso": ("tipo_ingresso", self._safe_str),
            "turma_pref": ("turma_pref", self._safe_str),
            "turno": ("turno", self._safe_str),
            "unidade_ensino": ("unidade_ensino", self._safe_str),
            "unidade_fisica": ("unidade_fisica", self._safe_str),
        }

        for api_field, (db_field, converter) in field_map.items():
            value = raw_data.get(api_field)
            normalized[db_field] = converter(value) if converter else value

        # Campos de controle interno
        normalized["data_sincronizacao"] = datetime.now()
        normalized["sincronizado"] = True
        return normalized

    @staticmethod
    def _safe_representante(v):
        """Valida campo representante_turma (S/N)."""
        if v is None:
            return None
        v = str(v).strip().upper()
        return v if v in ("S", "N") else None

# Função de conveniência para uso no endpoint
async def sync_alunos(db: AsyncSession, incremental: bool = False) -> Dict:
    service = SyncAlunoService(db)
    return await service.sync_all(incremental=incremental)