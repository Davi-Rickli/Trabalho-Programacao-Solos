import json
import os
from typing import List
from Receita import Receita


class CadernoReceitas:
    """
    Classe responsável por gerenciar uma lista de receitas,
    realizando as tarefas de CRUD com persistência em
    arquivo JSON.
    """
    def __init__(self, _arquivo="receitas.json"):
        self.arquivo = _arquivo
        self.receitas = self.__carregar_receitas()

    @property
    def arquivo(self) -> str:
        return self.__arquivo

    @arquivo.setter
    def arquivo(self, _arquivo: str) -> None:
        self.__arquivo = _arquivo

    @property
    def receitas(self) -> List[Receita]:
        return self.__receitas

    @receitas.setter
    def receitas(self, _list: List[Receita]) -> None:
        self.__receitas = _list

    def __carregar_receitas(self) -> List[Receita]:
        """
        Carrega as receitas do arquivo JSON,
        se o arquivo existir.
        """
        if os.path.exists(self.arquivo):
            with open(self.arquivo, "r", encoding="utf-8") as f:
                _dados = json.load(f)
                _receitas: List[Receita] = []
                for _r in _dados:
                    receita = Receita(
                        _r["nome"],
                        _r["tipo"],
                        _r["modo_preparo"],
                        _r["rendimento"],
                        _r["ingredientes"]
                    )
                    _receitas.append(receita)
                return _receitas

    def __salvar_receitas(self):
        """
        Salva as receitas atuais no arquivo JSON.
        """
        _dados = [
            {
                "nome": _r.nome,
                "tipo": _r.tipo,
                "modo_preparo": _r.modo_preparo,
                "rendimento": _r.rendimento,
                "ingredientes": _r.ingredientes
            }
            for _r in self.receitas
        ]
        with open(self.arquivo, "w", encoding="utf-8") as f:
            json.dump(_dados, f, ensure_ascii=False, indent=4)

    def criar(self, receita: Receita) -> bool:
        """
        Adiciona uma nova receita se não existir
        duplicidade de nome.
        :return: True se adicionada ou False se duplicada.
        """
        try:
            if self.buscar_por_nome(receita.nome):
                return False
            self.receitas.append(receita)
            self.__salvar_receitas()
            return True
        except ValueError as ve:
            print(ve)
            return False

    def consultar(self, _i: int) -> Receita:
        return self.receitas[_i]

    def alterar(self, _nova_receita: Receita) -> bool:
        for _i, _receita in enumerate(self.receitas):
            if _receita.nome.lower() == _nova_receita.nome.lower():
                self.receitas[_i] = _nova_receita
                self.__salvar_receitas()
                return True
        return False

    def deletar(self, _nome: str) -> bool:
        _receita = self.buscar_por_nome(_nome)
        if _receita:
            self.receitas.remove(_receita)
            self.__salvar_receitas()
            return True
        return False

    def filtrar_por_ingrediente(self, _ingrediente: str) -> List[Receita]:
        if not _ingrediente.strip():
            return self.receitas
        return [
            _receita
            for _receita in self.receitas
            if _receita.tem_ingrediente(_ingrediente.strip())
        ]

    def buscar_por_nome(self, _nome: str) -> Receita | None:
        for _receita in self.receitas:
            if _receita.nome.lower() == _nome.lower():
                return _receita
        return None
