import win32com.client
from config import get_ou_by_sector, get_groups

# Módulo para integração com Active Directory
# Implementação futura: funções para criar usuário, adicionar a grupos, etc.

def create_ad_user(fullname, username, sector, role, general_group, department_group):
    try:
        # Conexão com o AD
        ldap_path = f"LDAP://{get_ou_by_sector(sector)}"
        ad = win32com.client.Dispatch("ADsNameSpaces")
        domain = ad.GetObject("","LDAP:")
        ou = domain.OpenDSObject(ldap_path, None, None, 0)

        # Criação do usuário
        user = ou.Create("user", f"CN={fullname}")
        user.Put("sAMAccountName", username)
        user.Put("displayName", fullname)
        user.Put("userPrincipalName", f"{username}@roderjan.com.br")
        user.Put("description", role)
        user.SetInfo()

        # Definir senha padrão
        user.SetPassword("qwe123@")
        # Password never expires
        ADS_UF_DONT_EXPIRE_PASSWD = 0x10000
        user.Put("userAccountControl", ADS_UF_DONT_EXPIRE_PASSWD)
        user.SetInfo()

        # Adicionar aos grupos
        groups = get_groups(sector, role, general_group, department_group)
        for group_name in groups:
            group_path = f"LDAP://CN={group_name},CN=Users,DC=roderjan,DC=com,DC=br"
            try:
                group = domain.OpenDSObject(group_path, None, None, 0)
                group.Add(user.ADsPath)
            except Exception as e:
                print(f"Erro ao adicionar ao grupo {group_name}: {e}")

        return True
    except Exception as e:
        print(f"Erro na criação do usuário: {e}")
        return False
