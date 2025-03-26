# PowerShell script to set up MkDocs
# Run with: .\scripts\setup_docs.ps1

Write-Host "Setting up MkDocs for Hephaestus documentation..." -ForegroundColor Green

# Check if virtual environment exists
if (-not (Test-Path -Path ".\docs_env")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv docs_env
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
.\docs_env\Scripts\Activate.ps1

# Install dependencies
Write-Host "Installing documentation dependencies..." -ForegroundColor Yellow
pip install -r docs\requirements.txt

# Success message
Write-Host "`nSetup complete!" -ForegroundColor Green
Write-Host "To serve the documentation locally, run:" -ForegroundColor Cyan
Write-Host ".\docs_env\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "mkdocs serve" -ForegroundColor White
Write-Host "`nTo build the documentation for production, run:" -ForegroundColor Cyan
Write-Host ".\docs_env\Scripts\Activate.ps1" -ForegroundColor White
Write-Host "mkdocs build" -ForegroundColor White 