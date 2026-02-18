$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

$pythonExe = Join-Path $PSScriptRoot ".venv\\Scripts\\python.exe"
if (-not (Test-Path $pythonExe)) {
    throw "Virtual environment not found. Run .\\quickstart.ps1 -Token <YOUR_TOKEN> first."
}

if (-not (Test-Path ".env")) {
    throw ".env not found. Run .\\quickstart.ps1 -Token <YOUR_TOKEN> first."
}

$env:PYTHONPATH = "."
$env:PYTHONDONTWRITEBYTECODE = "1"
$env:HTTP_PROXY = ""
$env:HTTPS_PROXY = ""
$env:http_proxy = ""
$env:https_proxy = ""
$env:ALL_PROXY = ""
$env:all_proxy = ""

& $pythonExe ".\\app\\main.py"
