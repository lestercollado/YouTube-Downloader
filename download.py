"""
Descargador de YouTube con seleccion de resolucion/calidad.
Usa cookies del navegador para videos restringidos cuando sea posible.
Requisitos: pip install yt-dlp y ffmpeg instalado.
"""

import os
import shutil
import yt_dlp

CARPETA_DESTINO = "descargas"
NAVEGADOR_COOKIES = "firefox"
RESOLUCIONES_VALIDAS = {"360", "480", "720", "1080", "1440", "2160"}
CALIDADES_VALIDAS = {"128", "192", "256", "320"}
FORMATOS_VIDEO_VALIDOS = {"mp4", "mkv"}

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
        "outtmpl": os.path.join(CARPETA_DESTINO, "%(title)s [%(id)s].%(ext)s"),
        "noplaylist": True,
        "progress_hooks": [mostrar_progreso],
        "quiet": False,
        "no_warnings": False,
    }


def _descargar_con_fallback_cookies(url, opciones):
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])
        return
    except Exception as e:
        print(f"\nError con cookies ({NAVEGADOR_COOKIES}): {e}")
        print("Reintentando sin cookies del navegador...")

    opciones_sin_cookies = dict(opciones)
    opciones_sin_cookies.pop("cookiesfrombrowser", None)
    try:
        with yt_dlp.YoutubeDL(opciones_sin_cookies) as ydl:
            ydl.download([url])
    except Exception as e:
        mensaje_error = str(e).lower()
        if "n challenge" in mensaje_error or "only images are available" in mensaje_error:
            _mostrar_ayuda_challenge()
        raise


def _mostrar_ayuda_challenge():
    runtimes = [rt for rt in ("node", "deno", "bun", "qjs") if shutil.which(rt)]
    print("\nNo se pudieron obtener formatos de video/audio de YouTube.")
    print("Esto suele pasar por cambios recientes en YouTube (n challenge / PO token).")
    print("Acciones recomendadas:")
    print("1) Actualiza yt-dlp: py -m pip install -U yt-dlp")
    if runtimes:
        print(f"2) Runtime JS detectado: {', '.join(runtimes)}")
    else:
        print("2) Instala un runtime JavaScript (Node.js recomendado): https://nodejs.org/")
    print("3) Reintenta la descarga.")


def descargar_video(url, resolucion="best", formato_salida="mp4"):
    if resolucion != "best" and resolucion not in RESOLUCIONES_VALIDAS:
        raise ValueError(f"Resolucion no valida: {resolucion}")
    if formato_salida not in FORMATOS_VIDEO_VALIDOS:
        raise ValueError(f"Formato de salida no valido: {formato_salida}")

    formato_video = (
        "bv*+ba/b"
        if resolucion == "best"
        else f"bv*[height<={resolucion}]+ba/b[height<={resolucion}]"
    )

    opciones = _opciones_base()
    opciones.update(
        {
            "format": formato_video,
            "merge_output_format": formato_salida,
            "cookiesfrombrowser": (NAVEGADOR_COOKIES,),
        }
    )

    print(f"\nDescargando video de: {url}")
    print(f"Resolucion objetivo: {resolucion}")
    print(f"Formato final: {formato_salida}")
    try:
        _descargar_con_fallback_cookies(url, opciones)
    except Exception as e:
        if resolucion != "best" and "Requested format is not available" in str(e):
            print("\nLa resolucion solicitada no esta disponible. Reintentando con mejor calidad disponible...")
            opciones["format"] = "bv*+ba/b"
            _descargar_con_fallback_cookies(url, opciones)
        else:
            raise
    print("\nDescarga de video completada.")


def descargar_audio(url, calidad="best"):
    if calidad != "best" and calidad not in CALIDADES_VALIDAS:
        raise ValueError(f"Calidad no valida: {calidad}")

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

    print(f"\nDescargando audio de: {url}")
    print(f"Calidad objetivo: {calidad} kbps")
    _descargar_con_fallback_cookies(url, opciones)
    print("\nDescarga de audio completada.")

def menu():
    print("="*50)
    print("DESCARGADOR DE YOUTUBE (Cookies de Firefox)")
    print("="*50)
    print("1. Descargar VIDEO")
    print("2. Descargar AUDIO MP3")
    print("3. Salir")
    
    opcion = input("\nSelecciona una opción (1-3): ").strip()
    
    if opcion in ['1', '2']:
        url = input("\nIngresa el link del video de YouTube: ").strip()
        if not url:
            print("\nDebes ingresar una URL valida.")
            return True
        
        if opcion == '1':
            print("\nResoluciones disponibles: 360, 480, 720, 1080, 1440, 2160")
            resolucion = input("Selecciona resolucion (Enter para mejor disponible): ").strip() or "best"
            formato_salida = input("Formato final de video [mp4/mkv] (Enter=mp4): ").strip().lower() or "mp4"
            try:
                descargar_video(url, resolucion, formato_salida)
            except ValueError as e:
                print(f"\nError: {e}")
            except Exception as e:
                print(f"\nError al descargar video: {e}")
        else:
            print("\nCalidades de audio disponibles: 128, 192, 256, 320 kbps")
            calidad = input("Selecciona calidad (Enter para mejor disponible): ").strip() or "best"
            try:
                descargar_audio(url, calidad)
            except ValueError as e:
                print(f"\nError: {e}")
            except Exception as e:
                print(f"\nError al descargar audio: {e}")
    
    elif opcion == '3':
        print("\nHasta luego.")
        return False
    else:
        print("\nOpción no válida.")
    
    return True

if __name__ == "__main__":
    continuar = True
    while continuar:
        continuar = menu()
        if continuar:
            input("\nPresiona Enter para continuar...")
            print("\n" * 2)
