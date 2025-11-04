import json
import os
from typing import List
from Cadastro import Cadastro


class CadernoCadastros:
    """
    Classe responsável por gerenciar uma lista de Cadastros,
    realizando as tarefas de CRUD com persistência em
    arquivo JSON.
    """
    def __init__(self, _arquivo="Cadastros.json"):
        self.arquivo = _arquivo
        self.Cadastros = self.__carregar_Cadastros()

    @property
    def arquivo(self) -> str:
        return self.__arquivo

    @arquivo.setter
    def arquivo(self, _arquivo: str) -> None:
        self.__arquivo = _arquivo

    @property
    def Cadastros(self) -> List[Cadastro]:
        return self.__Cadastros

    @Cadastros.setter
    def Cadastros(self, _list: List[Cadastro]) -> None:
        self.__Cadastros = _list

    def __carregar_Cadastros(self) -> List[Cadastro]:
        """
        Carrega as Cadastros do arquivo JSON,
        se o arquivo existir.
        """
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                _dados = json.load(f)
                _Cadastros: List[Cadastro] = []
                for _r in _dados:
                    Cadastro = Cadastro(
                        _r["nome"],
                        _r["tipo"],
                        _r["modo_preparo"],
                        _r["rendimento"],
                        _r["ingredientes"]
                    )
                    _Cadastros.append(Cadastro)
                return _Cadastros

    def __salvar_Cadastros(self):
        """
        Salva as Cadastros atuais no arquivo JSON.
        """
        _dados = [
            {
                "nome": _r.nome,
                "tipo": _r.tipo,
                "modo_preparo": _r.modo_preparo,
                "rendimento": _r.rendimento,
                "ingredientes": _r.ingredientes
            }
            for _r in self.Cadastros
        ]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(_dados, f, ensure_ascii=False, indent=4)

    def criar(self, Cadastro: Cadastro) -> bool:
        """
        Adiciona uma nova Cadastro se não existir
        duplicidade de nome.
        :return: True se adicionada ou False se duplicada.
        """
        try:
            if self.buscar_por_nome(Cadastro.nome):
                return False
            self.Cadastros.append(Cadastro)
            self.__salvar_Cadastros()
            return True
        except ValueError as ve:
            print(ve)
            return False

    def consultar(self, _i: int) -> Cadastro:
        return self.Cadastros[_i]

    def alterar(self, _nova_Cadastro: Cadastro) -> bool:
        for _i, _Cadastro in enumerate(self.Cadastros):
            if _Cadastro.nome.lower() == _nova_Cadastro.nome.lower():
                self.Cadastros[_i] = _nova_Cadastro
                self.__salvar_Cadastros()
                return True
        return False

    def deletar(self, _nome: str) -> bool:
        _Cadastro = self.buscar_por_nome(_nome)
        if _Cadastro:
            self.Cadastros.remove(_Cadastro)
            self.__salvar_Cadastros()
            return True
        return False

    def filtrar_por_ingrediente(self, _ingrediente: str) -> List[Cadastro]:
        if not _ingrediente.strip():
            return self.Cadastros
        return [
            _Cadastro
            for _Cadastro in self.Cadastros
            if _Cadastro.tem_ingrediente(_ingrediente.strip())
        ]

    def buscar_por_nome(self, _nome: str) -> Cadastro | None:
        for _Cadastro in self.Cadastros:
            if _Cadastro.nome.lower() == _nome.lower():
                return _Cadastro
        return None
