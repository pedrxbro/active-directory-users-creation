import tkinter as tk
from tkinter import ttk, messagebox
from ad_manager import create_ad_user
from config import get_ou_by_sector, get_groups

class UserCreationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Criação de Usuário - Active Directory")
        self.root.geometry("400x400")

        # Labels e Entradas
        ttk.Label(root, text="Nome Completo:").pack(pady=5)
        self.fullname_entry = ttk.Entry(root, width=40)
        self.fullname_entry.pack(pady=5)

        ttk.Label(root, text="Nome de Usuário (nome.ultimosobrenome):").pack(pady=5)
        self.username_entry = ttk.Entry(root, width=40)
        self.username_entry.pack(pady=5)

        ttk.Label(root, text="Setor:").pack(pady=5)
        self.sector_entry = ttk.Entry(root, width=40)
        self.sector_entry.pack(pady=5)

        ttk.Label(root, text="Cargo:").pack(pady=5)
        self.role_entry = ttk.Entry(root, width=40)
        self.role_entry.pack(pady=5)

        # Flags para grupos
        self.general_group_var = tk.BooleanVar()
        self.department_group_var = tk.BooleanVar()
        ttk.Checkbutton(root, text="Adicionar aos grupos gerais", variable=self.general_group_var).pack(pady=5)
        ttk.Checkbutton(root, text="Adicionar aos grupos por departamento", variable=self.department_group_var).pack(pady=5)

        # Botão de criação
        ttk.Button(root, text="Criar Usuário", command=self.create_user).pack(pady=20)

    def create_user(self):
        fullname = self.fullname_entry.get()
        username = self.username_entry.get()
        sector = self.sector_entry.get()
        role = self.role_entry.get()
        general_group = self.general_group_var.get()
        department_group = self.department_group_var.get()

        # Validação simples
        if not fullname or not username or not sector or not role:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        ou = get_ou_by_sector(sector)
        groups = get_groups(sector, role, general_group, department_group)
        success = create_ad_user(fullname, username, sector, role, general_group, department_group)

        if success:
            messagebox.showinfo("Sucesso", f"Usuário {username} criado com sucesso!")
        else:
            messagebox.showerror("Erro", f"Falha ao criar usuário {username}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = UserCreationApp(root)
    root.mainloop()
