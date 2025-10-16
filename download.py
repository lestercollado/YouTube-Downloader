"""
Descargador de YouTube con selección de resolución/calidad
Cookies de Firefox automáticamente
Requisitos: pip install yt-dlp, ffmpeg instalado
"""

import yt_dlp
import os

CARPETA_DESTINO = 'descargas'
NAVEGADOR_COOKIES = 'firefox'

if not os.path.exists(CARPETA_DESTINO):
    os.makedirs(CARPETA_DESTINO)

def mostrar_progreso(d):
    if d['status'] == 'downloading':
        porcentaje = d.get('_percent_str', 'N/A')
        velocidad = d.get('_speed_str', 'N/A')
        print(f"\rProgreso: {porcentaje} - Velocidad: {velocidad}", end='')
    elif d['status'] == 'finished':
        print("\nProcesando archivo...")

def descargar_video(url, resolucion='best'):
    opciones = {
        'format': f'bestvideo[height<={resolucion}]+bestaudio/best' if resolucion != 'best' else 'bestvideo+bestaudio/best',
        'outtmpl': os.path.join(CARPETA_DESTINO, '%(title)s.%(ext)s'),
        'cookiesfrombrowser': (NAVEGADOR_COOKIES,),
        'merge_output_format': 'mp4',
        'progress_hooks': [mostrar_progreso],
        'quiet': False,
        'no_warnings': False,
    }
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            print(f"\nDescargando video de: {url} en resolución: {resolucion}")
            ydl.download([url])
            print("\n✅ ¡Descarga completada!")
    except Exception as e:
        print(f"\n❌ Error al descargar: {str(e)}")

def descargar_audio(url, calidad='best'):
    opciones = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(CARPETA_DESTINO, '%(title)s.%(ext)s'),
        'cookiesfrombrowser': (NAVEGADOR_COOKIES,),
        'progress_hooks': [mostrar_progreso],
        'quiet': False,
        'no_warnings': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': calidad if calidad != 'best' else '192',
        }],
    }
    try:
        with yt_dlp.YoutubeDL(opciones) as ydl:
            print(f"\nDescargando audio de: {url} con calidad: {calidad} kbps")
            ydl.download([url])
            print("\n✅ ¡Descarga completada!")
    except Exception as e:
        print(f"\n❌ Error al descargar: {str(e)}")

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
        
        if opcion == '1':
            print("\nResoluciones disponibles: 360, 480, 720, 1080, 2160 (4K)")
            resolucion = input("Selecciona resolución (Enter para mejor disponible): ").strip() or 'best'
            descargar_video(url, resolucion)
        else:
            print("\nCalidades de audio disponibles: 128, 192, 256, 320 kbps")
            calidad = input("Selecciona calidad (Enter para mejor disponible): ").strip() or 'best'
            descargar_audio(url, calidad)
    
    elif opcion == '3':
        print("\n¡Hasta luego! 👋")
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
