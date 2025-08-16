import win32com.client
from config import get_ou_by_sector, get_groups, find_group_dn
from logger import log
import traceback
import subprocess
import os
import shlex
import sys


# Módulo para integração com Active Directory
# Implementação futura: funções para criar usuário, adicionar a grupos, etc.

def split_name(fullname):
    parts = fullname.strip().split()
    if len(parts) > 1:
        given_name = parts[0]
        sn = ' '.join(parts[1:])
    else:
        given_name = fullname
        sn = ''
    return given_name, sn


def tail_file(path, max_lines=200):
    """Retorna as últimas max_lines linhas de um arquivo de log (silenciosamente em caso de erro)."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return ''.join(lines[-max_lines:])
    except Exception as e:
        return f"Could not read log file {path}: {e}"


def create_ad_user(fullname, username, sector, role, general_group, department_group):
    try:
        log(f"[INPUT] Nome Completo: {fullname}")
        log(f"[INPUT] Nome de Usuário: {username}")
        log(f"[INPUT] Setor: {sector}")
        log(f"[INPUT] Cargo: {role}")
        log(f"[INPUT] Grupos Gerais: {general_group}")
        log(f"[INPUT] Grupos Departamento: {department_group}")

        ldap_dn = get_ou_by_sector(sector)
        ldap_path = f"LDAP://{ldap_dn}"
        log(f"[LDAP] OU destino: {ldap_path}")

        try:
            ad = win32com.client.Dispatch("ADsNameSpaces")
            domain = ad.GetObject("","LDAP:")
            ou = domain.OpenDSObject(ldap_path, None, None, 0)
            log(f"[AD] Conexão com OU realizada.")
        except Exception as e:
            log(f"[ERRO] Falha ao conectar/abrir OU: {e}")
            log(traceback.format_exc())
            return False

        # Extrair primeiro nome e sobrenome
        given_name, sn = split_name(fullname)
        log(f"[AD] givenName: {given_name}")
        log(f"[AD] sn: {sn}")

        # Criação do usuário
        try:
            user = ou.Create("user", f"CN={fullname}")
            log(f"[AD] Usuário criado: CN={fullname}")

            # Atribuir atributos básicos
            user.Put("sAMAccountName", username)
            user.Put("displayName", fullname)
            user.Put("userPrincipalName", f"{username}@roderjan.com.br")
            user.Put("description", role)
            user.Put("givenName", given_name)
            user.Put("sn", sn)

            # Definir userAccountControl inicialmente como Conta Normal (512)
            try:
                UF_NORMAL_ACCOUNT = 0x200  # 512
                user.Put("userAccountControl", UF_NORMAL_ACCOUNT)
                log(f"[AD] userAccountControl inicial (NORMAL_ACCOUNT) setado: {UF_NORMAL_ACCOUNT}")
            except Exception as e:
                log(f"[ERRO] Ao setar userAccountControl inicial: {e}")
                log(traceback.format_exc())

            # Persistir atributos iniciais
            user.SetInfo()
            log(f"[AD] Atributos iniciais gravados com SetInfo().")
        except Exception as e:
            log(f"[ERRO] Ao criar usuário ou definir atributos: {e}")
            log(traceback.format_exc())
            return False

        # Definir senha padrão (deve ser chamado após SetInfo em alguns ambientes)
        try:
            user.SetPassword("qwe123@")
            log(f"[AD] Senha padrão definida.")
        except Exception as e:
            log(f"[ERRO] Ao definir senha: {e}")
            log(traceback.format_exc())
            return False

        # Ajustar userAccountControl para incluir 'Password never expires' se desejado
        try:
            ADS_UF_DONT_EXPIRE_PASSWD = 0x10000  # 65536
            UF_NORMAL_ACCOUNT = 0x200  # 512
            combined = UF_NORMAL_ACCOUNT | ADS_UF_DONT_EXPIRE_PASSWD
            user.Put("userAccountControl", combined)
            user.SetInfo()
            log(f"[AD] userAccountControl atualizado: {combined} (NORMAL + DONT_EXPIRE)")
        except Exception as e:
            log(f"[ERRO] Ao definir flag de expiração de senha: {e}")
            log(traceback.format_exc())
            return False

        # Adicionar aos grupos
        groups = get_groups(sector, role, general_group, department_group)
        for group_name in groups:
            try:
                group_dn = find_group_dn(group_name)
                log(f"[GRUPO] Tentando adicionar ao grupo: {group_name} | DN: {group_dn}")
                if group_dn:
                    group_path = f"LDAP://{group_dn}"
                    try:
                        group = domain.OpenDSObject(group_path, None, None, 0)
                        group.Add(user.ADsPath)
                        log(f"[AD] Usuário adicionado ao grupo: {group_name}")
                    except Exception as e:
                        log(f"[ERRO] Ao adicionar ao grupo {group_name}: {e}")
                        log(traceback.format_exc())
                else:
                    log(f"[ERRO] Grupo {group_name} não encontrado nas OUs conhecidas.")
            except Exception as e:
                log(f"[ERRO] Erro ao processar grupo {group_name}: {e}")
                log(traceback.format_exc())

        log(f"[SUCESSO] Usuário {username} criado com sucesso!")
        return True
    except Exception as e:
        log(f"[ERRO] Erro geral na criação do usuário {username}: {e}")
        log(traceback.format_exc())
        return False


def create_ad_user_via_powershell(fullname, username, sector, role, email):
    """
    Invoca o script PowerShell `create_user.ps1` (no mesmo diretório deste arquivo) para criar o usuário no AD.
    Suporta execução quando empacotado com PyInstaller (--onefile).
    O parâmetro email agora é obrigatório.
    """
    try:
        if not email:
            msg = "Email parameter is required"
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}

        log(f"[PS_CALL] Iniciando criação via PowerShell: {username}")
        # Suporta PyInstaller onefile: arquivos adicionados com --add-data serão extraídos em _MEIPASS
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        ps1_path = os.path.join(base_dir, "create_user.ps1")
        if not os.path.isfile(ps1_path):
            msg = f"create_user.ps1 não encontrado em {ps1_path}"
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}

        ou_dn = get_ou_by_sector(sector)
        groups = get_groups(sector, role, True, True)
        groups_str = ','.join(groups)

        cmd = [
            "powershell.exe",
            "-NoProfile",
            "-NonInteractive",
            "-ExecutionPolicy", "Bypass",
            "-File", ps1_path,
            "-FullName", fullname,
            "-SamAccountName", username,
            "-OU", ou_dn,
            "-Title", role,
            "-Groups", groups_str
        ]

        cmd.extend(["-Email", email])

        # Registrar o comando (com escape) para diagnóstico
        try:
            cmd_str = ' '.join(shlex.quote(p) for p in cmd)
        except Exception:
            cmd_str = str(cmd)
        log(f"[PS_CALL] Command: {cmd_str}")

        # Executa o PowerShell
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError as e:
            msg = f"powershell.exe not found: {e}"
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}
        except Exception as e:
            log(f"[ERRO] Falha ao executar PowerShell: {e}")
            log(traceback.format_exc())
            return {"success": False, "error": str(e)}

        log(f"[PS_CALL] returncode={result.returncode}")
        if result.stdout:
            log(f"[PS_CALL][STDOUT] {result.stdout.strip()}")
        if result.stderr:
            log(f"[PS_CALL][STDERR] {result.stderr.strip()}")

        # Tentar anexar o log do PowerShell (criado pelo script)
        ps_log_path = r"C:\Users\adm.operator\Desktop\ad_user_creation_logs\ps_log.txt"
        ps_log_tail = None
        if os.path.isfile(ps_log_path):
            ps_log_tail = tail_file(ps_log_path, max_lines=200)

        success = (result.returncode == 0) or ("SUCCESS" in (result.stdout or ""))
        return {
            "success": success,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "ps_log_tail": ps_log_tail
        }

    except Exception as e:
        log(f"[ERRO][PS_CALL] {e}")
        log(traceback.format_exc())
        return {"success": False, "error": str(e)}
