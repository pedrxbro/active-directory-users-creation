# Módulo de configurações e mapeamento de OUs/grupos

# OU base para colaboradores
def get_ou_by_sector(sector):
    base_ou = "OU=Setores,OU=Roderjan Servicos,OU=Roderjan Group,DC=roderjan,DC=com,DC=br"
    return f"OU={sector},{base_ou}"

# Grupos gerais para todos os colaboradores
general_groups = [
    "S_LIST", "S_LIST_DPTOS", "S_LIST_FORMS", "S_LIST_DECLARACOES", "S_LIST_SOCIETARIO", "S_LIST_DP", "S_LIST_COLETA", "S_LIST_ARQUIVO",
    "BLOQUEIA_CERTIFICADOS", "BLOQUEIA_CONTROLE_CERTIFICADOS", "BLOQUEIA_GERAL_CONT", "BLOQUEIA_HORARIO", "DENY_MSTSC_", "G_U_SPARK",
    "H_LIST", "H_LIST_INFORMATIVO", "Q_RODERJAN"
]

# Grupos por setor/cargo
groups_by_sector = {
    "Fiscal": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST", "EMP_TRANSF", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES", "S_LIST_FISCAL",
            "S_FIS_OPERACIONAL", "S_FIS_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO"
        ]
    },
    # Adicione outros setores/cargos conforme necessário
}

def get_groups(sector, role, general=True, department=True):
    groups = []
    if general:
        groups.extend(general_groups)
    if department:
        sector_groups = groups_by_sector.get(sector, {})
        role_groups = sector_groups.get(role, [])
        groups.extend(role_groups)
    return groups
