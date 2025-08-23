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
general_groups_coordinator = [
    "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_OPE_FORMS", "S_OPE_DECLARACOES", "S_LIST_ATENDIMENTO","S_LIST_FISCAL",
    "S_LIST_FISCAL", "S_LIST_CONTABIL","S_LIST_INFORMACAO", "S_LIST_INOVACAO", "S_LIST_COMERCIAL", "S_READ_COORDENADORES", "S_OPE_COORDENADORES", 
]

# Grupos por setor/cargo
groups_by_sector = {
    "Fiscal": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_FORMS", "S_READ_DECLARACOES", "S_LIST_FISCAL",
            "S_FIS_OPERACIONAL", "S_FIS_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Fiscal"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_FIS_COORDENACAO", "S_FIS_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Fiscal"
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
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_CTB_COORDENACAO", "S_CTB_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "S_OPE_VISAO", "Dep_Contabil"
        ]
    },
    "Departamento Pessoal": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_OPE_MONITORADA","S_READ_EMP_TRANSF", "S_READ_FORMS", "S_READ_DECLARACOES", "S_LIST_FISCAL",
            "S_DP_OPERACIONAL", "S_DP_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Dessoal"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_EMP_TRANSF","S_DP_COORDENACAO", "S_DP_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Pessoal"
        ]
    },
    "Atendimento": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_FORMS","S_READ_DECLARACOES", "S_LIST_ATENDIMENTO", "S_LIST_FISCAL",
            "S_LIST_CONTABIL", "S_ATD_OPERACIONAL","S_ATD_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Atendimento"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_EMP_TRANSF","S_ATD_COORDENACAO", "S_ATD_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Atendimento"
        ]
    },
    "Comercial": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS","S_READ_EMPRESAS", "S_READ_EMP_TRANSF", "S_READ_FORMS","S_READ_DECLARACOES", "S_LIST_COMERCIAL",
            "S_COM_OPERACIONAL", "S_COM_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Comercial"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_EMPRESAS", "S_READ_EMP_TRANSF","S_COM_COORDENACAO", "S_COM_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Atendimento"
        ]
    },
    "Societário": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_READ_EMPRESAS","S_READ_EMP_TRANSF", "S_READ_FORMS","S_READ_DECLARACOES", "S_OPE_EMPRESAS", "S_GESTAO_EMPRESAS", "S_OPE_EMPRESAS_TRANSF",
            "S_LIST_FISCAL", "S_SOC_OPERACIONAL", "S_SOC_CONSULTA_EXT", "Dep_Societario"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_EMPRESAS", "S_READ_EMP_TRANSF", "S_OPE_EMPRESAS", "S_GESTAO_EMPRESAS","S_OPE_EMPRESAS_TRANSF", "S_SOC_COORDENACAO", "S_SOC_CONSULTA_EXT", "Dep_Societario"
        ]
    },
    
    "Coleta": {
        "Operacional": general_groups + [
            "S_READ_EMPRESAS", "S_READ_EMP_TRANSF","S_READ_FORMS", "S_READ_DECLARACOES","S_LIST_FISCAL", "S_LIST_COLETA", "S_CE_OPERACIONAL", "S_CE_CONSULTA_EXT", "Dep_Boys"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_READ_EMPRESAS", "S_READ_EMP_TRANSF", "S_CE_COORDENACAO","S_CE_CONSULTA_EXT","S_BLOCK_EMPRESAS_GRUPO", "Dep_Boys"
        ]
    },
    "Informação": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_OPE_MONITORADA", "S_READ_EMPRESAS", "S_READ_FORMS","S_READ_DECLARACOES","S_OPE_EMPRESAS_TRANSF", "S_OPE_DECLARACOES", "S_LIST_FISCAL", 
            "S_LIST_INFORMACAO", "S_SOC_CONTROLE_ICP", "S_SOC_CONSULTA_ICP", "S_INF_OPERACIONAL", "S_INF_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Informacao"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_LIST_EMPRESAS_TRANSFERIDAS","S_READ_EMPRESAS", "S_OPE_EMPRESAS_TRANSF", "S_SOC_CONTROLE_ICP", "S_SOC_CONSULTA_ICP", "S_INF_COORDENACAO","S_INF_CONSULTA_EXT","S_BLOCK_EMPRESAS_GRUPO", "Dep_Informacao"
        ]
    },
    "Inovação": {
        "Operacional": general_groups + [
            "S_OPE_MONITORADA", "S_READ_EMPRESAS", "S_READ_EMP_TRANSF", "S_READ_FORMS", "S_READ_DECLARACOES", "S_OPE_EMPRESAS", "S_GESTAO_EMPRESAS", "S_OPE_EMPRESAS_TRANSF",
            "S_OPE_DECLARACOES", "S_LIST_ATENDIMENTO", "S_LIST_FISCAL", "S_LIST_INFORMACAO", "S_LIST_INOVACAO", "S_LIST_COMERCIAL", "S_INV_OPERACIONAL", "S_OPE_VISAO", "Dep_Inovação"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_READ_EMPRESAS","S_READ_EMP_TRANSF","S_OPE_EMPRESAS","S_GESTAO_EMPRESAS","S_OPE_EMPRESAS_TRANSF","S_OPE_EMPRESAS_TRANSF", "S_INV_COORDENACAO","S_INV_CONSULTA_EXT","S_BLOCK_EMPRESAS_GRUPO", "S_OPE_VISAO", "Dep_Inovação"
        ]
    },
    "Arquivo": {
        "Operacional": general_groups + [
            "S_LIST_EMPRESAS", "S_LIST_EMPRESAS_TRANSFERIDAS", "S_READ_FORMS", "S_READ_DECLARACOES", "S_ARQ_OPERACIONAL", "S_ARQ_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Arquivo"
        ],
        "Coordenador": general_groups + general_groups_coordinator + [
            "S_READ_EMPRESAS","S_READ_EMP_TRANSF", "S_ARQ_COORDENACAO", "S_ARQ_CONSULTA_EXT", "S_BLOCK_EMPRESAS_GRUPO", "Dep_Arquivo"
        ]
    }
}

def get_groups(sector, role):
    # Para o setor Fiscal, todos os cargos são tratados como 'Auxiliar'
    if sector != "Contábil" and role in ["Analista", "Assistente", "Auxiliar"]:
        role = "Operacional"
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


# Ramais por setor
ramais_by_sector = {
    "Fiscal": ["7110", "7113"],
    "Contábil": ["7108", "7105"],
    "Contabil": ["7108", "7105"],
    "Departamento Pessoal": ["7106", "7109", "7743", "7745"],
    "Arquivo": ["7112"],
    "Coleta e Entrega": ["7112"],
    "Informação": ["7112"],
    "Atendimento": ["7725", "7723", "7724"],
    "Inovação": ["7111"],
    "Societário": ["7736", "7735"],
}

def get_ramais_by_sector(sector):
    return ramais_by_sector.get(sector, [])
