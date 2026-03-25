#!/bin/bash
# ─────────────────────────────────────────────
#  Cotizador Barbaratto — Launcher macOS
#  Doble clic para abrir. Se abre en el navegador.
# ─────────────────────────────────────────────

cd "$(dirname "$0")"

# Activar conda
eval "$(/opt/anaconda3/bin/conda shell.bash hook)"
conda activate barbaratto

# Instalar streamlit si falta
pip install --quiet -r requirements.txt 2>/dev/null

echo "Iniciando Cotizador Barbaratto..."
streamlit run app.py --server.headless=true
