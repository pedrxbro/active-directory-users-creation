Instruções para gerar o .exe usando PyInstaller

Pré-requisitos:
- Windows (no servidor alvo normalmente já disponível)
- Python 3.8+ (somente para construir o .exe)
- Instalar dependências: pip install -r requirements.txt

Comandos recomendados (Powershell):

# Instalar dependências no ambiente de build
pip install -r requirements.txt

# Empacotar em um único executável (--onefile). Incluir o script PowerShell e o diretório de logs se desejar.
# Observação: quando usar --onefile, arquivos listados em --add-data serão extraídos em tempo de execução para _MEIPASS.
pyinstaller --onefile --noconsole \
  --add-data "create_user.ps1;." \
  --add-data "C:\Users\adm.operator\Desktop\ad_user_creation_logs;C:\Users\adm.operator\Desktop\ad_user_creation_logs" \
  main.py

Explicações:
- --onefile: gera um único .exe
- --noconsole: esconde a janela de console (útil para apps GUI)
- --add-data "src;dest": inclui arquivos/diretórios adicionais. No Windows, separe com ponto-e-vírgula.

Considerações de implantação:
- O servidor de destino deve ter o módulo ActiveDirectory disponível no PowerShell (RSAT/Active Directory module).
- A conta que executar o .exe deve ter permissões para criar usuários e adicionar a grupos no AD.
- Política de execução do PowerShell: o exe chama powershell.exe -ExecutionPolicy Bypass -File ... para evitar bloqueios.
- Teste em ambiente seguro antes de produção.

Assinatura digital do executável (recomendado) para evitar bloqueios por antivírus.
