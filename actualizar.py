import requests
import re
import urllib.parse

CANALES_BOL = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c",
    "Bolivia TV 7.1": "x9nzqpo",
    "Bolivia TV 7.2": "x9ny70y",
    "Red UNO SCZ": "x9n2qyk"
}

def obtener_m3u8(video_id):
    session = requests.Session()
    
    # 1. Definir cabeceras de alta confianza imitando a un dispositivo real
    headers_base = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "es-419,es;q=0.9",
        "Referer": "https://www.atb.com.bo/",
        "Origin": "https://www.atb.com.bo"
    }
    session.headers.update(headers_base)
    
    try:
        # 2. Paso clave: Visitar la URL embebida para forzar que Dailymotion nos asigne cookies válidas
        url_embed = f"https://dailymotion.com{video_id}?autoplay=1&mute=1"
        response_embed = session.get(url_embed, timeout=15)
        
        if response_embed.status_code == 200:
            # 3. Buscar la URL interna de metadatos protegida por el token de sesión dentro del código fuente
            match = re.search(r'"type":"application\\/x-mpegURL","url":"([^"]+)"', response_embed.text)
            
            if match:
                url_m3u8 = match.group(1).replace("\\/", "/")
                # Descodificar caracteres URL (%3A, %2F, etc.) si existieran
                return urllib.parse.unquote(url_m3u8)
                
            # Método alternativo secundario si cambiaron las variables internas del HTML
            match_alt = re.search(r'https://dailymotion.com[^"\']+', response_embed.text)
            if match_alt:
                return match_alt.group(0).replace("\\/", "/")
                
    except Exception as e:
        print(f"Error procesando canal {video_id}: {str(e)}")
        
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_BOL.items():
        print(f"Generando handshake para: {nombre}...")
        url = obtener_m3u8(video_id)
        
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia" tvg-logo="https://atb.com.bo", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print("    -> Enlace extraído con bypass de cookies exitoso.")
        else:
            print("    -> Bloqueo persistente. Intentando generar enlace de respaldo.")
            # Si todo falla, metemos el puente compatible como contingencia
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\nhttps://www.dailymotion.com/video/{video_id}\n'
            
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print(f"\nProceso finalizado. Total guardados: {enlaces_encontrados} transmisiones puras.")

if __name__ == "__main__":
    generar_m3u()
