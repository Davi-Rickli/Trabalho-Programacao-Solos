import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from Cadastro import Cadastro
from Controller import CadernoCadastros


class CadastrosView:
    def __init__(self):
        self.root = root
        self.root.title("Caderno de Cadastros")
        self.caderno = CadernoCadastros(_arquivo="Cadastro.json")
        self.__filtro_ingrediente = tk.StringVar()
        self.item_selecionado = ""

        # ======= Layout principal (grid 2 colunas) =======
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Linha 0: Nome
        tk.Label(self.frm, text="Nome do produtor:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_nome = tk.Entry(self.frm, width=50)
        self.entry_nome.grid(row=0, column=1, sticky="we", pady=4)

        # Linha 1: Tipo
        tk.Label(self.frm, text="Tipo do solo:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(self.frm, width=47, state="readonly",
                                       values=["Argissolos", "Cambissolos", "Chernossolos",
                                               "Espodossolos", "Gleissolos", "Latossolos", "Luvissolos", "Neossolos", "Nitossolos",
                                               "Organossolos", "Planossolos", "Plintossolos", "Vertissolos"])
        self.combo_tipo.grid(row=1, column=1, sticky="we", pady=4)

        # Linha 2: ph
        tk.Label(self.frm, text="PH:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_ph = tk.Entry(self.frm, width=20)
        self.entry_ph.grid(row=2, column=1, sticky="w", pady=4)

        # Linha 3: p
        tk.Label(self.frm, text="p:").grid(row=3, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_p = tk.Text(self.frm, width=50, height=6)
        self.entry_p.grid(row=3, column=1, sticky="we", pady=4)
        
        # Linha 4: k
        tk.Label(self.frm, text="k:").grid(row=4, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_k = tk.Text(self.frm, width=50, height=6)
        self.entry_k.grid(row=4, column=1, sticky="we", pady=4)

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

        # Campo filtro por produtor
        filtro_frame = tk.Frame(self.frm)
        filtro_frame.grid(row=6, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por Produtor:").pack(side="left")
        filtro_entry = tk.Entry(filtro_frame, textvariable=self.__filtro_produtor, width=30)
        filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.atualizar_listbox).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpar", command=self.__limpar_filtro).pack(side="left")

        # Lista de Cadastros
        self.listbox_Cadastros = tk.Listbox(self.frm, width=75, height=10)
        self.listbox_Cadastros.grid(row=7, column=0, columnspan=2, sticky="we")
        self.listbox_Cadastros.bind("<<ListboxSelect>>", self.selecionar)

        # Ajuste das colunas
        self.frm.grid_columnconfigure(1, weight=1)

        # Carregar lista
        self.atualizar_listbox()

    @property
    def caderno(self) -> CadernoCadastros:
        return self.__caderno

    @caderno.setter
    def caderno(self, _caderno: CadernoCadastros) -> None:
        self.__caderno = _caderno

    @property
    def item_selecionado(self) -> str:
        return self.__item_selecionado

    @item_selecionado.setter
    def item_selecionado(self, _item: str) -> None:
        self.__item_selecionado = _item

    def __formatar_texto_preparo(self) -> str:
        return self.entry_fazenda.get("1.0", tk.END).strip()

    def __formatar_texto_produtor(self) -> str:
        return self.entry_produtor.get("1.0", tk.END).strip()

    def __montar_Cadastro(self) -> Cadastro | None:
        _nome = self.entry_nome.get().strip()
        if not _nome:
            messagebox.showerror("Erro", "Informe o nome da Cadastro.")
            return None

        _tipo = self.combo_tipo.get()
        if not _tipo:
            messagebox.showerror("Erro", "Selecione o tipo da Cadastro.")
            return None

        _preparo = self.__formatar_texto_preparo()
        if not _preparo:
            messagebox.showerror("Erro", "Informe o ph da Cadastro.")
            return None

        try:
            _ph = int(self.entry_ph.get())
        except ValueError:
            messagebox.showerror("Erro", "ph deve ser número inteiro.")
            return None

        _ingredientes = self.__formatar_texto_ingredientes().strip()
        _dict_ingredientes = {}
        if not _ingredientes:
            messagebox.showerror("Erro", "Informe a lista de ingredientes da Cadastro.")
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

        return Cadastro(_nome, _tipo, _preparo, _ph, _dict_ingredientes)

    def atualizar_listbox(self):
        self.item_selecionado = self.__filtro_ingrediente.get().strip()
        if self.item_selecionado:
            _lista_Cadastros = self.caderno.filtrar_por_ingrediente(self.item_selecionado)
        else:
            _lista_Cadastros = self.caderno.Cadastros
        self.listbox_Cadastros.delete(0, tk.END)
        for _r in _lista_Cadastros:
            self.listbox_Cadastros.insert(tk.END, f"{_r.nome}")
        self.selecionar()

    def __limpar_campos(self):
        self.entry_nome.config(state='normal')
        self.entry_nome.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_ph.delete(0, tk.END)
        self.entry_ingredientes.delete("1.0", tk.END)
        self.entry_fazenda.delete("1.0", tk.END)
        self.__btn_atualizar.config(state='disabled')
        self.__btn_remover.config(state='disabled')
        self.__btn_imprimir.config(state='disabled')
        self.__btn_adicionar.config(text='Adicionar')

    def __limpar_filtro(self):
        self.caderno = CadernoCadastros()
        self.__filtro_ingrediente.set("")
        self.item_selecionado = ""
        self.atualizar_listbox()

    def selecionar(self, _event=None):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            return
        self.item_selecionado = self.listbox_Cadastros.get(_Cadastro_selecionada)
        _Cadastro_selecionada = self.caderno.buscar_por_nome(self.item_selecionado)

        self.entry_nome.config(state='normal')
        self.entry_nome.delete(0, tk.END)
        self.entry_nome.insert(0, _Cadastro_selecionada.nome)
        self.entry_nome.config(state='disabled')

        self.combo_tipo.set(_Cadastro_selecionada.tipo)

        self.entry_ph.delete(0, tk.END)
        self.entry_ph.insert(0, str(_Cadastro_selecionada.ph))

        self.entry_fazenda.delete("1.0", tk.END)
        self.entry_fazenda.insert(tk.END, _Cadastro_selecionada.modo_preparo)

        self.entry_ingredientes.delete("1.0", tk.END)
        self.entry_ingredientes.insert(tk.END, ";\n".join(f"{k}: {v}"
                                                          for k, v in _Cadastro_selecionada.ingredientes.items()))

        self.__btn_atualizar.config(state='normal')
        self.__btn_imprimir.config(state='normal')
        self.__btn_remover.config(state='normal')
        self.__btn_adicionar.config(text='Novo Registro')

    def adicionar(self):
        if self.__btn_adicionar.cget("text") == 'Novo Registro':
            self.__limpar_campos()
            return
        elif self.__btn_adicionar.cget("text") == 'Adicionar':
            _nova_Cadastro = self.__montar_Cadastro()
            if not _nova_Cadastro:
                return
            elif self.caderno.criar(_nova_Cadastro):
                self.atualizar_listbox()
                messagebox.showinfo("Sucesso", f"Cadastro '{_nova_Cadastro.nome}' adicionada.")
            else:
                messagebox.showerror("Erro", f"Não foi possível cadastrar a Cadastro '{_nova_Cadastro.nome}'.")

    def atualizar(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para atualizar.")
            return
        _nova_Cadastro = self.__montar_Cadastro()
        if _nova_Cadastro:
            if self.caderno.alterar(_nova_Cadastro):
                messagebox.showinfo("Sucesso", f"Cadastro '{_nova_Cadastro.nome}' atualizada.")
            else:
                messagebox.showerror("Erro", "Falha ao atualizar. Verifique duplicidade de nome.")

    def remover(self):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para remover.")
            return
        _i = _Cadastro_selecionada[0]
        _nome = self.caderno.consultar(_i).nome
        if self.caderno.deletar(_nome):
            self.atualizar_listbox()
            messagebox.showinfo("Sucesso", f"Cadastro '{_nome}' removida.")
        else:
            messagebox.showerror("Erro", "Cadastro não encontrada.")

    def imprimir(self):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para imprimir.")
            return
        _i = _Cadastro_selecionada[0]
        _Cadastro = self.caderno.consultar(_i)

        _caminho = filedialog.asksaveasfilename(
            title="Salvar Cadastro como PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{_Cadastro.nome}.pdf",
        )
        if not _caminho:
            return
        try:
            _Cadastro.imprimir_Cadastro(_caminho)
            messagebox.showinfo("Sucesso", f"PDF gerado em:\n{_caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastrosView()
    root.mainloop()
