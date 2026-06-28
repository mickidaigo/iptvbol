import requests
import re
import urllib.parse

CANALES_ATB = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c"
}

def obtener_m3u8(video_id):
    session = requests.Session()
    
    headers_base = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept": "*/*",
        "Accept-Language": "es-419,es;q=0.9",
        "Referer": "https://atb.com.bo",
        "Origin": "https://atb.com.bo"
    }
    session.headers.update(headers_base)
    
    try:
        url_embed = f"https://dailymotion.com{video_id}?autoplay=1&mute=1"
        response_embed = session.get(url_embed, timeout=15)
        
        if response_embed.status_code == 200:
            match = re.search(r'"type":"application\\/x-mpegURL","url":"([^"]+)"', response_embed.text)
            if match:
                url_m3u8 = match.group(1).replace("\\/", "/")
                return urllib.parse.unquote(url_m3u8)
                
            match_alt = re.search(r'https://dailymotion.com[^"\']+', response_embed.text)
            if match_alt:
                return match_alt.group(0).replace("\\/", "/")
                
    except Exception as e:
        print(f"Error procesando canal {video_id}: {str(e)}")
        
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_ATB.items():
        url = obtener_m3u8(video_id)
        
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia" tvg-logo="https://atb.com.bowp-content/uploads/2023/04/logo-atb.png", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print(f" -> Éxito: {nombre}")
        else:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\nhttps://dailymotion.com{video_id}\n'
            print(f" -> Respaldo para: {nombre}")
            
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
        
    print(f"\nProceso finalizado. Canales procesados: {enlaces_encontrados}")

if __name__ == "__main__":
    generar_m3u()
