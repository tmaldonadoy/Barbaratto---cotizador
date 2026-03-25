# Cotizador Barbaratto

Sistema de cotización de productos de packaging con interfaz web local (Streamlit).

Incluye dos modos de acceso:
- **Ventas**: cotización rápida de cajas, cinta, film y cartón corrugado.
- **Manager** (con contraseña): edición de costos, márgenes, simulador de escenarios con gráficos y precios STOCK.

---

## Requisitos previos

- **Python 3.9 o superior**.
  - macOS: generalmente viene preinstalado. Verificar con `python3 --version`.
  - Windows: descargar desde [python.org](https://www.python.org/downloads/). **Marcar "Add Python to PATH"** durante la instalación.
- **pip** (viene incluido con Python).
- No se requiere Conda. Si usás Conda u otro gestor de entornos, simplemente activá tu entorno antes de ejecutar.

---

## Instalación y ejecución

### macOS

**Opción A — Doble clic:**

1. Abrir la carpeta `cotizacion` en Finder.
2. Doble clic en **`Cotizador.command`**.
3. Si macOS bloquea la ejecución: ir a **Ajustes del Sistema > Privacidad y Seguridad** y permitirlo.
4. La primera vez crea un entorno virtual e instala dependencias (~1 minuto).
5. Se abre el navegador en `http://localhost:8501`.

**Opcion B — Desde terminal:**

```bash
cd /ruta/a/cotizacion
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

### Windows

**Opción A — Doble clic:**

1. Abrir la carpeta `cotizacion` en el Explorador.
2. Doble clic en **`Cotizador.bat`**.
3. La primera vez crea un entorno virtual e instala dependencias (~2 minutos).
4. Se abre el navegador en `http://localhost:8501`.

**Opción B — Desde CMD / PowerShell:**

```cmd
cd C:\ruta\a\cotizacion
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### Usando Conda (opcional, cualquier SO)

Si prefieres usar Conda en lugar de venv:

```bash
conda create -n NOMBRE_ENTORNO python=3.11 -y
conda activate NOMBRE_ENTORNO
pip install -r requirements.txt
streamlit run app.py
```

Reemplaza `NOMBRE_ENTORNO` por el nombre que prefieras.

---

## Crear un paquete distribuible

Para enviar el cotizador a alguien que no quiere usar la terminal.

### macOS — Paquete .app con Automator

1. Abrir **Automator** (viene con macOS).
2. Crear nuevo documento > seleccionar **Aplicación**.
3. Buscar y arrastrar la acción **"Ejecutar script de Shell"**.
4. Pegar este script:
   ```bash
   cd "$(dirname "$0")/../Resources"
   if [ ! -d ".venv" ]; then
       python3 -m venv .venv
       .venv/bin/pip install --quiet -r requirements.txt
   fi
   open http://localhost:8501
   .venv/bin/streamlit run app.py --server.headless=true
   ```
5. Guardar como `Cotizador.app` (Formato: Aplicación).
6. Click derecho en `Cotizador.app` > **Mostrar contenido del paquete**.
7. Ir a `Contents/Resources/` y copiar ahí: `app.py`, `config.json`, `requirements.txt`.
8. Listo. `Cotizador.app` se abre con doble clic.

### macOS — Con Platypus (más profesional)

1. Instalar [Platypus](https://sveinbjorn.org/platypus) (gratis).
2. Abrir Platypus:
   - **Script Type**: bash
   - **Script Path**: seleccionar `Cotizador.command`
   - **Interface Type**: None
   - **Bundled Files**: agregar `app.py`, `config.json`, `requirements.txt`
3. Click en **Create App** > genera un `.app` con ícono personalizable.

### Windows — Opción simple (recomendada)

1. Instalar Python en la PC destino.
2. Copiar la carpeta `cotizacion` completa.
3. Doble clic en `Cotizador.bat`. Se configura solo la primera vez.

### Windows — Paquete .exe standalone (avanzado)

Para crear un `.exe` que no requiera Python instalado:

1. Instalar herramientas:
   ```cmd
   pip install -r requirements.txt
   pip install pyinstaller pywebview
   ```
2. Crear un archivo `launcher.py` en la carpeta:
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
     --collect-all streamlit ^
     launcher.py
   ```
4. El ejecutable queda en `dist\Cotizador.exe` (~150-200 MB).

> Algunos antivirus pueden marcarlo como falso positivo. Es normal con PyInstaller.

---

## Estructura del proyecto

```
cotizacion/
├── app.py               <- Interfaz Streamlit (venta + manager)
├── config.json          <- Parametros de costos y margenes (editable desde Manager)
├── requirements.txt     <- Dependencias Python
├── Cotizador.command    <- Launcher macOS (doble clic)
├── Cotizador.bat        <- Launcher Windows (doble clic)
├── cotizacion2025.cpp   <- Codigo original C++ (referencia)
└── README.md            <- Este archivo
```

## Credenciales

| Rol | Contraseña |
|-----|-----------|
| Ventas | *(sin contraseña)* |
| Manager | `barbaratto2025` |

La contraseña se puede cambiar editando `password_manager` en `config.json`.

---

## Solución de problemas

| Problema | Solución |
|----------|----------|
| `command not found: streamlit` | Ejecutar `pip install streamlit` en el entorno activo |
| El navegador no se abre | Ir manualmente a `http://localhost:8501` |
| Puerto 8501 ocupado | Cerrar otras instancias o usar `streamlit run app.py --server.port=8502` |
| macOS bloquea el .command | Ajustes del Sistema > Privacidad y Seguridad > Permitir |
| Windows: "python no se reconoce" | Reinstalar Python marcando "Add Python to PATH" |
