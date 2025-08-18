Param(
    [Parameter(Mandatory=$true)][string]$FullName,
    [Parameter(Mandatory=$true)][string]$SamAccountName,
    [Parameter(Mandatory=$true)][string]$OU,
    [Parameter(Mandatory=$false)][string]$Title = "",
    [Parameter(Mandatory=$false)][string]$Groups = "",
    [Parameter(Mandatory=$true)][string]$Email
)

# Caminho para o LOG (Alterar caso mude de usuário)
$logPath = 'C:\Users\adm.operator\Desktop\ad_user_creation_logs\ps_log.txt'
function Write-Log([string]$msg){
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') $msg"
    Add-Content -Path $logPath -Value $line
}

Write-Log "Iniciando create_user.ps1 para $SamAccountName"

try {
    Import-Module ActiveDirectory -ErrorAction Stop
} catch {
    Write-Log "ERRO: Falha ao importar o módulo ActiveDirectory: $_"
    Write-Output "ERRO: Falha ao importar o módulo ActiveDirectory: $_"
    exit 2
}

# Divisão do nome já está aqui, mantida em português
$parts = $FullName.Trim() -split '\s+',2
$givenName = $parts[0]
$surname = if ($parts.Length -gt 1) { $parts[1] } else { "" }
Write-Log "Primeiro nome=$givenName; Sobrenome=$surname"

# Senha Padrão
$plainPwd = 'qwe123@'
$securePwd = ConvertTo-SecureString $plainPwd -AsPlainText -Force

try {
    Write-Log "Criando usuário $SamAccountName na OU $OU"
    New-ADUser -Name $FullName `
      -SamAccountName $SamAccountName `
      -UserPrincipalName "$SamAccountName@roderjan.com.br" `
      -DisplayName $FullName `
      -GivenName $givenName `
      -Surname $surname `
      -Path $OU `
      -AccountPassword $securePwd `
      -Enabled $true `
      -Title $Title -ErrorAction Stop

    Write-Log "Novo usuário do AD criado: $SamAccountName"

    # Email obrigatório
    try {
        Set-ADUser -Identity $SamAccountName -EmailAddress $Email -ErrorAction Stop
        Write-Log "Email adicionado: $($SamAccountName): $($Email)"
    } catch {
        Write-Log "AVISO: Não foi possível definir o campo email: $($_)"
    }

    # Senha nunca expira.
    try {
        Set-ADUser -Identity $SamAccountName -PasswordNeverExpires $true -ErrorAction Stop
        Write-Log "Senha nunca expira configurada para $SamAccountName"
    } catch {
        Write-Log "AVISO: Não foi possível definir PasswordNeverExpires: $_"
    }

    # Processa os grupos
    if ($Groups -ne "") {
        $groupList = $Groups -split ',' | ForEach-Object { $_.Trim() } | Where-Object { $_ -ne '' }
        foreach ($g in $groupList) {
            try {
                $grp = Get-ADGroup -Filter { Name -eq $g } -ErrorAction SilentlyContinue
                if ($grp) {
                    Add-ADGroupMember -Identity $grp -Members $SamAccountName -ErrorAction Stop
                    Write-Log "Adicionado $SamAccountName ao grupo $g"
                } else {
                    Write-Log "Grupo não encontrado: $g"
                }
            } catch {
                Write-Log "ERRO ao adicionar ao grupo $($g): $($_)"
            }
        }
    }

    Write-Log "SUCESSO: $SamAccountName criado"
    Write-Output "SUCESSO"
    exit 0
} catch {
    Write-Log "ERRO ao criar usuário $($SamAccountName): $($_)"
    Write-Output "ERRO: $_"
    exit 1
}
