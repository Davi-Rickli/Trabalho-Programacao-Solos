import json
import os
from typing import List
from PerfilProdutor import PerfilProdutor


class ControllerPerfilProdutor:
    """
    Classe responsável por gerenciar uma lista de Cadastros,
    realizando as tarefas de CRUD com persistência em
    arquivo JSON.
    """
    def __init__(self, _arquivo="Cadastros.json"):
        self.arquivo = _arquivo
        self.cadastros = self.__carregar_cadastros()

    @property
    def arquivo(self) -> str:
        return self.__arquivo

    @arquivo.setter
    def arquivo(self, _arquivo: str) -> None:
        self.__arquivo = _arquivo

    @property
    def cadastros(self) -> List[PerfilProdutor]:
        return self.__Cadastros

    @cadastros.setter
    def cadastros(self, _list: List[PerfilProdutor]) -> None:
        self.__Cadastros = _list

    def __carregar_cadastros(self) -> List[PerfilProdutor]:
        """
        Carrega as Cadastros do arquivo JSON,
        se o arquivo existir.
        """
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                _dados = json.load(f)
                _cadastros: List[ControllerPerfilProdutor] = []
                for _r in _dados:
                    _registro = PerfilProdutor(
                        _r["produtor"],
                        _r["tipo_solos"],
                        _r["fazenda"],
                        _r["talhao"],
                        _r["ph"],
                        _r["p"],
                        _r["k"]
                    )
                    _cadastros.append(_registro)
                return _cadastros


    def __salvar_Cadastros(self):
        """
        Salva as Cadastros atuais no arquivo JSON.
        """
        _dados = [
            {
                "produtor": _r.produtor,
                "tipo_solos": _r.tipo_solos,
                "fazenda": _r.fazenda,
                "talhao": _r.talhao,
                "ph": _r.ph,
                "p": _r.p,
                "k": _r.k
            }
            for _r in self.cadastros
        ]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(_dados, f, ensure_ascii=False, indent=4)

    def criar(self, _perfil: PerfilProdutor) -> bool:
        """
        Adiciona uma nova Cadastro se não existir
        duplicidade de produtor.
        :return: True se adicionada ou False se duplicada.
        """
        try:
            if self.buscar_por_produtor(_perfil.produtor):
                return False
            self.cadastros.append(_perfil)
            self.__salvar_Cadastros()
            return True
        except ValueError as ve:
            print(ve)
            return False

    def consultar(self, _i: int) -> PerfilProdutor:
        return self.cadastros[_i]

    def alterar(self, _nova_Cadastro: PerfilProdutor) -> bool:
        for _i, _Cadastro in enumerate(self.cadastros):
            if _Cadastro.produtor.lower() == _nova_Cadastro.produtor.lower():
                self.cadastros[_i] = _nova_Cadastro
                self.__salvar_Cadastros()
                return True
        return False

    def deletar(self, _produtor: str) -> bool:
        _Cadastro = self.buscar_por_produtor(_produtor)
        if _Cadastro:
            self.cadastros.remove(_Cadastro)
            self.__salvar_Cadastros()
            return True
        return False

    def filtrar_por_fazenda(self, _fazenda: str) -> List[PerfilProdutor]:
        if not _fazenda.strip():
            return self.cadastros
        return [
            _Cadastro
            for _Cadastro in self.cadastros
            if _Cadastro.tem_fazenda(_fazenda.strip())
        ]

    def buscar_por_produtor(self, _produtor: str) -> PerfilProdutor | None:
        for _Cadastro in self.cadastros:
            if _Cadastro.produtor.lower() == _produtor.lower():
                return _Cadastro
        return None
.