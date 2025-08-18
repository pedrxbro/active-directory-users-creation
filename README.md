# 🛠️ Criador de Usuários no Active Directory (Python + PowerShell)

Este projeto foi desenvolvido para **automatizar a criação de usuários no Active Directory (AD)**, utilizando:

- **Python (Tkinter)** → Interface gráfica para entrada dos dados.  
- **PowerShell (create_user.ps1)** → Execução da criação do usuário no AD.  
- **Logs detalhados** → Para auditoria e acompanhamento.  

O fluxo principal é:

```
Usuário preenche dados na interface → Python valida e prepara comandos →
Python chama PowerShell → PowerShell cria usuário no AD →
Logs são gerados e retornados à interface
```

---

## 📂 Estrutura do Repositório

```
├── main.py              # Interface gráfica (Tkinter)
├── ad_manager.py        # Ponte entre Python e PowerShell
├── config.py            # Configurações de OUs, grupos e ramais
├── logger.py            # Registro de logs de execução
├── create_user.ps1      # Script PowerShell que cria o usuário no AD
├── README_PyInstaller.md# Instruções para gerar o executável
└── .gitignore           # Arquivos ignorados pelo Git
```

---

## 🚀 Como utilizar

1. **Executar o programa**:
   Após gerar o executável (.exe) com o PyInstaller, é necessário abrir o programa diretamente no servidor de Active Directory (srv-ad01), pois:
   O script PowerShell (create_user.ps1) depende do módulo ActiveDirectory, que só está disponível no servidor.
   A execução exige permissões administrativas no AD.

2. **Preencher os dados na interface gráfica:**
   - Nome completo
   - Nome de usuário (ex.: `nome.sobrenome`)
   - Setor
   - Cargo
   - Selecionar ramal
   - E-mail (obrigatório)

3. Clicar em **“Criar Usuário”**.  
   O sistema validará os dados, chamará o **PowerShell** e exibirá logs/detalhes de sucesso ou erro.

---

## 🖥️ Interface (Tkinter)

Exemplo de construção de campos no `main.py`:

```python
ttk.Label(root, text="Nome Completo:").pack(pady=5)
self.fullname_entry = ttk.Entry(root, width=60)
self.fullname_entry.pack(pady=5)

ttk.Label(root, text="Setor:").pack(pady=5)
self.sector_cb = ttk.Combobox(root, values=["Fiscal", "Contábil"], state="readonly")
self.sector_cb.pack(pady=5)
```

Na criação:

```python
result = create_ad_user(fullname, username, sector, role, email)
if result.get("success"):
    messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
```

---

## ⚙️ Criação do Usuário (Python → PowerShell)

O `ad_manager.py` é responsável por preparar e invocar o PowerShell:

```python
cmd = [
    "powershell.exe", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass",
    "-File", ps1_path,
    "-FullName", fullname,
    "-SamAccountName", username,
    "-OU", ou_dn,
    "-Title", role,
    "-Groups", groups_str,
    "-Email", email
]

result = subprocess.run(cmd, capture_output=True, text=True)
```

Ele também faz logging e coleta os últimos 200 registros do log do PowerShell.

---

## 📜 Script PowerShell (`create_user.ps1`)

Responsável pela criação do usuário no AD:

```powershell
New-ADUser -Name $FullName `
  -SamAccountName $SamAccountName `
  -UserPrincipalName "$SamAccountName@roderjan.com.br" `
  -DisplayName $FullName `
  -Path $OU `
  -AccountPassword $securePwd `
  -Enabled $true `
  -Title $Title
```

Funções adicionais:
- Define **senha padrão** (`qwe123@`)  
- Configura **e-mail**  
- Define que a senha **nunca expira**  
- Adiciona o usuário aos **grupos correspondentes**  
- Registra logs em `C:\Users\adm.operator\Desktop\ad_user_creation_logs\ps_log.txt`  

---

## 🗂️ Configurações (config.py)

Arquivo central de configuração de **OUs, grupos e ramais**.  

Exemplo de OU por setor:

```python
def get_ou_by_sector(sector):
    base_ou = "OU=Setores,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br"
    sector_ou_map = {"Contábil": "Contabil"}
    ou_name = sector_ou_map.get(sector, sector).replace(",", "").strip()
    return f"OU={ou_name},{base_ou}"
```

Exemplo de ramais:

```python
ramais_by_sector = {
    "Fiscal": ["7110", "7113"],
    "Contábil": ["7108", "7105"]
}
```

---

## 📝 Logs

- **Python (logger.py):** grava em `log.txt`  
- **PowerShell:** grava em `ps_log.txt`  

Exemplo em Python:

```python
def log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
```

---

## 🔨 Gerando o Executável (.exe)

### 1. Criar e ativar ambiente virtual (opcional, mas recomendado)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

### 2. Instalar dependências
```powershell
pip install -r requirements.txt
```

### 3. Gerar o executável
```powershell
python -m PyInstaller --onefile --noconsole --noupx --add-data "create_user.ps1:." --name=ad_user_creator --uac-admin main.py
```

### 🔑 Explicação das flags:
- `--onefile` → gera um único `.exe`  
- `--noconsole` → esconde a janela de console  
- `--noupx` → evita compactação UPX (reduz riscos de erro)  
- `--add-data "src;dest"` → inclui arquivos/diretórios adicionais (nesse caso o PowerShell)  
- `--uac-admin` → solicita privilégios administrativos (necessário para criação no AD)  

👉 O executável será gerado na pasta `dist`.

---

## 📌 Observações importantes
- O **campo e-mail é obrigatório** para criação.  
- Caso algum grupo definido em `config.py` não exista, o PowerShell **pula esse grupo** e registra no log.  
- Sempre que houver alterações no código, **gere novamente o `.exe` com PyInstaller**.  
