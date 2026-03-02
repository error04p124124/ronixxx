# PowerShell script to setup and run the Django project

Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "Inventory Management System - Ronix-L" -ForegroundColor Cyan
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""

# Check if virtual environment exists
if (Test-Path "venv") {
    Write-Host "[OK] Virtual environment found" -ForegroundColor Green
} else {
    Write-Host "[*] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    Write-Host "[OK] Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "[*] Activating virtual environment..." -ForegroundColor Yellow
.\venv\Scripts\Activate.ps1

# Check if requirements are installed
Write-Host "[*] Checking dependencies..." -ForegroundColor Yellow
$installed = pip list --format=freeze

if ($installed -notmatch "Django") {
    Write-Host "[*] Installing dependencies..." -ForegroundColor Yellow
    pip install -r requirements.txt
    Write-Host "[OK] Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "[OK] Dependencies already installed" -ForegroundColor Green
}

# Check if .env exists
if (Test-Path ".env") {
    Write-Host "[OK] .env file found" -ForegroundColor Green
} else {
    Write-Host "[!] .env file not found. Copying from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "[OK] .env file created" -ForegroundColor Green
}

# Check if migrations are applied
Write-Host "[*] Checking migrations..." -ForegroundColor Yellow
if (-not (Test-Path "db.sqlite3")) {
    Write-Host "[*] Applying migrations..." -ForegroundColor Yellow
    python manage.py makemigrations
    python manage.py migrate
    Write-Host "[OK] Migrations applied" -ForegroundColor Green
    
    # Ask to populate data
    Write-Host ""
    $populate = Read-Host "Load test data? (y/n)"
    if ($populate -eq "y" -or $populate -eq "Y") {
        python manage.py populate_data
        Write-Host "[OK] Test data loaded" -ForegroundColor Green
        Write-Host ""
        Write-Host "Test users:" -ForegroundColor Cyan
        Write-Host "  Client:  client / client123" -ForegroundColor White
        Write-Host "  Worker:  worker / worker123" -ForegroundColor White
    }
} else {
    Write-Host "[OK] Database already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host "[*] Starting development server..." -ForegroundColor Yellow
Write-Host "==================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Open browser: http://localhost:8080" -ForegroundColor Green
Write-Host "Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver 127.0.0.1:8080
