import requests
import re

CANALES_ATB = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c"
}

def obtener_m3u8(video_id):
    # Consultamos la página del reproductor público de Dailymotion
    url_embed = f"https://dailymotion.com{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9"
    }
    
    try:
        response = requests.get(url_embed, headers=headers, timeout=15)
        if response.status_code == 200:
            # Buscamos la URL del archivo .m3u8 maestro dentro del HTML usando expresiones regulares
            match = re.search(r'"type":"application\\/x-mpegURL","url":"([^"]+)"', response.text)
            if match:
                url_limpia = match.group(1).replace("\\/", "/")
                return url_limpia
    except Exception as e:
        print(f"Error con ID {video_id}: {e}")
        return None
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_ATB.items():
        print(f"Buscando transmisión para: {nombre}...")
        url = obtener_m3u8(video_id)
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print(" -> Enlace extraído con éxito.")
        else:
            print(" -> No se pudo extraer la señal en este intento.")
    
    # FORZAMOS la creación del archivo siempre para evitar el error 128 de Git
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"Proceso finalizado. Enlaces guardados: {enlaces_encontrados}")

if __name__ == "__main__":
    generar_m3u()
