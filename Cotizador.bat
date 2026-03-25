@echo off
REM ─────────────────────────────────────────────
REM  Cotizador Barbaratto — Launcher Windows
REM  Doble clic para abrir. Se abre en el navegador.
REM ─────────────────────────────────────────────

cd /d "%~dp0"

if not exist ".venv" (
    echo Primera ejecucion: configurando entorno...
    python -m venv .venv
    .venv\Scripts\pip install --quiet -r requirements.txt
    echo Entorno listo.
)

echo Instalando dependencias...
.venv\Scripts\pip install --quiet -r requirements.txt 2>nul

echo Iniciando Cotizador Barbaratto...
.venv\Scripts\streamlit run app.py --server.headless=true
