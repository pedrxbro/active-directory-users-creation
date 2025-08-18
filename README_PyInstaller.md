Instruções para gerar o executável (.exe) usando PyInstaller

1. (Opcional, mas recomendado) Crie e ative um ambiente virtual (venv):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate
```

2. Instale as dependências do projeto:

```powershell
pip install -r requirements.txt
```

3. Gere o executável com o comando abaixo (ajuste caminhos se necessário):

```powershell
python -m PyInstaller --onefile --noconsole --noupx --add-data "create_user.ps1:." --name=ad_user_creator --uac-admin main.py
```

Explicações:
- --onefile: gera um único .exe
- --noconsole: esconde a janela de console
- --add-data "src;dest": inclui arquivos/diretórios adicionais no executável

O executável será gerado na pasta `dist`.