import tkinter as tk
from tkinter import messagebox, filedialog, ttk


class SoloView:
    def __init__(self, root):
        self.root = root
        self.root.title("Gerenciamento de Solo - Fazendas")
        self.__filtro = tk.StringVar()
        self.item_selecionado = ""

        # ======= Layout principal =======
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Linha 0: Produtor/Técnico
        tk.Label(self.frm, text="Produtor/Técnico:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_produtor = tk.Entry(self.frm, width=50)
        self.entry_produtor.grid(row=0, column=1, sticky="we", pady=4)

        # Linha 1: Fazenda
        tk.Label(self.frm, text="Fazenda:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_fazenda = tk.Entry(self.frm, width=50)
        self.entry_fazenda.grid(row=1, column=1, sticky="we", pady=4)

        # Linha 2: Talhão
        tk.Label(self.frm, text="Talhão:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_talhao = tk.Entry(self.frm, width=50)
        self.entry_talhao.grid(row=2, column=1, sticky="we", pady=4)

        # Linha 3: Tipo de Solo
        tk.Label(self.frm, text="Tipo de Solo:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo_solo = ttk.Combobox(self.frm, width=47, state="readonly",
                                            values=["Argiloso", "Arenoso", "Misto", "Latossolo", "Gleissolo", "Cambissolo"])
        self.combo_tipo_solo.grid(row=3, column=1, sticky="we", pady=4)

        # Linha 4: Resultados de Análise do Solo
        tk.Label(self.frm, text="Resultado da Análise (pH, P, K, MO...):").grid(row=4, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_analise = tk.Text(self.frm, width=50, height=6)
        self.entry_analise.grid(row=4, column=1, sticky="we", pady=4)

        # Botões
        botoes = tk.Frame(self.frm)
        botoes.grid(row=5, column=0, columnspan=2, pady=(6, 10))
        self.btn_adicionar = tk.Button(botoes, text="Adicionar", command=self.adicionar)
        self.btn_adicionar.grid(row=0, column=0, padx=4)

        self.btn_atualizar = tk.Button(botoes, text="Atualizar", command=self.atualizar, state='disabled')
        self.btn_atualizar.grid(row=0, column=1, padx=4)

        self.btn_remover = tk.Button(botoes, text="Remover", command=self.remover, state='disabled')
        self.btn_remover.grid(row=0, column=2, padx=4)

        self.btn_imprimir = tk.Button(botoes, text="Imprimir", command=self.imprimir, state='disabled')
        self.btn_imprimir.grid(row=0, column=3, padx=4)

        self.btn_limpar = tk.Button(botoes, text="Limpar", command=self.limpar_campos)
        self.btn_limpar.grid(row=0, column=4, padx=4)

        # Filtro
        filtro_frame = tk.Frame(self.frm)
        filtro_frame.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por Fazenda ou Talhão:").pack(side="left")
        filtro_entry = tk.Entry(filtro_frame, textvariable=self.__filtro, width=30)
        filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.atualizar_listbox).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpar", command=self.limpar_filtro).pack(side="left")

        # Lista de análises
        self.listbox = tk.Listbox(self.frm, width=75, height=10)
        self.listbox.grid(row=7, column=0, columnspan=2, sticky="we")
        self.listbox.bind("<<ListboxSelect>>", self.selecionar)

        # Ajuste coluna
        self.frm.grid_columnconfigure(1, weight=1)
        self.atualizar_listbox()

    # ==== Métodos base para conectar ao Controller ====
    def atualizar_listbox(self):
        pass

    def limpar_campos(self):
        self.entry_produtor.delete(0, tk.END)
        self.entry_fazenda.delete(0, tk.END)
        self.entry_talhao.delete(0, tk.END)
        self.entry_analise.delete("1.0", tk.END)
        self.combo_tipo_solo.set("")

    def limpar_filtro(self):
        self.__filtro.set("")
        self.atualizar_listbox()

    def selecionar(self, event=None):
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
    app = SoloView(root)
    root.mainloop()
