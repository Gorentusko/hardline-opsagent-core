# Hardline OpsAgent Core Windows test helper
# Run from the repository root in PowerShell after installing Docker Desktop.

$ErrorActionPreference = "Stop"

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
}

docker compose up --build
