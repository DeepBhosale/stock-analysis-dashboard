$RootDir = $PSScriptRoot
$BackendDir = Join-Path $RootDir 'backend'
$FrontendDir = Join-Path $RootDir 'frontend'
$VenvPython = Join-Path $BackendDir '.venv-backend\Scripts\python.exe'

Write-Host "Setting up backend..."
if (-Not (Test-Path $BackendDir)) {
    Write-Error "Backend folder not found: $BackendDir"
    exit 1
}

if (-Not (Test-Path $VenvPython)) {
    Set-Location $BackendDir
    python -m venv .venv-backend
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create Python virtual environment. Make sure Python is installed and available as 'python'."
        exit 1
    }
}

& $VenvPython -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to upgrade pip."
    exit 1
}

& $VenvPython -m pip install -r (Join-Path $BackendDir 'requirements.txt')
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install backend dependencies."
    exit 1
}

Write-Host "Setting up frontend..."
if (-Not (Test-Path $FrontendDir)) {
    Write-Error "Frontend folder not found: $FrontendDir"
    exit 1
}

Set-Location $FrontendDir
npm install
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to install frontend dependencies. Make sure Node.js is installed."
    exit 1
}

Set-Location $RootDir
Write-Host "Setup complete."
Write-Host "Run the project with: .\start-all.ps1"
