param(
    [string]$ProjectPath = (Resolve-Path "$PSScriptRoot\.." | Select-Object -ExpandProperty Path),
    [string]$Environment = 'production',
    [string]$ErpService = 'erp',
    [string]$PostgresService = 'Postgres',
    [string]$LocalDbContainer = 'mohi_db',
    [string]$LocalDbName = 'mohi_erp',
    [string]$LocalDbUser = 'mohi_admin',
    [switch]$SkipDb,
    [switch]$SkipDeploy,
    [switch]$DataOnly,
    [switch]$NoWipeRemote,
    [switch]$Detach
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Require-Command {
    param([Parameter(Mandatory=$true)][string]$Name)
    if (-not (Get-Command $Name -ErrorAction SilentlyContinue)) {
        throw "Required command not found: $Name"
    }
}

function Exec {
    param(
        [Parameter(Mandatory=$true)][string]$Cmd,
        [switch]$Sensitive
    )
    if (-not $Sensitive) {
        Write-Host "==> $Cmd" -ForegroundColor Cyan
    } else {
        Write-Host "==> (sensitive command hidden)" -ForegroundColor Cyan
    }
    Invoke-Expression $Cmd
}

function Get-RailwayVarsJson {
    param(
        [Parameter(Mandatory=$true)][string]$Service
    )

    $raw = Exec "npx railway variables --service \"$Service\" --environment \"$Environment\" --json" | Out-String
    if (-not $raw.Trim()) {
        throw "No variables returned from Railway for service '$Service'."
    }
    return ($raw | ConvertFrom-Json)
}

function Get-VarValue {
    param(
        [Parameter(Mandatory=$true)]$VarsJson,
        [Parameter(Mandatory=$true)][string]$Name
    )

    # Railway JSON shape may be either an array of {name,value} or an object.
    if ($VarsJson -is [System.Collections.IEnumerable] -and -not ($VarsJson -is [string])) {
        $match = $VarsJson | Where-Object { $_.name -eq $Name } | Select-Object -First 1
        return $match.value
    }
    if ($VarsJson.PSObject.Properties.Name -contains $Name) {
        return $VarsJson.$Name
    }
    return $null
}

function Parse-PostgresUrl {
    param([Parameter(Mandatory=$true)][string]$Url)
    $uri = [Uri]$Url
    $userInfo = $uri.UserInfo
    if (-not $userInfo -or ($userInfo -notmatch ':')) {
        throw "DATABASE_PUBLIC_URL missing user:password: $Url"
    }
    $user = $userInfo.Split(':', 2)[0]
    $pass = $userInfo.Split(':', 2)[1]
    $db = $uri.AbsolutePath.Trim('/')
    return [pscustomobject]@{
        Host = $uri.Host
        Port = $uri.Port
        User = $user
        Password = $pass
        Database = $db
    }
}

Require-Command docker
Require-Command npx

Push-Location $ProjectPath
try {
    Exec "npx railway status" | Out-Null

    if (-not $SkipDb) {
        Write-Host "==> Preparing database dump from local Docker Postgres ($LocalDbContainer)" -ForegroundColor Green

        if ($DataOnly -and -not $NoWipeRemote) {
            throw "-DataOnly requires -NoWipeRemote (data-only restore needs existing schema)."
        }

        $timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
        $dumpLocalPath = Join-Path $ProjectPath "mohi_erp_backup_$timestamp.dump"
        $dumpRemotePath = "/tmp/mohi_erp_backup_$timestamp.dump"

        if (-not (docker ps --format '{{.Names}}' | Select-String -SimpleMatch $LocalDbContainer)) {
            throw "Local DB container not running: $LocalDbContainer"
        }

        $dumpFlags = "-F c"
        if ($DataOnly) {
            $dumpFlags = "$dumpFlags --data-only"
        }

        # Create dump inside container (binary safe), then copy to host.
        Exec "docker exec $LocalDbContainer pg_dump -U $LocalDbUser -d $LocalDbName $dumpFlags -f $dumpRemotePath" | Out-Null
        Exec "docker cp ${LocalDbContainer}:$dumpRemotePath \"$dumpLocalPath\"" | Out-Null

        Write-Host "==> Fetching Railway Postgres public URL" -ForegroundColor Green
        $pgVars = Get-RailwayVarsJson -Service $PostgresService
        $publicUrl = Get-VarValue -VarsJson $pgVars -Name 'DATABASE_PUBLIC_URL'
        if (-not $publicUrl) {
            $publicUrl = Get-VarValue -VarsJson $pgVars -Name 'DATABASE_URL'
        }
        if (-not $publicUrl) {
            throw "Could not find DATABASE_PUBLIC_URL (or DATABASE_URL) in Railway variables for '$PostgresService'."
        }

        $pg = Parse-PostgresUrl -Url $publicUrl

        if (-not $NoWipeRemote) {
            Write-Host "==> Wiping remote schema (public) before restore" -ForegroundColor Yellow
            $wipeSql = "DROP SCHEMA IF EXISTS public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
            Exec "docker exec -e PGPASSWORD=\"$($pg.Password)\" $LocalDbContainer psql -h $($pg.Host) -p $($pg.Port) -U $($pg.User) -d $($pg.Database) -v ON_ERROR_STOP=1 -c \"$wipeSql\"" -Sensitive | Out-Null
        }

        Write-Host "==> Restoring into Railway Postgres ($($pg.Host):$($pg.Port)/$($pg.Database))" -ForegroundColor Green
        $restoreArgs = "--no-owner --no-acl"
        if (-not $DataOnly) {
            $restoreArgs = "$restoreArgs --clean --if-exists"
        }
        Exec "docker exec -e PGPASSWORD=\"$($pg.Password)\" $LocalDbContainer pg_restore -h $($pg.Host) -p $($pg.Port) -U $($pg.User) -d $($pg.Database) $restoreArgs $dumpRemotePath" -Sensitive | Out-Null

        Write-Host "==> Remote DB restore complete" -ForegroundColor Green
    }

    if (-not $SkipDeploy) {
        Write-Host "==> Deploying code to Railway service '$ErpService' ($Environment)" -ForegroundColor Green
        $detachFlag = ''
        if ($Detach) {
            $detachFlag = '--detach'
        }
        Exec "npx railway up $detachFlag --service \"$ErpService\" --environment \"$Environment\"" | Out-Null
        Write-Host "==> Deploy complete" -ForegroundColor Green
    }

    Write-Host "==> Smoke check" -ForegroundColor Green
    Exec "curl.exe -sS https://erp.mohiindustries.in/health" | Out-Null
    Write-Host "==> OK: https://erp.mohiindustries.in/auth/login" -ForegroundColor Green
}
finally {
    Pop-Location
}
