$repositoryRoot = (Resolve-Path (Join-Path $PSScriptRoot ".." )).Path
$hooksDirectory = Join-Path $repositoryRoot ".git\hooks"
$hookPath = Join-Path $hooksDirectory "post-push"

New-Item -ItemType Directory -Path $hooksDirectory -Force | Out-Null

$hook = @'
#!/bin/sh

read local_ref local_sha remote_ref remote_sha
case "$remote_ref" in
  refs/heads/*) branch="${remote_ref#refs/heads/}" ;;
  *) exit 0 ;;
esac

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "scripts/sync-after-push.ps1" \
  -RemoteName "$1" \
  -Branch "$branch" \
  -PushedSha "$local_sha"
exit $?
'@

Set-Content -Path $hookPath -Value $hook -Encoding ascii
Write-Host "Installed local post-push hook at $hookPath"
