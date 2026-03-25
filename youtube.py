"""
Descargador de YouTube con seleccion de resolucion/calidad.
Usa cookies de Firefox, pero reintenta sin ellas si limitan los formatos.
Requisitos: pip install yt-dlp, ffmpeg instalado.
"""

import os

import yt_dlp

CARPETA_DESTINO = "descargas"
NAVEGADOR_COOKIES = "firefox"
RESOLUCIONES_VALIDAS = {"360", "480", "720", "1080", "2160"}
CALIDADES_VALIDAS = {"128", "192", "256", "320"}

os.makedirs(CARPETA_DESTINO, exist_ok=True)


def mostrar_progreso(d):
    estado = d.get("status")
    if estado == "downloading":
        porcentaje = d.get("_percent_str", "N/A")
        velocidad = d.get("_speed_str", "N/A")
        eta = d.get("_eta_str", "N/A")
        print(f"\rProgreso: {porcentaje} | Velocidad: {velocidad} | ETA: {eta}", end="")
    elif estado == "finished":
        print("\nProcesando archivo...")


def _opciones_base():
    return {
        "outtmpl": os.path.join(CARPETA_DESTINO, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [mostrar_progreso],
        "quiet": False,
        "no_warnings": False,
    }


def _descargar(url, opciones):
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])


def _descargar_con_fallback_cookies(url, opciones):
    try:
        _descargar(url, opciones)
        return
    except Exception as error:
        print(f"\nAviso: fallo usando cookies de {NAVEGADOR_COOKIES}: {error}")
        print("Reintentando sin cookies del navegador...")

    opciones_sin_cookies = dict(opciones)
    opciones_sin_cookies.pop("cookiesfrombrowser", None)
    _descargar(url, opciones_sin_cookies)


def descargar_video(url, resolucion="best"):
    if resolucion != "best" and resolucion not in RESOLUCIONES_VALIDAS:
        print(f"\nResolucion no valida: {resolucion}")
        return

    selector_formato = (
        "bv*+ba/b"
        if resolucion == "best"
        else f"bv*[height<={resolucion}]+ba/b[height<={resolucion}]"
    )

    opciones = _opciones_base()
    opciones.update(
        {
            "format": selector_formato,
            "cookiesfrombrowser": (NAVEGADOR_COOKIES,),
            "merge_output_format": "mp4",
            "postprocessors": [
                {
                    "key": "FFmpegVideoConvertor",
                    "preferedformat": "mp4",
                }
            ],
        }
    )

    try:
        print(f"\nDescargando video de: {url}")
        print(f"Resolucion objetivo: {resolucion}")
        _descargar_con_fallback_cookies(url, opciones)
        print("\nDescarga completada.")
    except Exception as error:
        print(f"\nError al descargar: {error}")


def descargar_audio(url, calidad="best"):
    if calidad != "best" and calidad not in CALIDADES_VALIDAS:
        print(f"\nCalidad no valida: {calidad}")
        return

    opciones = _opciones_base()
    opciones.update(
        {
            "format": "bestaudio/best",
            "cookiesfrombrowser": (NAVEGADOR_COOKIES,),
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": calidad if calidad != "best" else "192",
                }
            ],
        }
    )

    try:
        print(f"\nDescargando audio de: {url}")
        print(
            "Calidad objetivo: mejor disponible"
            if calidad == "best"
            else f"Calidad objetivo: {calidad} kbps"
        )
        _descargar_con_fallback_cookies(url, opciones)
        print("\nDescarga completada.")
    except Exception as error:
        print(f"\nError al descargar: {error}")

def menu():
    print("=" * 50)
    print("DESCARGADOR DE YOUTUBE (Cookies de Firefox)")
    print("=" * 50)
    print("1. Descargar VIDEO")
    print("2. Descargar AUDIO MP3")
    print("3. Salir")

    opcion = input("\nSelecciona una opcion (1-3): ").strip()

    if opcion in ["1", "2"]:
        url = input("\nIngresa el link del video de YouTube: ").strip()

        if not url:
            print("\nDebes ingresar una URL valida.")
            return True

        if opcion == '1':
            print("\nResoluciones disponibles: 360, 480, 720, 1080, 2160 (4K)")
            resolucion = input("Selecciona resolucion (Enter para mejor disponible): ").strip() or "best"
            descargar_video(url, resolucion)
        else:
            print("\nCalidades de audio disponibles: 128, 192, 256, 320 kbps")
            calidad = input("Selecciona calidad (Enter para mejor disponible): ").strip() or "best"
            descargar_audio(url, calidad)

    elif opcion == "3":
        print("\nHasta luego.")
        return False
    else:
        print("\nOpcion no valida.")

    return True

if __name__ == "__main__":
    continuar = True
    while continuar:
        continuar = menu()
        if continuar:
            input("\nPresiona Enter para continuar...")
            print("\n" * 2)
