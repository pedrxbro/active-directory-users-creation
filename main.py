import tkinter as tk
from tkinter import ttk, messagebox
from ad_manager import create_ad_user_via_powershell as create_ad_user
from config import get_ramais_by_sector

class UserCreationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criação de Usuário - Active Directory")
        self.root.geometry("600x600")

        # Labels e Entradas
        ttk.Label(root, text="Nome Completo:").pack(pady=5)
        self.fullname_entry = ttk.Entry(root, width=60)
        self.fullname_entry.pack(pady=5)

        ttk.Label(root, text="Nome de Usuário (nome.ultimosobrenome):").pack(pady=5)
        self.username_entry = ttk.Entry(root, width=60)
        self.username_entry.pack(pady=5)

        ttk.Label(root, text="Setor:").pack(pady=5)
        # substitui entrada livre por combobox (exemplo: adicionar setores conhecidos)
        self.sector_cb = ttk.Combobox(root, values=["Fiscal", "Contábil", "Departamento Pessoal", "Societário", "Coleta e Entrega", "Informação", "Inovação", "Arquivo", "Comercial"], state="readonly")
        self.sector_cb.pack(pady=5)
        self.sector_cb.bind('<<ComboboxSelected>>', self.on_sector_change)

        ttk.Label(root, text="Cargo:").pack(pady=5)
        self.role_cb = ttk.Combobox(root, values=["Auxiliar", "Assistente", "Analista", "Coordenação"], state="readonly")
        self.role_cb.pack(pady=5)
        self.role_cb.bind('<<ComboboxSelected>>', self.update_email_preview)

        # Ramal: área dinâmica. Sempre mostra opções de ramal
        self.ramal_frame_label = ttk.Label(root, text="Selecione o ramal do setor:")
        self.ramal_frame_label.pack(pady=2)
        self.ramal_frame = ttk.Frame(root)
        self.ramal_frame.pack(pady=5, fill=tk.X)
        self.ramal_var = tk.StringVar(value="")

        # Campo email (ramal)
        ttk.Label(root, text="Ramal: '<Setor> Serviços - Ramal <numero>':").pack(pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(root, width=80, textvariable=self.email_var)
        self.email_entry.pack(pady=5)

        # Botão de criação
        ttk.Button(root, text="Criar Usuário", command=self.create_user).pack(pady=20)

    def on_sector_change(self, event=None):
        sector = self.sector_cb.get()
        # atualizar lista de ramais
        for child in self.ramal_frame.winfo_children():
            child.destroy()
        self.ramal_var.set("")
        self.ramal_frame_label.config(text="Selecione o ramal do setor:")
        ramais = get_ramais_by_sector(sector)
        for r in ramais:
            rb = ttk.Radiobutton(self.ramal_frame, text=r, value=r, variable=self.ramal_var, command=self.update_email_preview)
            rb.pack(side=tk.LEFT, padx=5)
        self.update_email_preview()

    def update_email_preview(self):
        sector = self.sector_cb.get()
        if sector:
            base = f"{sector} Serviços"
        else:
            base = ""
        ramal = self.ramal_var.get()
        if ramal:
            email_preview = f"{base} - Ramal {ramal}"
        else:
            email_preview = base
        self.email_var.set(email_preview)

    def show_details_window(self, title, content):
        win = tk.Toplevel(self.root)
        win.title(title)
        win.geometry("800x500")
        txt = tk.Text(win, wrap=tk.NONE)
        txt.insert("1.0", content)
        txt.config(state=tk.DISABLED)
        txt.pack(fill=tk.BOTH, expand=True)
        ttk.Button(win, text="Fechar", command=win.destroy).pack(pady=5)

    def create_user(self):
        fullname = self.fullname_entry.get()
        username = self.username_entry.get()
        sector = self.sector_cb.get()
        role = self.role_cb.get()

        # Validação simples
        if not fullname or not username or not sector or not role:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        # Sempre exige seleção de ramal
        if not self.ramal_var.get():
            messagebox.showerror("Erro", "Selecione o ramal do setor (obrigatório).")
            return

        # montar email a partir do preview (campo obrigatório)
        email = self.email_var.get().strip()
        if not email:
            messagebox.showerror("Erro", "O campo Email é obrigatório.")
            return

        # Chama a função que usa PowerShell
        result = create_ad_user(fullname, username, sector, role, email)

        # Interpreta resultado
        success = False
        details = ""
        if isinstance(result, dict):
            success = result.get("success", False)
            parts = []
            parts.append(f"Return code: {result.get('returncode')}")
            if result.get('stdout'):
                parts.append("STDOUT:\n" + result.get('stdout'))
            if result.get('stderr'):
                parts.append("STDERR:\n" + result.get('stderr'))
            if result.get('ps_log_tail'):
                parts.append("PS_LOG_TAIL:\n" + result.get('ps_log_tail'))
            if result.get('error'):
                parts.append("ERROR_LOCAL:\n" + result.get('error'))
            details = "\n\n".join(parts)
        elif isinstance(result, bool):
            success = result
        elif result is None:
            success = False
        else:
            success = False
            details = str(result)

        if success:
            if messagebox.askyesno("Sucesso", f"Usuário {username} criado com sucesso!\n\nDeseja ver os detalhes/logs ?"):
                self.show_details_window(f"Detalhes - {username}", details)
        else:
            msg = f"Falha ao criar usuário {username}."
            if messagebox.askyesno("Erro", msg + "\n\nDeseja ver os detalhes/erros ?"):
                self.show_details_window(f"Erros - {username}", details)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserCreationApp(root)
    root.mainloop()
