# Controller.py
import json
import os
from typing import List, Optional
from PerfilProdutor import PerfilProdutor


class ControllerPerfilProdutor:
    """
    Gerencia lista de PerfilProdutor com persistência em JSON.
    """
    def __init__(self, _arquivo: str = "Cadastros.json"):
        self.arquivo = _arquivo
        self.cadastros: List[PerfilProdutor] = self.__carregar_cadastros()

    def __carregar_cadastros(self) -> List[PerfilProdutor]:
        if not os.path.exists(self.arquivo):
            return []
        try:
            with open(self.arquivo, "r", encoding="utf-8") as f:
                _dados = json.load(f)
            _cadastros: List[PerfilProdutor] = []
            for _r in _dados:
                # compatibilidade defensiva: use keys com fallback
                produtor = _r.get("produtor", "")
                tipo_solos = _r.get("tipo_solos", "")
                fazenda = _r.get("fazenda", "")
                talhao = _r.get("talhao", "")
                ph = float(_r.get("ph", 0.0))
                p = float(_r.get("p", 0.0))
                k = float(_r.get("k", 0.0))
                _cadastros.append(PerfilProdutor(produtor, tipo_solos, fazenda, talhao, ph, p, k))
            return _cadastros
        except Exception:
            # se arquivo inválido, retorna lista vazia
            return []

    def __salvar_cadastros(self) -> None:
        _dados = [
            {
                "produtor": c.produtor,
                "tipo_solos": c.tipo_solos,
                "fazenda": c.fazenda,
                "talhao": c.talhao,
                "ph": c.ph,
                "p": c.p,
                "k": c.k
            }
            for c in self.cadastros
        ]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(_dados, f, ensure_ascii=False, indent=4)

    def criar(self, _perfil: PerfilProdutor) -> bool:
        """
        Adiciona um novo perfil se não houver produtor duplicado (por nome).
        """
        if not _perfil or not _perfil.produtor:
            return False
        if self.buscar_por_produtor(_perfil.produtor):
            return False
        self.cadastros.append(_perfil)
        self.__salvar_cadastros()
        return True

    def consultar(self, index: int) -> Optional[PerfilProdutor]:
        try:
            return self.cadastros[index]
        except Exception:
            return None

    def alterar(self, _nova: PerfilProdutor) -> bool:
        """
        Substitui o registro do mesmo produtor (case-insensitive).
        """
        for i, c in enumerate(self.cadastros):
            if c.produtor.lower() == _nova.produtor.lower():
                self.cadastros[i] = _nova
                self.__salvar_cadastros()
                return True
        return False

    def deletar(self, _produtor: str) -> bool:
        obj = self.buscar_por_produtor(_produtor)
        if obj:
            self.cadastros.remove(obj)
            self.__salvar_cadastros()
            return True
        return False

    def filtrar_por_fazenda(self, _fazenda: str) -> List[PerfilProdutor]:
        if not _fazenda or not _fazenda.strip():
            return self.cadastros
        key = _fazenda.strip().lower()
        return [c for c in self.cadastros if key in str(c.fazenda).lower()]

    def buscar_por_produtor(self, _produtor: str) -> Optional[PerfilProdutor]:
        if not _produtor:
            return None
        for c in self.cadastros:
            if c.produtor.lower() == _produtor.lower():
                return c
        return None
