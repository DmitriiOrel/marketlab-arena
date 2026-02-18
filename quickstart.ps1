param(
    [Parameter(Mandatory = $true)]
    [string]$Token,
    [string]$PythonVersion = "3.11",
    [switch]$Run
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' not found. Install Python 3.11+ first."
}

$pyArgs = @("-$PythonVersion")
try {
    py @pyArgs --version | Out-Null
}
catch {
    Write-Host "Python $PythonVersion not found, using default 'py'."
    $pyArgs = @()
}

if (-not (Test-Path ".venv\\Scripts\\python.exe")) {
    py @pyArgs -m venv .venv
}

$pythonExe = Join-Path $PSScriptRoot ".venv\\Scripts\\python.exe"

& $pythonExe -m pip install --upgrade pip
& $pythonExe -m pip install -r requirements.txt

if (-not (Test-Path ".env")) {
    Copy-Item ".env.template" ".env"
}

$env:SETUP_TOKEN = $Token
$env:PYTHONPATH = "."
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:ALL_PROXY = ""
$env:all_proxy = ""

@'
import os
from pathlib import Path

from tinkoff.invest import Client
from tinkoff.invest.constants import INVEST_GRPC_API_SANDBOX

token = os.environ["SETUP_TOKEN"].strip()
if not token:
    raise ValueError("Token is empty")

with Client(token, target=INVEST_GRPC_API_SANDBOX) as client:
    accounts = client.users.get_accounts().accounts
    if not accounts:
        client.sandbox.open_sandbox_account()
        accounts = client.users.get_accounts().accounts
    account_id = accounts[0].id

env_path = Path(".env")
env_path.write_text(
    f"TOKEN={token}\nACCOUNT_ID={account_id}\nSANDBOX=True\n",
    encoding="utf-8",
)

print(account_id)
'@ | & $pythonExe -

Write-Host ""
Write-Host "Setup complete."
Write-Host "ACCOUNT_ID written to .env."
Write-Host "Run bot: .\\run_sandbox.ps1"

if ($Run) {
    & ".\\run_sandbox.ps1"
}
