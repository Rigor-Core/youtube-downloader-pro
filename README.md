<div align="center">
  <h1>YouTube Downloader PRO 🎥</h1>
  <p>Una aplicación de escritorio rápida, moderna y en múltiples idiomas para descargar videos de YouTube con la máxima calidad.</p>
</div>

![Menú de Descarga](photos/p1.jpeg)
*Interfaz principal del descargador.*

![Menú de Búsqueda](photos/p2.jpeg)
*Buscador integrado súper veloz.*

---

## 🚀 Características Principales

- **Descarga de Alta Calidad**: Soporte para resoluciones desde 360p hasta 4K/8K a 60 FPS.
- **Selección de Códecs**: Elige entre H.264 (mayor compatibilidad) o VP9 (mejor compresión/calidad).
- **Soporte Multilenguaje**: Configura la interfaz en Español, Inglés, Francés, Portugués o Ruso desde el menú ⚙️.
- **Buscador Rápido Integrado**: Busca videos directamente desde la aplicación sin necesidad de abrir el navegador web.
- **Estimación de Peso**: Calcula automáticamente el tamaño estimado del archivo antes de descargar.
- **Cancelación Segura**: Detén cualquier descarga en cualquier momento.

---

## 📦 Método 1: Descargar el Ejecutable (.exe)

Si no quieres instalar Python ni librerías, ve a la sección de **[Releases](https://github.com/Rigor-Core/youtube-downloader-pro/releases)** para descargar directamente el archivo **`.exe`**.

1. Ve a **Releases** en este repositorio.
2. Descarga el archivo `YouTubeDownloaderPRO.exe`.
3. Ejecútalo y listo. No necesitas instalar Python, FFmpeg ni nada adicional.

---

## 🛠️ Método 2: Instalación para Desarrolladores (Python)

Si deseas ejecutar el código fuente o modificar la aplicación, sigue estos pasos:

### 1. Requisitos Previos
- [Python 3.10+](https://www.python.org/downloads/) (agrégalo al PATH durante la instalación).
- **FFmpeg**: Necesario para fusionar video y audio. Descárgalo desde [ffmpeg.org](https://ffmpeg.org/download.html) o coloca `ffmpeg.exe` y `ffprobe.exe` en una carpeta `bin/` dentro del proyecto.

### 2. Clonar el repositorio
```bash
git clone https://github.com/Rigor-Core/youtube-downloader-pro.git
cd youtube-downloader-pro
```

### 3. Instalar Dependencias
```bash
pip install yt-dlp customtkinter pillow
```

### 4. Ejecutar la Aplicación
```bash
python run.py
```

---

## 🏗️ Compilar el Ejecutable (.exe)

Para generar tu propio `.exe` standalone:

### Requisitos
```bash
pip install pyinstaller
```

### Preparar binarios
Coloca los siguientes archivos en la carpeta `bin/` del proyecto:
- `ffmpeg.exe` y `ffprobe.exe` — desde [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)
- `upx.exe` (opcional, para comprimir) — desde [upx.github.io](https://upx.github.io/)
- `icon.ico` — en la raíz del proyecto

### Compilar
```bash
python build.py
```

El ejecutable se generará en `dist/YouTubeDownloaderPRO.exe`.

---

## 🧰 Tecnologías Usadas
- [Python 3](https://www.python.org/) — Lenguaje base.
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter) — Interfaz gráfica moderna.
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) — Extracción de metadatos y descarga de YouTube.
- [FFmpeg](https://ffmpeg.org/) — Fusión de video + audio de máxima calidad.
- [PyInstaller](https://www.pyinstaller.org/) + [UPX](https://upx.github.io/) — Compilación y compresión del ejecutable.

---

## 🤝 Contribuciones
¡Las contribuciones son bienvenidas! Si encuentras un error o quieres sugerir mejoras, abre un *Issue* o envía un *Pull Request*.
