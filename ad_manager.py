from config import get_ou_by_sector, get_groups
from logger import log
import traceback
import subprocess
import os
import shlex
import sys


# Módulo para integração com Active Directory

def tail_file(path, max_lines=200):
    """Retorna as últimas max_lines linhas de um arquivo de log (silenciosamente em caso de erro)."""
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            return ''.join(lines[-max_lines:])
    except Exception as e:
        return f"Não foi possível ler o arquivo de log {path}: {e}"


def create_ad_user(fullname, username, sector, role, email=None):
    """
    Wrapper para manter compatibilidade: redireciona para create_ad_user_via_powershell.
    """
    if email is None:
        raise ValueError("O parâmetro 'email' é obrigatório para criação de usuário via PowerShell.")
    return create_ad_user_via_powershell(fullname, username, sector, role, email)


def create_ad_user_via_powershell(fullname, username, sector, role, email):
    """
    Invoca o script PowerShell `create_user.ps1` (no mesmo diretório deste arquivo) para criar o usuário no AD.
    Suporta execução quando empacotado com PyInstaller (--onefile).
    O parâmetro email agora é obrigatório.
    """
    try:
        if not email:
            msg = "O parâmetro 'email' é obrigatório."
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}

        log(f"[PS_CALL] Iniciando criação via PowerShell para o usuário: {username}")
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
        ps1_path = os.path.join(base_dir, "create_user.ps1")
        if not os.path.isfile(ps1_path):
            msg = f"Arquivo create_user.ps1 não encontrado em {ps1_path}"
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}

        ou_dn = get_ou_by_sector(sector)
        groups = get_groups(sector, role)
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

        try:
            cmd_str = ' '.join(shlex.quote(p) for p in cmd)
        except Exception:
            cmd_str = str(cmd)
        log(f"[PS_CALL] Comando: {cmd_str}")

        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
        except FileNotFoundError as e:
            msg = f"powershell.exe não encontrado: {e}"
            log(f"[ERRO] {msg}")
            return {"success": False, "error": msg}
        except Exception as e:
            log(f"[ERRO] Falha ao executar o PowerShell: {e}")
            log(traceback.format_exc())
            return {"success": False, "error": str(e)}

        log(f"[PS_CALL] Código de retorno={result.returncode}")
        if result.stdout:
            log(f"[PS_CALL][STDOUT] {result.stdout.strip()}")
        if result.stderr:
            log(f"[PS_CALL][STDERR] {result.stderr.strip()}")

        ps_log_path = r"C:\Users\adm.operator\Desktop\ad_user_creation_logs\ps_log.txt"
        ps_log_tail = None
        if os.path.isfile(ps_log_path):
            ps_log_tail = tail_file(ps_log_path, max_lines=200)

        sucesso = (result.returncode == 0) or ("SUCESSO" in (result.stdout or ""))
        return {
            "success": sucesso,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "ps_log_tail": ps_log_tail
        }

    except Exception as e:
        log(f"[ERRO][PS_CALL] {e}")
        log(traceback.format_exc())
        return {"success": False, "error": str(e)}
