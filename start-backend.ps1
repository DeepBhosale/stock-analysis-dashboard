# Run this from the repository root to start the backend quickly.
$BackendDir = Join-Path $PSScriptRoot 'backend'
$VenvPython = Join-Path $BackendDir '.venv-backend\Scripts\python.exe'

Set-Location $BackendDir

if (-Not (Test-Path $VenvPython)) {
    Write-Error "Backend virtual environment not found. Run: cd backend; python -m venv .venv-backend; .\.venv-backend\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

& $VenvPython -c "import sys" *> $null
if ($LASTEXITCODE -ne 0) {
    Write-Error "Backend virtual environment is broken or was copied from another folder. Recreate it with: cd backend; Remove-Item -Recurse -Force .venv-backend; python -m venv .venv-backend; .\.venv-backend\Scripts\python.exe -m pip install -r requirements.txt"
    exit 1
}

& $VenvPython -m uvicorn main:app --host 0.0.0.0 --port 8000
