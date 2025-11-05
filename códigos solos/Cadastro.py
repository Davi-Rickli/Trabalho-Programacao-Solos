from __future__ import annotations
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap


class Cadastro:

    def __init__(self, _produtor: str, _tipo_solos: str,
                 _fazenda: str, _talhao: int,
                 _ph: float, _p: float, _k: float):
        self.produtor = _produtor
        self.tipo_solos = _tipo_solos
        self.fazenda = _fazenda
        self.talhao = _talhao
        self.ph = _ph
        self.p = _p
        self.k = _k

    @property
    def produtor(self) -> str:
        return self.__produtor

    @produtor.setter
    def produtor(self, _produtor: str) -> None:
        self.__produtor = _produtor

    @property
    def tipo_solos(self) -> str:
        return self.__tipo_solos

    @tipo_solos.setter
    def tipo_solos(self, _tipo_solos: str) -> None:
        self.__tipo_solos = _tipo_solos

    @property
    def fazenda(self) -> str:
        return self.__fazenda

    @fazenda.setter
    def fazenda(self, _fazenda: str) -> None:
        self.__fazenda = _fazenda

    @property
    def talhao(self) -> int:
        return self.__talhao

    @talhao.setter
    def talhao(self, _talhao: int) -> None:
        self.__talhao = _talhao

    @property
    def ph(self) -> float:
        return self.__ph

    @ph.setter
    def ph(self, _ph: float) -> None:
        self.__ph = _ph

    @property
    def p(self) -> float:
        return self.__p

    @p.setter
    def p(self, _p: float) -> None:
        self.__p = _p

    @property
    def k(self) -> float:
        return self.__k

    @k.setter
    def k(self, _k: float) -> None:
        self.__k = _k


    def imprimir_cadastro(self, _caminho: str) -> None:
        """Gera um PDF do cadastro."""
        _arquivo = canvas.Canvas(_caminho, pagesize=A4)
        _largura, _altura = A4

        y = _altura - 50
        _arquivo.setFont("Helvetica-Bold", 16)
        _arquivo.drawString(50, y, f"Receita: {self.produtor}")
        y -= 30

        _arquivo.setFont("Helvetica", 12)
        _arquivo.drawString(50, y, f"tipo_solos: {self.tipo_solos}")
        y -= 20
        _arquivo.drawString(50, y, f"talhao: {self.talhao}")
        y -= 30

        _arquivo.setFont("Helvetica-Bold", 12)
        _arquivo.drawString(50, y, "ph:")
        y -= 20

        _arquivo.setFont("Helvetica", 12)
        for ing, qtd in self.ingredientes.items():
            _arquivo.drawString(70, y, f"- {qtd} de {ing}")
            y -= 20
            if y < 100:
                _arquivo.showPage()
                y = _altura - 50

        y -= 10
        _arquivo.setFont("Helvetica-Bold", 12)
        _arquivo.drawString(50, y, "Fazenda:")
        y -= 20

        _arquivo.setFont("Helvetica", 12)
        for linha in wrap(self.fazenda, width=80):
            _arquivo.drawString(70, y, linha)
            y -= 20
            if y < 100:
                _arquivo.showPage()
                y = _altura - 50

        _arquivo.save()

