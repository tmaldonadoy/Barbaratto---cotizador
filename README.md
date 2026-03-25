# Cotizador Barbaratto

Sistema de cotización de productos de packaging con interfaz web local (Streamlit).

Incluye dos modos de acceso:
- **Ventas**: cotización rápida de cajas, cinta, film y cartón corrugado.
- **Manager** (con contraseña): edición de costos, márgenes, simulador de escenarios con gráficos y precios STOCK.

---

## Requisitos previos

### macOS

1. **Python 3.9+** instalado. Verificar con:
   ```bash
   python3 --version
   ```
2. **(Opción A) Conda** — si ya tenés un entorno conda:
   ```bash
   conda activate barbaratto
   ```
3. **(Opción B) Sin conda** — funciona con cualquier Python 3.9+.

### Windows

1. **Python 3.9+** instalado desde [python.org](https://www.python.org/downloads/).
   - Durante la instalación, marcar **"Add Python to PATH"**.
2. Verificar con:
   ```cmd
   python --version
   ```

---

## Instalación y ejecución

### macOS — Opción 1: Doble clic

1. Abrir la carpeta `cotizacion` en Finder.
2. Hacer doble clic en **`Cotizador.command`**.
3. Si aparece un aviso de seguridad: ir a **Preferencias del Sistema > Privacidad y Seguridad** y permitir la ejecución.
4. La primera vez instala dependencias automáticamente (~1 minuto).
5. Se abre el navegador en `http://localhost:8501`.

> **Nota:** El launcher usa el entorno conda `barbaratto` ubicado en `/opt/anaconda3/envs/barbaratto`. Si tu entorno está en otra ruta, editá la línea de `conda` dentro de `Cotizador.command`.

### macOS — Opción 2: Desde terminal

```bash
cd /ruta/a/cotizacion
pip install -r requirements.txt
streamlit run app.py
```

### Windows — Opción 1: Doble clic

1. Abrir la carpeta `cotizacion` en el Explorador.
2. Hacer doble clic en **`Cotizador.bat`**.
3. La primera vez crea un entorno virtual e instala dependencias (~2 minutos).
4. Se abre el navegador en `http://localhost:8501`.

### Windows — Opción 2: Desde CMD / PowerShell

```cmd
cd C:\ruta\a\cotizacion
pip install -r requirements.txt
streamlit run app.py
```

---

## Crear un paquete distribuible

Si querés enviar el cotizador a alguien que no tiene Python instalado ni quiere usar la terminal.

### macOS — Paquete .app con Automator

1. Abrir **Automator** (viene con macOS).
2. Crear nuevo documento → seleccionar **Aplicación**.
3. Buscar y arrastrar la acción **"Ejecutar script de Shell"**.
4. Pegar este script:
   ```bash
   cd "$(dirname "$0")/../Resources"
   eval "$(/opt/anaconda3/bin/conda shell.bash hook)"
   conda activate barbaratto
   pip install --quiet -r requirements.txt 2>/dev/null
   open http://localhost:8501
   streamlit run app.py --server.headless=true
   ```
5. Guardar como `Cotizador.app` (Formato: Aplicación).
6. Click derecho en `Cotizador.app` → **Mostrar contenido del paquete**.
7. Ir a `Contents/Resources/` y copiar ahí los archivos: `app.py`, `config.json`, `requirements.txt`.
8. Ahora `Cotizador.app` se puede abrir con doble clic.

### macOS — Alternativa con Platypus (más profesional)

1. Instalar [Platypus](https://sveinbjorn.org/platypus) (gratis).
2. Abrir Platypus:
   - **Script Type**: bash
   - **Script Path**: seleccionar `Cotizador.command`
   - **Interface Type**: None
   - **Bundled Files**: agregar `app.py`, `config.json`, `requirements.txt`
3. Click en **Create App** → genera un `.app` con ícono que se ejecuta con doble clic.

### Windows — Paquete .exe con PyInstaller (avanzado)

> Para crear un `.exe` standalone que no requiera Python instalado, se necesita un wrapper. Esto es más complejo porque Streamlit corre como servidor web.

1. Instalar dependencias:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller pywebview
   ```
2. Crear un archivo `launcher.py`:
   ```python
   import subprocess
   import threading
   import time
   import webview

   def start_streamlit():
       subprocess.Popen(["streamlit", "run", "app.py",
                         "--server.headless=true",
                         "--server.port=8501"])

   if __name__ == "__main__":
       threading.Thread(target=start_streamlit, daemon=True).start()
       time.sleep(3)
       webview.create_window("Cotizador Barbaratto", "http://localhost:8501",
                             width=1024, height=720)
       webview.start()
   ```
3. Empaquetar:
   ```cmd
   pyinstaller --windowed --onefile ^
     --name "Cotizador" ^
     --add-data "app.py;." ^
     --add-data "config.json;." ^
     --add-data "requirements.txt;." ^
     --collect-all streamlit ^
     launcher.py
   ```
4. El ejecutable queda en `dist\Cotizador.exe`.

> **Nota:** El `.exe` generado puede pesar ~150-200 MB y algunos antivirus pueden marcarlo como falso positivo. Esto es normal con PyInstaller.

### Windows — Opción simple (recomendada)

Para la mayoría de los casos, la forma más práctica es:

1. Instalar Python en la PC destino.
2. Copiar la carpeta `cotizacion` completa.
3. Doble clic en `Cotizador.bat`.

---

## Estructura del proyecto

```
cotizacion/
├── app.py               ← Interfaz Streamlit (venta + manager)
├── config.json          ← Parámetros de costos y márgenes (editable desde Manager)
├── requirements.txt     ← Dependencias Python
├── Cotizador.command    ← Launcher macOS (doble clic)
├── Cotizador.bat        ← Launcher Windows (doble clic)
├── cotizacion2025.cpp   ← Código original C++ (referencia)
└── README.md            ← Este archivo
```

## Credenciales

| Rol | Contraseña |
|-----|-----------|
| Ventas | *(sin contraseña)* |
| Manager | `barbaratto2025` |

La contraseña se puede cambiar editando el campo `password_manager` en `config.json`.

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| "command not found: streamlit" | Ejecutar `pip install streamlit` en el entorno correcto |
| "command not found: conda" | Editar `Cotizador.command` y ajustar la ruta de conda |
| El navegador no se abre | Ir manualmente a `http://localhost:8501` |
| Puerto 8501 ocupado | Cerrar otras instancias de Streamlit o ejecutar `streamlit run app.py --server.port=8502` |
| macOS bloquea el .command | Preferencias del Sistema → Privacidad y Seguridad → Permitir |
