# Run this script to setup and start the application

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "║   🧠 Deep Learning Model Comparison Platform - Startup             ║" -ForegroundColor Cyan
Write-Host "║   Retina Dataset Analysis                                          ║" -ForegroundColor Cyan
Write-Host "║                                                                    ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "🔍 Checking Python installation..." -ForegroundColor Yellow
python --version

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found! Please install Python 3.8+" -ForegroundColor Red
    exit 1
}

Write-Host "✓ Python found!`n" -ForegroundColor Green

# Run setup
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "📦 RUNNING SETUP SCRIPT" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

python setup.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "`n❌ Setup failed!" -ForegroundColor Red
    exit 1
}

# Offer choices
Write-Host "`n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host "✅ SETUP COMPLETE!" -ForegroundColor Green
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━`n" -ForegroundColor Cyan

Write-Host "What would you like to do?`n" -ForegroundColor Yellow
Write-Host "  1) Open Jupyter Notebook" -ForegroundColor Cyan
Write-Host "  2) Launch Streamlit Dashboard" -ForegroundColor Cyan
Write-Host "  3) Exit" -ForegroundColor Cyan
Write-Host ""

$choice = Read-Host "Enter your choice (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`n📓 Opening Jupyter Notebook..." -ForegroundColor Green
        jupyter notebook notebooks/Retina_DL_Analysis.ipynb
    }
    "2" {
        Write-Host "`n📊 Launching Streamlit Dashboard..." -ForegroundColor Green
        Write-Host "Dashboard will open at: http://localhost:8501`n" -ForegroundColor Cyan
        streamlit run dashboard/app.py
    }
    "3" {
        Write-Host "`n👋 Goodbye!" -ForegroundColor Green
        exit 0
    }
    default {
        Write-Host "`n❌ Invalid choice!" -ForegroundColor Red
        exit 1
    }
}
