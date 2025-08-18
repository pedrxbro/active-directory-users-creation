# Módulo de configurações e mapeamento de OUs/grupos

# OU base para colaboradores
def get_ou_by_sector(sector):
    base_ou = "OU=Setores,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br"
    # Mapear nomes exibidos para o nome real da OU quando houver diferença (ex.: acentos)
    sector_ou_map = {
        "Contábil": "Contabil",
        "Contabil": "Contabil",
    }
    ou_name = sector_ou_map.get(sector, sector)
    # Sanitização básica: remover vírgulas e espaços extras
    ou_name = str(ou_name).replace(",", "").strip()
    return f"OU={ou_name},{base_ou}"

# Grupos gerais para todos os colaboradores
general_groups = [
    "S_LIST", "S_LIST_DPTOS", "S_LIST_FORMS", "S_LIST_DECLARACOES", "S_LIST_SOCIETARIO", "S_LIST_DP", "S_LIST_COLETA", "S_LIST_ARQUIVO",
    "BLOQUEIA_CERTIFICADOS", "BLOQUEIA_CONTROLE_CERTIFICADO", "BLOQUEIA_GERAL_CONT", "BLOQUEIA_HORARIO", "DENY_MSTSC", "G_U_SPARK",
    "H_LIST", "H_LIST_INFORMATIVO", "Q_RODERJAN"
]

# Grupos por setor/cargo
groups_by_sector = {
    "Fiscal": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES", "S_LIST_FISCAL",
            "S_FIS_OPERACIONAL", "S_FIS_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Fiscal"
        ]
    },
    "Contábil": {
        "Auxiliar": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES",
            "S_LIST_FISCAL", "S_LIST_CONTABIL", "S_CTB_OPERACIONAL", "S_CTB_CONSULTA_EXT", "S_OPE_VISAO", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Contabil"
        ],
        "Assistente": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES",
            "S_LIST_FISCAL", "S_LIST_CONTABIL", "S_CTB_OPERACIONAL", "S_CTB_CONSULTA_EXT", "S_OPE_VISAO", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Contabil"
        ],
        "Analista": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES",
            "S_LIST_FISCAL", "S_LIST_CONTABIL", "S_CTB_ANALISTA", "S_CTB_CONSULTA_EXT", "S_OPE_VISAO", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Contabil"
        ],
        "Supervisor": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES", 
            "S_LIST_FISCAL", "S_LIST_CONTABIL", "S_CTB_SUPERVISAO", "S_CTB_CONSULTA_EXT", "S_OPE_VISAO", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Contabil"
        ]
    },
    # Adicione outros setores/cargos conforme necessário
}

def get_groups(sector, role):
    groups = []
    groups.extend(general_groups)
    sector_groups = groups_by_sector.get(sector, {})
    role_groups = sector_groups.get(role, [])
    groups.extend(role_groups)
    return groups

group_ou_paths = [
    "OU=Grupos Dptos,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=Grupos List Dptos,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=Grupos List Servicos,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=Grupos Coord Servicos,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=Grupos List Holding,OU=Roderjan Holding,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=WebApp Group,OU=Roderjan Holding,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=OpenfireChat,OU=Roderjan Group,DC=roderjan,DC=com,DC=br",
    "OU=Grupos,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br"
]


# Ramais por setor (números de ramal como strings)
ramais_by_sector = {
    "Fiscal": ["7110", "7113"],
    "Contábil": ["7108", "7105"],
    "Contabil": ["7108", "7105"],
    # Adicione outros setores e seus ramais conforme necessário
}

def get_ramais_by_sector(sector):
    return ramais_by_sector.get(sector, [])
