# PerfilProdutor.py
from __future__ import annotations
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap
from typing import Union


class PerfilProdutor:
    def __init__(self,
                 _produtor: str,
                 _tipo_solos: str,
                 _fazenda: Union[str, dict],
                 _talhao: Union[int, str],
                 _ph: float,
                 _p: float,
                 _k: float):
        self.produtor = _produtor
        self.tipo_solos = _tipo_solos
        self.fazenda = _fazenda
        self.talhao = _talhao
        self.ph = float(_ph)
        self.p = float(_p)
        self.k = float(_k)

    # properties simples (opcionais) - mantidas para compatibilidade
    @property
    def produtor(self) -> str:
        return self.__produtor

    @produtor.setter
    def produtor(self, v: str) -> None:
        self.__produtor = str(v).strip()

    @property
    def tipo_solos(self) -> str:
        return self.__tipo_solos

    @tipo_solos.setter
    def tipo_solos(self, v: str) -> None:
        self.__tipo_solos = str(v).strip()

    @property
    def fazenda(self) -> Union[str, dict]:
        return self.__fazenda

    @fazenda.setter
    def fazenda(self, v: Union[str, dict]) -> None:
        self.__fazenda = v

    @property
    def talhao(self) -> Union[int, str]:
        return self.__talhao

    @talhao.setter
    def talhao(self, v: Union[int, str]) -> None:
        self.__talhao = v

    @property
    def ph(self) -> float:
        return self.__ph

    @ph.setter
    def ph(self, v: float) -> None:
        self.__ph = float(v)

    @property
    def p(self) -> float:
        return self.__p

    @p.setter
    def p(self, v: float) -> None:
        self.__p = float(v)

    @property
    def k(self) -> float:
        return self.__k

    @k.setter
    def k(self, v: float) -> None:
        self.__k = float(v)


    def imprimir_cadastro(self, caminho: str) -> None:
        """
        Gera um PDF contendo os dados do perfil.
        caminho: caminho completo para salvar o PDF (ex: '/home/user/arquivo.pdf')
        """
        c = canvas.Canvas(caminho, pagesize=A4)
        largura, altura = A4
        x_margin = 50
        y = altura - 50

        c.setFont("Helvetica-Bold", 16)
        c.drawString(x_margin, y, f"Perfil do Produtor: {self.produtor}")
        y -= 30

        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Informações gerais:")
        y -= 20

        c.setFont("Helvetica", 11)
        c.drawString(x_margin, y, f"- Tipo de solo: {self.tipo_solos}")
        y -= 18
        c.drawString(x_margin, y, f"- Talhão: {self.talhao}")
        y -= 18
        c.drawString(x_margin, y, f"- pH: {self.ph}")
        y -= 18
        c.drawString(x_margin, y, f"- P: {self.p}")
        y -= 18
        c.drawString(x_margin, y, f"- K: {self.k}")
        y -= 24

        # Fazenda: pode ser string longa ou dicionário de informações
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_margin, y, "Fazenda / Observações:")
        y -= 18
        c.setFont("Helvetica", 11)

        if isinstance(self.fazenda, dict):
            for key, val in self.fazenda.items():
                linha = f"- {key}: {val}"
                for sub in wrap(linha, width=90):
                    c.drawString(x_margin + 10, y, sub)
                    y -= 16
                    if y < 80:
                        c.showPage()
                        y = altura - 50
        else:
            text = str(self.fazenda)
            for linha in wrap(text, width=90):
                c.drawString(x_margin + 10, y, linha)
                y -= 16
                if y < 80:
                    c.showPage()
                    y = altura - 50

        c.save()
