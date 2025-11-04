import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from Receita import Receita
from Controller import CadernoReceitas


class ReceitasView:
    def __init__(self):
        self.root = root
        self.root.title("Caderno de Receitas")
        self.caderno = CadernoReceitas(_arquivo="receitas.json")
        self.__filtro_ingrediente = tk.StringVar()
        self.item_selecionado = ""

        # ======= Layout principal (grid 2 colunas) =======
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Linha 0: Nome
        tk.Label(self.frm, text="Nome da Receita:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_nome = tk.Entry(self.frm, width=50)
        self.entry_nome.grid(row=0, column=1, sticky="we", pady=4)

        # Linha 1: Tipo
        tk.Label(self.frm, text="Tipo:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(self.frm, width=47, state="readonly",
                                       values=["Entrada", "Prato Principal", "Sobremesa",
                                               "Bebida sem Álcool", "Bebida com Álcool"])
        self.combo_tipo.grid(row=1, column=1, sticky="we", pady=4)

        # Linha 2: Rendimento
        tk.Label(self.frm, text="Rendimento:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_rendimento = tk.Entry(self.frm, width=20)
        self.entry_rendimento.grid(row=2, column=1, sticky="w", pady=4)

        # Linha 3: Ingredientes
        tk.Label(self.frm, text="Ingredientes (nome:quantidade; ...):").grid(row=3, column=0,
                                                                             sticky="e", padx=(0, 8), pady=4)
        self.entry_ingredientes = tk.Text(self.frm, width=50, height=6)
        self.entry_ingredientes.grid(row=3, column=1, sticky="we", pady=4)

        # Linha 4: Modo de Preparo
        tk.Label(self.frm, text="Modo de Preparo:").grid(row=4, column=0, sticky="ne", padx=(0, 8), pady=4)
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

        # Campo filtro por ingrediente
        filtro_frame = tk.Frame(self.frm)
        filtro_frame.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por Ingrediente:").pack(side="left")
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

    @property
    def caderno(self) -> CadernoReceitas:
        return self.__caderno

    @caderno.setter
    def caderno(self, _caderno: CadernoReceitas) -> None:
        self.__caderno = _caderno

    @property
    def item_selecionado(self) -> str:
        return self.__item_selecionado

    @item_selecionado.setter
    def item_selecionado(self, _item: str) -> None:
        self.__item_selecionado = _item

    def __formatar_texto_preparo(self) -> str:
        return self.entry_preparo.get("1.0", tk.END).strip()

    def __formatar_texto_ingredientes(self) -> str:
        return self.entry_ingredientes.get("1.0", tk.END).strip()

    def __montar_receita(self) -> Receita | None:
        _nome = self.entry_nome.get().strip()
        if not _nome:
            messagebox.showerror("Erro", "Informe o nome da receita.")
            return None

        _tipo = self.combo_tipo.get()
        if not _tipo:
            messagebox.showerror("Erro", "Selecione o tipo da receita.")
            return None

        _preparo = self.__formatar_texto_preparo()
        if not _preparo:
            messagebox.showerror("Erro", "Informe o modo de preparo da receita.")
            return None

        try:
            _rendimento = int(self.entry_rendimento.get())
        except ValueError:
            messagebox.showerror("Erro", "Rendimento deve ser número inteiro.")
            return None

        _ingredientes = self.__formatar_texto_ingredientes().strip()
        _dict_ingredientes = {}
        if not _ingredientes:
            messagebox.showerror("Erro", "Informe a lista de ingredientes da receita.")
            return None
        else:
            for item in _ingredientes.split(";"):
                item = item.strip()
                if not item:
                    continue
                try:
                    k, v = item.split(":")
                except ValueError:
                    messagebox.showerror("Erro", "Ingredientes no formato 'nome: quantidade; nome: quantidade; ...'")
                    return None
                if k.strip() and v.strip():
                    _dict_ingredientes[k.strip()] = v.strip()
                else:
                    messagebox.showerror("Erro", "Ingredientes no formato 'nome:quantidade; nome:quantidade; ...'")
                    return None

        return Receita(_nome, _tipo, _preparo, _rendimento, _dict_ingredientes)

    def atualizar_listbox(self):
        self.item_selecionado = self.__filtro_ingrediente.get().strip()
        if self.item_selecionado:
            _lista_receitas = self.caderno.filtrar_por_ingrediente(self.item_selecionado)
        else:
            _lista_receitas = self.caderno.receitas
        self.listbox_receitas.delete(0, tk.END)
        for _r in _lista_receitas:
            self.listbox_receitas.insert(tk.END, f"{_r.nome}")
        self.selecionar()

    def __limpar_campos(self):
        self.entry_nome.config(state='normal')
        self.entry_nome.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_rendimento.delete(0, tk.END)
        self.entry_ingredientes.delete("1.0", tk.END)
        self.entry_preparo.delete("1.0", tk.END)
        self.__btn_atualizar.config(state='disabled')
        self.__btn_remover.config(state='disabled')
        self.__btn_imprimir.config(state='disabled')
        self.__btn_adicionar.config(text='Adicionar')

    def __limpar_filtro(self):
        self.caderno = CadernoReceitas()
        self.__filtro_ingrediente.set("")
        self.item_selecionado = ""
        self.atualizar_listbox()

    def selecionar(self, _event=None):
        _receita_selecionada = self.listbox_receitas.curselection()
        if not _receita_selecionada:
            return
        self.item_selecionado = self.listbox_receitas.get(_receita_selecionada)
        _receita_selecionada = self.caderno.buscar_por_nome(self.item_selecionado)

        self.entry_nome.config(state='normal')
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, _receita_selecionada.nome)
        self.entry_nome.config(state='disabled')

        self.combo_tipo.set(_receita_selecionada.tipo)

        self.entry_rendimento.delete(0, tk.END)
        self.entry_rendimento.insert(0, str(_receita_selecionada.rendimento))

        self.entry_preparo.delete("1.0", tk.END)
        self.entry_preparo.insert(tk.END, _receita_selecionada.modo_preparo)

        self.entry_ingredientes.delete("1.0", tk.END)
        self.entry_ingredientes.insert(tk.END, ";\n".join(f"{k}: {v}"
                                                          for k, v in _receita_selecionada.ingredientes.items()))

        self.__btn_atualizar.config(state='normal')
        self.__btn_imprimir.config(state='normal')
        self.__btn_remover.config(state='normal')
        self.__btn_adicionar.config(text='Novo Registro')

    def adicionar(self):
        if self.__btn_adicionar.cget("text") == 'Novo Registro':
            self.__limpar_campos()
            return
        elif self.__btn_adicionar.cget("text") == 'Adicionar':
            _nova_receita = self.__montar_receita()
            if not _nova_receita:
                return
            elif self.caderno.criar(_nova_receita):
                self.atualizar_listbox()
                messagebox.showinfo("Sucesso", f"Receita '{_nova_receita.nome}' adicionada.")
            else:
                messagebox.showerror("Erro", f"Não foi possível cadastrar a receita '{_nova_receita.nome}'.")

    def atualizar(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma receita para atualizar.")
            return
        _nova_receita = self.__montar_receita()
        if _nova_receita:
            if self.caderno.alterar(_nova_receita):
                messagebox.showinfo("Sucesso", f"Receita '{_nova_receita.nome}' atualizada.")
            else:
                messagebox.showerror("Erro", "Falha ao atualizar. Verifique duplicidade de nome.")

    def remover(self):
        _receita_selecionada = self.listbox_receitas.curselection()
        if not _receita_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma receita para remover.")
            return
        _i = _receita_selecionada[0]
        _nome = self.caderno.consultar(_i).nome
        if self.caderno.deletar(_nome):
            self.atualizar_listbox()
            messagebox.showinfo("Sucesso", f"Receita '{_nome}' removida.")
        else:
            messagebox.showerror("Erro", "Receita não encontrada.")

    def imprimir(self):
        _receita_selecionada = self.listbox_receitas.curselection()
        if not _receita_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma receita para imprimir.")
            return
        _i = _receita_selecionada[0]
        _receita = self.caderno.consultar(_i)

        _caminho = filedialog.asksaveasfilename(
            title="Salvar receita como PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{_receita.nome}.pdf",
        )
        if not _caminho:
            return
        try:
            _receita.imprimir_receita(_caminho)
            messagebox.showinfo("Sucesso", f"PDF gerado em:\n{_caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = ReceitasView()
    root.mainloop()
