$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest
Set-Location $PSScriptRoot

function Clear-NetworkEnv {
    $vars = @(
        "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
        "http_proxy", "https_proxy", "all_proxy",
        "GIT_HTTP_PROXY", "GIT_HTTPS_PROXY",
        "PIP_NO_INDEX", "PIP_INDEX_URL", "PIP_EXTRA_INDEX_URL"
    )
    foreach ($name in $vars) {
        Remove-Item -Path ("Env:{0}" -f $name) -ErrorAction SilentlyContinue
    }
}

$pythonExe = Join-Path $PSScriptRoot ".venv\\Scripts\\python.exe"
if (-not (Test-Path $pythonExe)) {
    throw "Virtual environment not found. Run .\\quickstart.ps1 -Token <YOUR_TOKEN> first."
}

if (-not (Test-Path ".env")) {
    throw ".env not found. Run .\\quickstart.ps1 -Token <YOUR_TOKEN> first."
}

$env:PYTHONPATH = "."
$env:PYTHONDONTWRITEBYTECODE = "1"
Clear-NetworkEnv

& $pythonExe -c "import tinkoff.invest"
if ($LASTEXITCODE -ne 0) {
    throw "Dependency 'tinkoff.invest' is missing. Run .\\quickstart.ps1 -Token <YOUR_TOKEN> again."
}

& $pythonExe ".\\app\\main.py"
