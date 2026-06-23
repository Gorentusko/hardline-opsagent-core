# Apply v0.1.4 package over an existing local repo.
# Run from the extracted v0.1.4 package root, not from inside the old repo.
# Example:
# powershell -ExecutionPolicy Bypass -File .\scripts\apply_v0_1_4_local_polish.ps1 -TargetRepo "C:\path\to\old\hardline-opsagent-core"

param(
    [Parameter(Mandatory=$true)]
    [string]$TargetRepo
)

$ErrorActionPreference = "Stop"

if (!(Test-Path $TargetRepo)) {
    Write-Host "Target repo does not exist: $TargetRepo"
    exit 1
}

if (!(Test-Path ".\docker-compose.yml")) {
    Write-Host "Run this script from the v0.1.4 hardline-opsagent-core folder."
    exit 1
}

Write-Host "Applying v0.1.4 polish to: $TargetRepo"

$exclude = @(".git", "data\reports", "data\state", ".env")
Get-ChildItem -Force | ForEach-Object {
    if ($exclude -contains $_.Name) { return }
    Copy-Item $_.FullName -Destination $TargetRepo -Recurse -Force
}

Write-Host "Done. Now run:"
Write-Host "cd `"$TargetRepo`""
Write-Host "git status"
Write-Host "git add ."
Write-Host "git commit -m `"Polish public GitHub release v0.1.4`""
