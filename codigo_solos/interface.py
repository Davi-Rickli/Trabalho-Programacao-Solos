# interface.py
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from Controller import ControllerPerfilProdutor
from PerfilProdutor import PerfilProdutor


class CadastrosView:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro Perfil Produtor")
        self.listaPerfilProdutor = ControllerPerfilProdutor(_arquivo="Cadastros.json")
        self.__filtro_produtor = tk.StringVar()
        self.item_selecionado = None

        # layout
        self.frm = tk.Frame(root, padx=10, pady=10)
        self.frm.pack(fill="both", expand=True)

        # Produtor
        tk.Label(self.frm, text="Produtor:").grid(row=0, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_produtor = tk.Entry(self.frm, width=50)
        self.entry_produtor.grid(row=0, column=1, sticky="we", pady=4)

        # Fazenda (texto)
        tk.Label(self.frm, text="Fazenda / Observações:").grid(row=1, column=0, sticky="ne", padx=(0, 8), pady=4)
        self.entry_fazenda = tk.Text(self.frm, width=50, height=3)
        self.entry_fazenda.grid(row=1, column=1, sticky="we", pady=4)

        # Talhão
        tk.Label(self.frm, text="Talhão:").grid(row=2, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_talhao = tk.Entry(self.frm, width=50)
        self.entry_talhao.grid(row=2, column=1, sticky="we", pady=4)

        # Tipo de solo
        tk.Label(self.frm, text="Tipo de Solo:").grid(row=3, column=0, sticky="e", padx=(0, 8), pady=4)
        self.combo_tipo = ttk.Combobox(self.frm, width=47, state="readonly",
                                       values=["Argissolos", "Cambissolos", "Chernossolos",
                                               "Espodossolos", "Gleissolos", "Latossolos", "Luvissolos", "Neossolos",
                                               "Nitossolos", "Organossolos", "Planossolos", "Plintossolos", "Vertissolos"])
        self.combo_tipo.grid(row=3, column=1, sticky="we", pady=4)

        # ph, p, k
        tk.Label(self.frm, text="PH:").grid(row=4, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_ph = tk.Entry(self.frm, width=20)
        self.entry_ph.grid(row=4, column=1, sticky="w", pady=4)

        tk.Label(self.frm, text="P:").grid(row=5, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_p = tk.Entry(self.frm, width=20)
        self.entry_p.grid(row=5, column=1, sticky="w", pady=4)

        tk.Label(self.frm, text="K:").grid(row=6, column=0, sticky="e", padx=(0, 8), pady=4)
        self.entry_k = tk.Entry(self.frm, width=20)
        self.entry_k.grid(row=6, column=1, sticky="w", pady=4)

        # Botões
        botoes = tk.Frame(self.frm)
        botoes.grid(row=7, column=0, columnspan=2, pady=(6, 10))
        self.__btn_adicionar = tk.Button(botoes, text="Adicionar", command=self.adicionar)
        self.__btn_adicionar.grid(row=0, column=0, padx=4)
        self.__btn_atualizar = tk.Button(botoes, text="Atualizar", command=self.atualizar, state='disabled')
        self.__btn_atualizar.grid(row=0, column=1, padx=4)
        self.__btn_remover = tk.Button(botoes, text="Remover", command=self.remover, state='disabled')
        self.__btn_remover.grid(row=0, column=2, padx=4)
        self.__btn_imprimir = tk.Button(botoes, text="Imprimir", command=self.imprimir, state='disabled')
        self.__btn_imprimir.grid(row=0, column=3, padx=4)
        self.__btn_limpar = tk.Button(botoes, text="Limpar", command=self.__limpar_campos)
        self.__btn_limpar.grid(row=0, column=4, padx=4)

        # Filtro
        filtro_frame = tk.Frame(self.frm)
        filtro_frame.grid(row=8, column=0, columnspan=2, sticky="we", pady=(10, 4))
        tk.Label(filtro_frame, text="Filtrar por Produtor:").pack(side="left")
        filtro_entry = tk.Entry(filtro_frame, textvariable=self.__filtro_produtor, width=30)
        filtro_entry.pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Filtrar", command=self.__atualizar_listbox).pack(side="left", padx=5)
        tk.Button(filtro_frame, text="Limpar", command=self.__limpar_filtro).pack(side="left")

        # Lista
        self.listbox = tk.Listbox(self.frm, width=75, height=10)
        self.listbox.grid(row=9, column=0, columnspan=2, sticky="we")
        self.listbox.bind("<<ListboxSelect>>", self.selecionar)

        self.frm.grid_columnconfigure(1, weight=1)

        # inicializa listbox
        self.__atualizar_listbox()

    def __montar_perfil(self) -> PerfilProdutor | None:
        produtor = self.entry_produtor.get().strip()
        if not produtor:
            messagebox.showerror("Erro", "Informe o nome do produtor.")
            return None

        tipo = self.combo_tipo.get().strip()
        if not tipo:
            messagebox.showerror("Erro", "Selecione o tipo de solo.")
            return None

        fazenda = self.entry_fazenda.get("1.0", "end-1c").strip()
        talhao = self.entry_talhao.get().strip()
        if not talhao:
            messagebox.showerror("Erro", "Informe o talhão.")
            return None

        try:
            ph = float(self.entry_ph.get())
            p = float(self.entry_p.get())
            k = float(self.entry_k.get())
        except ValueError:
            messagebox.showerror("Erro", "PH, P e K devem ser números (use ponto como separador).")
            return None

        return PerfilProdutor(produtor, tipo, fazenda, talhao, ph, p, k)

    def __atualizar_listbox(self):
        texto_filtro = self.__filtro_produtor.get().strip().lower()
        self.listbox.delete(0, tk.END)
        if texto_filtro:
            lista = [c for c in self.listaPerfilProdutor.cadastros if texto_filtro in c.produtor.lower()]
        else:
            lista = self.listaPerfilProdutor.cadastros

        for c in lista:
            self.listbox.insert(tk.END, c.produtor)

    def __limpar_campos(self):
        self.entry_produtor.config(state='normal')
        self.entry_produtor.delete(0, tk.END)
        self.entry_fazenda.delete("1.0", tk.END)
        self.entry_talhao.delete(0, tk.END)
        self.combo_tipo.set("")
        self.entry_ph.delete(0, tk.END)
        self.entry_p.delete(0, tk.END)
        self.entry_k.delete(0, tk.END)
        self.__btn_atualizar.config(state='disabled')
        self.__btn_remover.config(state='disabled')
        self.__btn_imprimir.config(state='disabled')
        self.item_selecionado = None
        self.__btn_adicionar.config(text='Adicionar')

    def __limpar_filtro(self):
        self.__filtro_produtor.set("")
        self.__atualizar_listbox()

    def selecionar(self, event=None):
        sel = self.listbox.curselection()
        if not sel:
            return
        nome = self.listbox.get(sel[0])
        perfil = self.listaPerfilProdutor.buscar_por_produtor(nome)
        if not perfil:
            return

        self.item_selecionado = perfil

        self.entry_produtor.config(state='normal')
        self.entry_produtor.delete(0, tk.END)
        self.entry_produtor.insert(0, perfil.produtor)
        self.entry_produtor.config(state='disabled')

        self.entry_fazenda.delete("1.0", tk.END)
        if isinstance(perfil.fazenda, dict):
            for k, v in perfil.fazenda.items():
                self.entry_fazenda.insert(tk.END, f"{k}: {v}\n")
        else:
            self.entry_fazenda.insert(tk.END, str(perfil.fazenda))

        self.entry_talhao.delete(0, tk.END)
        self.entry_talhao.insert(0, str(perfil.talhao))

        self.combo_tipo.set(perfil.tipo_solos)
        self.entry_ph.delete(0, tk.END)
        self.entry_ph.insert(0, str(perfil.ph))
        self.entry_p.delete(0, tk.END)
        self.entry_p.insert(0, str(perfil.p))
        self.entry_k.delete(0, tk.END)
        self.entry_k.insert(0, str(perfil.k))

        self.__btn_atualizar.config(state='normal')
        self.__btn_imprimir.config(state='normal')
        self.__btn_remover.config(state='normal')
        self.__btn_adicionar.config(text='Novo Registro')

    def adicionar(self):
        if self.__btn_adicionar.cget("text") == 'Novo Registro':
            self.__limpar_campos()
            return

        perfil = self.__montar_perfil()
        if not perfil:
            return

        if self.listaPerfilProdutor.criar(perfil):
            messagebox.showinfo("Sucesso", f"Cadastro '{perfil.produtor}' adicionado.")
            self.__atualizar_listbox()
            self.__limpar_campos()
        else:
            messagebox.showerror("Erro", "Já existe um produtor com este nome ou houve erro ao salvar.")

    def atualizar(self):
        if not self.item_selecionado:
            messagebox.showwarning("Aviso", "Selecione um registro para atualizar.")
            return
        novo = self.__montar_perfil()
        if not novo:
            return
        if self.listaPerfilProdutor.alterar(novo):
            messagebox.showinfo("Sucesso", f"Cadastro '{novo.produtor}' atualizado.")
            self.__atualizar_listbox()
            self.__limpar_campos()
        else:
            messagebox.showerror("Erro", "Falha ao atualizar. Verifique duplicidade.")

    def remover(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro para remover.")
            return
        nome = self.listbox.get(sel[0])
        if messagebox.askyesno("Confirmar", f"Remover cadastro '{nome}'?"):
            if self.listaPerfilProdutor.deletar(nome):
                messagebox.showinfo("Sucesso", "Removido.")
                self.__atualizar_listbox()
                self.__limpar_campos()
            else:
                messagebox.showerror("Erro", "Falha ao remover.")

    def imprimir(self):
        sel = self.listbox.curselection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro para imprimir.")
            return
        nome = self.listbox.get(sel[0])
        perfil = self.listaPerfilProdutor.buscar_por_produtor(nome)
        if not perfil:
            messagebox.showerror("Erro", "Registro não encontrado.")
            return

        caminho = filedialog.asksaveasfilename(
            title="Salvar Cadastro como PDF",
            defaultextension=".pdf",
            filetypes=[("PDF", "*.pdf")],
            initialfile=f"{perfil.produtor}.pdf",
        )
        if not caminho:
            return
        try:
            perfil.imprimir_cadastro(caminho)
            messagebox.showinfo("Sucesso", f"PDF gerado em:\n{caminho}")
        except Exception as e:
            messagebox.showerror("Erro ao imprimir", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = CadastrosView(root)
    root.mainloop()
