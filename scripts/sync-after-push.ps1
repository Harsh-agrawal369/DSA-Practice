param(
    [Parameter(Mandatory = $true)]
    [string]$RemoteName,

    [Parameter(Mandatory = $true)]
    [string]$Branch,

    [Parameter(Mandatory = $true)]
    [string]$PushedSha,

    [int]$TimeoutSeconds = 180
)

$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." )).Path
Set-Location $repositoryRoot
$deadline = (Get-Date).ToUniversalTime().AddSeconds($TimeoutSeconds)

Write-Host "Waiting for GitHub Actions to finish the README update..."

while ((Get-Date).ToUniversalTime() -lt $deadline) {
    git fetch --quiet $RemoteName $Branch 2>$null
    $remoteSha = (git rev-parse "$RemoteName/$Branch" 2>$null).Trim()

    if ($remoteSha -and $remoteSha -ne $PushedSha) {
        Write-Host "Remote changes found. Pulling them with rebase..."
        git pull --rebase $RemoteName $Branch
        exit $LASTEXITCODE
    }

    Start-Sleep -Seconds 3
}

Write-Warning "No follow-up README commit appeared within $TimeoutSeconds seconds. Run 'git pull --rebase' when the workflow finishes."
exit 0
