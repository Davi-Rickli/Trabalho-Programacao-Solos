import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from PerfilProdutor import PerfilProdutor
from Controller import ControllerPerfilProdutor


class CadastrosView:
    def __init__(self):
        self.root = root
        self.root.title("Minha Aplicação")
        self.listaPerfilProdutor = ControllerPerfilProdutor(_arquivo="Cadastros.json")
        self.__filtro_Produtor = tk.StringVar()
        self.item_selecionado = ""

        # ======= Layout principal (grid 2 colunas) =======
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Linha 0: produtor
        tk.Label(self.frm, text="Produtor:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_produtor = tk.Entry(self.frm, width=50)
        self.entry_produtor.grid(row=0, column=1, sticky="we", pady=4)

        # Linha 1: Tipo
        tk.Label(self.frm, text="Fazenda:").grid(row=1, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_fazenda = tk.Text(self.frm, width=50, height=1)
        self.entry_fazenda.grid(row=1, column=1, sticky="we", pady=4)

        # Linha 2: Produtor
        tk.Label(self.frm, text="Talhão:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_talhao = tk.Entry(self.frm, width=50)
        self.entry_talhao.grid(row=2, column=1, sticky="we", pady=4)

        # Linha 3: tipodesolos
        tk.Label(self.frm, text="Tipo de Solo:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(self.frm, width=47, state="readonly",
                                       values=["Argissolos", "Cambissolos", "Chernossolos",
                                               "Espodossolos", "Gleissolos", "Latossolos", "Luvissolos", "Neossolos",
                                               "Nitossolos",
                                               "Organossolos", "Planossolos", "Plintossolos", "Vertissolos"])
        self.combo_tipo.grid(row=3, column=1, sticky="we", pady=4)

        # Linha 4: Modo de Preparo
        tk.Label(self.frm, text="Resultado da Análise PH:").grid(row=4, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_ph = tk.Text(self.frm, width=50, height=1)
        self.entry_ph.grid(row=4, column=1, sticky="we", pady=4)

        tk.Label(self.frm, text="Resultado da Análise P:").grid(row=5, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_p = tk.Text(self.frm, width=50, height=1)
        self.entry_p.grid(row=5, column=1, sticky="we", pady=4)

        tk.Label(self.frm, text="Resultado da Análise K:").grid(row=6, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_k = tk.Text(self.frm, width=50, height=1)
        self.entry_k.grid(row=6, column=1, sticky="we", pady=4)

        # Botões
        botoes = tk.Frame(self.frm)
        botoes.grid(row=7, column=0, columnspan=2, pady=(6, 10))
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
        filtro_frame.grid(row=8, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por ...:").pack(side="left")
        filtro_entry = tk.Entry(filtro_frame, textvariable=self.__filtro_Produtor, width=30)
        filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.__atualizar_listbox).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpar", command=self.__limpar_filtro).pack(side="left")

        # Lista de Cadastros
        self.listbox_Cadastros = tk.Listbox(self.frm, width=75, height=10)
        self.listbox_Cadastros.grid(row=9, column=0, columnspan=2, sticky="we")
        self.listbox_Cadastros.bind("<<ListboxSelect>>", self.selecionar)

        # Ajuste das colunas
        self.frm.grid_columnconfigure(1, weight=1)

        # Carregar lista
        self.__atualizar_listbox()

    @property
    def listaPerfilProdutor(self) -> ControllerPerfilProdutor:
        return self.__caderno

    @listaPerfilProdutor.setter
    def listaPerfilProdutor(self, _caderno: ControllerPerfilProdutor) -> None:
        self.__caderno = _caderno

    @property
    def item_selecionado(self) -> str:
        return self.__item_selecionado

    @item_selecionado.setter
    def item_selecionado(self, _item: str) -> None:
        self.__item_selecionado = _item

    @property
    def __montar_cadastro(self) -> PerfilProdutor | None:
        _produtor = self.entry_produtor.get().strip()
        if not _produtor:
            messagebox.showerror("Erro", "Informe o produtor do Cadastro.")
            return None

        _fazenda = self.entry_fazenda.get("1.0", "end-1c").strip()
        if not _fazenda:
            messagebox.showerror("Erro", "Informe a fazenda do Cadastro.")
            return None

        _talhao = self.entry_talhao.get().strip()
        if not _talhao:
            messagebox.showerror("Erro", "Informe o talhao do Cadastro.")
            return None

        try:
            _ph = float(self.entry_ph.get("1.0", "end-1c"))
            _p = float(self.entry_p.get("1.0", "end-1c"))
            _k = float(self.entry_k.get("1.0", "end-1c"))
        except ValueError:
            messagebox.showerror("Erro", "PH, P e K devem ser números.")
            return None

        return PerfilProdutor(_produtor, _fazenda, _fazenda, _talhao, _ph, _p, _k)

    def __atualizar_listbox(self):
        """self.item_selecionado = self.__filtro_fazenda.get().strip()
        if self.item_selecionado:
            _lista_Cadastros = self.listaPerfilProdutor.filtrar_por_ingrediente(self.item_selecionado)
        else:
            _lista_Cadastros = self.listaPerfilProdutor.cadastros
        self.listbox_Cadastros.delete(0, tk.END)
        for _r in _lista_Cadastros:
            self.listbox_Cadastros.insert(tk.END, f"{_r.fazenda}")
        self.selecionar()"""
        pass

    def __limpar_campos(self):
        self.entry_produtor.config(state='normal')
        self.entry_produtor.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_ph.delete(0, tk.END)
        self.entry_fazenda.delete("1.0", tk.END)
        self.entry_fazenda.delete("1.0", tk.END)
        self.__btn_atualizar.config(state='disabled')
        self.__btn_remover.config(state='disabled')
        self.__btn_imprimir.config(state='disabled')
        self.__btn_adicionar.config(text='Adicionar')

    def __limpar_filtro(self):
        self.listaPerfilProdutor = ControllerPerfilProdutor()
        self.__filtro_fazenda.set("")
        self.item_selecionado = ""
        self.atualizar_listbox()

    def selecionar(self, _event=None):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            return
        self.item_selecionado = self.listbox_Cadastros.get(_Cadastro_selecionada)
        _Cadastro_selecionada = self.listaPerfilProdutor.buscar_por_produtor(self.item_selecionado)

        self.entry_produtor.config(state='normal')
        self.entry_produtor.delete(0, tk.END)
        self.entry_produtor.insert(0, _Cadastro_selecionada.produtor)
        self.entry_produtor.config(state='disabled')

        self.combo_tipo.set(_Cadastro_selecionada.tipo_solos)

        self.entry_ph.delete(0, tk.END)
        self.entry_ph.insert(0, str(_Cadastro_selecionada.ph))

        self.entry_fazenda.delete("1.0", tk.END)
        self.entry_fazenda.insert(tk.END, _Cadastro_selecionada.fazenda)

        self.entry_fazenda.delete("1.0", tk.END)
        self.entry_fazenda.insert(tk.END, ";\n".join(f"{k}: {v}"
                                                          for k, v in _Cadastro_selecionada.fazenda.items()))

        self.__btn_atualizar.config(state='normal')
        self.__btn_imprimir.config(state='normal')
        self.__btn_remover.config(state='normal')
        self.__btn_adicionar.config(text='Novo Registro')

    def adicionar(self):
        if self.__btn_adicionar.cget("text") == 'Novo Registro':
            self.__limpar_campos()
            return
        elif self.__btn_adicionar.cget("text") == 'Adicionar':
            _nova_Cadastro = self.__montar_cadastro
            if not _nova_Cadastro:
                return
            elif self.listaPerfilProdutor.criar(_nova_Cadastro):
                self.atualizar_listbox()
                messagebox.showinfo("Sucesso", f"Cadastro '{_nova_Cadastro.produtor}' adicionada.")
            else:
                messagebox.showerror("Erro", f"Não foi possível cadastrar a Cadastro '{_nova_Cadastro.produtor}'.")

    def atualizar(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para atualizar.")
            return
        _nova_Cadastro = self.__montar_cadastro
        if _nova_Cadastro:
            if self.listaPerfilProdutor.alterar(_nova_Cadastro):
                messagebox.showinfo("Sucesso", f"Cadastro '{_nova_Cadastro.produtor}' atualizada.")
            else:
                messagebox.showerror("Erro", "Falha ao atualizar. Verifique duplicidade de produtor.")

    def remover(self):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para remover.")
            return
        _i = _Cadastro_selecionada[0]
        _produtor = self.listaPerfilProdutor.consultar(_i).produtor
        if self.listaPerfilProdutor.deletar(_produtor):
            self.atualizar_listbox()
            messagebox.showinfo("Sucesso", f"Cadastro '{_produtor}' removida.")
        else:
            messagebox.showerror("Erro", "Cadastro não encontrada.")

    def imprimir(self):
        _Cadastro_selecionada = self.listbox_Cadastros.curselection()
        if not _Cadastro_selecionada:
            messagebox.showwarning("Aviso", "Selecione uma Cadastro para imprimir.")
            return
        _i = _Cadastro_selecionada[0]
        _Cadastro = self.listaPerfilProdutor.consultar(_i)

        _caminho = filedialog.asksaveasfilename(
            title="Salvar Cadastro como PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{_Cadastro.produtor}.pdf",
        )
        if not _caminho:
            return
        try:
            _Cadastro.imprimir_Cadastro(_caminho)
            messagebox.showinfo("Sucesso", f"PDF gerado em:\n{_caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))

    def __formatar_texto_fazenda(self):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastrosView()
    root.mainloop()
