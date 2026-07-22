# Run this from the repository root to start the full project.
$RootDir = $PSScriptRoot
$BackendScript = Join-Path $RootDir 'start-backend.ps1'
$FrontendScript = Join-Path $RootDir 'start-frontend.ps1'

if (-Not (Test-Path $BackendScript)) {
    Write-Error "Backend start script not found: $BackendScript"
    exit 1
}

if (-Not (Test-Path $FrontendScript)) {
    Write-Error "Frontend start script not found: $FrontendScript"
    exit 1
}

Start-Process powershell.exe -ArgumentList "-NoExit -ExecutionPolicy Bypass -File `"$BackendScript`"" -WorkingDirectory $RootDir
Start-Sleep -Seconds 3
Start-Process powershell.exe -ArgumentList "-NoExit -ExecutionPolicy Bypass -File `"$FrontendScript`"" -WorkingDirectory $RootDir

Write-Host "Backend and frontend are starting in separate windows."
Write-Host "Open the Vite URL shown in the frontend window, usually http://localhost:5173"
