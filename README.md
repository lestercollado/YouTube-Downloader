# YouTube Downloader

A Python script to download YouTube videos and audio with customizable resolution/quality, utilizing Firefox browser cookies for authentication.

## Características

*   Descarga videos con resolución específica (360p, 480p, 720p, 1080p, 2160p).
*   Descarga audio en formato MP3 con calidad específica (128kbps, 192kbps, 256kbps, 320kbps).
*   Uso automático de cookies del navegador Firefox para acceder a contenido restringido.
*   Muestra el progreso de la descarga.

## Requisitos

*   Python 3.x
*   `yt-dlp` (se instalará automáticamente con `pip`)
*   `ffmpeg` (debe estar instalado en tu sistema y accesible desde la variable de entorno PATH para la conversión de audio y la fusión de video/audio).
*   Iniciar sesión en youtube en el navegador Firefox

## Instalación

1.  **Clonar el repositorio (o descargar `download.py`):**
    ```bash
    git clone https://github.com/tu_usuario/tu_repositorio.git
    cd tu_repositorio
    ```
    (Si solo descargaste el archivo `download.py`, navega a la carpeta donde lo guardaste).

2.  **Instalar dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Instalar FFmpeg:**
    * Descarga FFmpeg https://www.gyan.dev/ffmpeg/builds. En la sección “Release builds”, descarga el archivo ZIP que diga “full build”
    * C:\ffmpeg\bin\ffmpeg.exe
    * Presiona Win + R, escribe: sysdm.cpl
    * Ve a Opciones avanzadas → Variables de entorno
    * En la sección Variables del sistema, selecciona la variable llamada Path y haz clic en Editar
    * Añade la ruta completa de la carpeta bin, por ejemplo: C:\ffmpeg\bin
    * Acepta todo y reinicia tu terminal

## Uso

1.  Ejecuta el script desde tu terminal:
    ```bash
    python download.py
    ```

2.  Se mostrará un menú con las siguientes opciones:
    ```
    ==================================================
    DESCARGADOR DE YOUTUBE (Cookies de Firefox)
    ==================================================
    1. Descargar VIDEO
    2. Descargar AUDIO MP3
    3. Salir

    Selecciona una opción (1-3):
    ```

3.  **Para descargar un video:**
    *   Selecciona `1`.
    *   Ingresa el link del video de YouTube.
    *   Opcionalmente, ingresa la resolución deseada (ej. `720`, `1080`). Si dejas en blanco, se descargará la mejor calidad disponible.

4.  **Para descargar solo el audio (MP3):**
    *   Selecciona `2`.
    *   Ingresa el link del video de YouTube.
    *   Opcionalmente, ingresa la calidad de audio deseada en kbps (ej. `192`, `320`). Si dejas en blanco, se descargará la mejor calidad disponible.

Los archivos descargados se guardarán en la carpeta `descargas` dentro del directorio del script.

## Configuración (Opcional)

Puedes modificar las siguientes variables directamente en el archivo `download.py` si lo deseas:

*   `CARPETA_DESTINO`: La carpeta donde se guardarán las descargas (por defecto: `descargas`).
*   `NAVEGADOR_COOKIES`: El navegador desde donde se obtendrán las cookies (por defecto: `firefox`).
