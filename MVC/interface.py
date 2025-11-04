import tkinter as tk
from tkinter import messagebox, filedialog, ttk
# from Receita import Receita
# from Controller import CadernoReceitas


class ReceitasView:
    def __init__(self):
        self.root = root
        self.root.title("Minha Aplicação")
        # self.caderno = CadernoReceitas(_arquivo="receitas.json")
        self.__filtro_ingrediente = tk.StringVar()
        self.item_selecionado = ""

        # ======= Layout principal (grid 2 colunas) =======
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Linha 0: Nome
        tk.Label(self.frm, text="Produtor:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_nome = tk.Entry(self.frm, width=50)
        self.entry_nome.grid(row=0, column=1, sticky="we", pady=4)

        # Linha 1: Tipo
        tk.Label(self.frm, text="Fazenda:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_ingredientes = tk.Text(self.frm, width=50, height=1)
        self.entry_ingredientes.grid(row=1, column=1, sticky="we", pady=4)

        # Linha 2: Rendimento
        tk.Label(self.frm, text="Talhão:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_rendimento = tk.Entry(self.frm, width=50)
        self.entry_rendimento.grid(row=2, column=1, sticky="we", pady=4)

        # Linha 3: Ingredientes
        tk.Label(self.frm, text="Tipo de Solo:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(self.frm, width=47, state="readonly",
                                       values=["Entrada", "Prato Principal", "Sobremesa",
                                               "Bebida sem Álcool", "Bebida com Álcool"])
        self.combo_tipo.grid(row=3, column=1, sticky="we", pady=4)

        # Linha 4: Modo de Preparo
        tk.Label(self.frm, text="Resultado da Análise (pH, P, K, MO...):").grid(row=4, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_preparo = tk.Text(self.frm, width=50, height=6)
        self.entry_preparo.grid(row=4, column=1, sticky="we", pady=4)

        # Botões
        botoes = tk.Frame(self.frm)
        botoes.grid(row=5, column=0, columnspan=2, pady=(6, 10))
        self.__btn_adicionar = tk.Button(botoes, text="Adicionar", command=self.adicionar, state='normal')
        self.__btn_adicionar.grid(row=0, column=0, padx=4)

        self.__btn_atualizar = tk.Button(botoes, text="Atualizar", command=self.atualizar, state='disabled')
        self.__btn_atualizar.grid(row=0, column=1, padx=4)

        self.__btn_remover = tk.Button(botoes, text="Remover", command=self.remover, state='disabled')
        self.__btn_remover.grid(row=0, column=2, padx=4)

        self.__btn_imprimir = tk.Button(botoes, text="Imprimir",  command=self.imprimir, state='disabled')
        self.__btn_imprimir.grid(row=0, column=3, padx=4)

        self.__btn_limpar = tk.Button(botoes, text="Limpar",  command=self.__limpar_campos, state='normal')
        self.__btn_limpar.grid(row=0, column=4, padx=4)

        # Campo filtro por ingrediente
        filtro_frame = tk.Frame(self.frm)
        filtro_frame.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por ...:").pack(side="left")
        filtro_entry = tk.Entry(filtro_frame, textvariable=self.__filtro_ingrediente, width=30)
        filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.atualizar_listbox).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpar", command=self.__limpar_filtro).pack(side="left")

        # Lista de receitas
        self.listbox_receitas = tk.Listbox(self.frm, width=75, height=10)
        self.listbox_receitas.grid(row=7, column=0, columnspan=2, sticky="we")
        self.listbox_receitas.bind("<<ListboxSelect>>", self.selecionar)

        # Ajuste das colunas
        self.frm.grid_columnconfigure(1, weight=1)

        # Carregar lista
        self.atualizar_listbox()

#    @property
#    def caderno(self) -> CadernoReceitas:
#        return self.__caderno

#    @caderno.setter
#    def caderno(self, _caderno: CadernoReceitas) -> None:
#        self.__caderno = _caderno

#    @property
#    def item_selecionado(self) -> str:
#        return self.__item_selecionado

#    @item_selecionado.setter
#    def item_selecionado(self, _item: str) -> None:
#        self.__item_selecionado = _item

#    def __montar_objeto(self) -> meuObjeto | None:
#        _nome = self.entry_nome.get().strip()
#        if not _nome:
#            messagebox.showerror("Erro", "Informe o nome da receita.")
#            return None

    def atualizar_listbox(self):
        pass

    def __limpar_campos(self):
        # self.entry_nome.config(state='normal')
        pass

    def __limpar_filtro(self):
        pass

    def selecionar(self, _event=None):
        pass

    def adicionar(self):
        pass

    def atualizar(self):
        pass

    def remover(self):
        pass

    def imprimir(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = ReceitasView()
    root.mainloop()
