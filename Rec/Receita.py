from __future__ import annotations
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from textwrap import wrap


class Receita:

    def __init__(self, _nome: str, _tipo: str,
                 _modo_preparo: str, _rendimento: int,
                 _ingredientes: dict):
        self.nome = _nome
        self.tipo = _tipo
        self.modo_preparo = _modo_preparo
        self.rendimento = _rendimento
        self.ingredientes = _ingredientes

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, _nome: str) -> None:
        self.__nome = _nome

    @property
    def tipo(self) -> str:
        return self.__tipo

    @tipo.setter
    def tipo(self, _tipo: str) -> None:
        self.__tipo = _tipo

    @property
    def modo_preparo(self) -> str:
        return self.__modo_preparo

    @modo_preparo.setter
    def modo_preparo(self, _modo_preparo: str) -> None:
        self.__modo_preparo = _modo_preparo

    @property
    def rendimento(self) -> int:
        return self.__rendimento

    @rendimento.setter
    def rendimento(self, _rendimento: int) -> None:
        self.__rendimento = _rendimento

    @property
    def ingredientes(self) -> dict:
        return self.__ingredientes

    @ingredientes.setter
    def ingredientes(self, _ingredientes: dict) -> None:
        if type(_ingredientes) is not dict or len(_ingredientes) <= 0:
            raise ValueError("A lista de ingredientes precisa estar organizada como um dicionário")
        self.__ingredientes = _ingredientes

    def tem_ingrediente(self, _ingrediente: str) -> bool:
        return _ingrediente in self.__ingredientes

    def imprimir_receita(self, _caminho: str) -> None:
        """Gera um PDF da receita."""
        _arquivo = canvas.Canvas(_caminho, pagesize=A4)
        _largura, _altura = A4

        y = _altura - 50
        _arquivo.setFont("Helvetica-Bold", 16)
        _arquivo.drawString(50, y, f"Receita: {self.nome}")
        y -= 30

        _arquivo.setFont("Helvetica", 12)
        _arquivo.drawString(50, y, f"Tipo: {self.tipo}")
        y -= 20
        _arquivo.drawString(50, y, f"Rendimento: {self.rendimento}")
        y -= 30

        _arquivo.setFont("Helvetica-Bold", 12)
        _arquivo.drawString(50, y, "Ingredientes:")
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
        _arquivo.drawString(50, y, "Modo de Preparo:")
        y -= 20

        _arquivo.setFont("Helvetica", 12)
        for linha in wrap(self.modo_preparo, width=80):
            _arquivo.drawString(70, y, linha)
            y -= 20
            if y < 100:
                _arquivo.showPage()
                y = _altura - 50

        _arquivo.save()


if __name__ == "__main__":
    print("Criando um objeto válido")
    receita1 = Receita("Brigadeiro de Panela",
                       "Sobremesa",
                       "1) Junte esses ingredientes numa panela. "
                       "Adicione o achocolatado e a manteiga, "
                       "e mexa até criar consistência, ou seja, "
                       "até começar a engrossar. 2) Despeje tudo "
                       "numa vasilha de vidro e leve a geladeira. "
                       "Espere aproximadamente uma hora e meia, e "
                       "está pronto, é só se deliciar!",
                       10,
                       {"leite condensado": "1 lata",
                        "manteiga": "2 colheres de sopa",
                        "achocolatado": "4 colheres de sopa"}
                       )
    receita1.imprimir_receita("receita.pdf")
    print(receita1)
    print(f"A receita têm azeite? "
          f"{receita1.tem_ingrediente('azeite')}")
    print(f"A receita têm leite condensado? "
          f"{receita1.tem_ingrediente('leite condensado')}")
