import requests

CANALES_ATB = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c"
}

def obtener_m3u8(video_id):
    # Consumimos el endpoint oficial de metadatos del reproductor
    url_api = f"https://dailymotion.com{video_id}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Referer": "https://dailymotion.com"
    }
    
    try:
        response = requests.get(url_api, headers=headers, timeout=15)
        if response.status_code == 200:
            datos = response.json()
            # Navegamos de forma segura en la estructura JSON del reproductor
            qualities = datos.get("qualities", {})
            auto_quality = qualities.get("auto", [])
            
            if auto_quality and isinstance(auto_quality, list) and len(auto_quality) > 0:
                url_stream = auto_quality[0].get("url")
                if url_stream:
                    # Limpiamos las barras inclinadas invertidas típicas del JSON
                    return url_stream.replace("\\/", "/")
    except Exception as e:
        print(f"Error en conexión para {video_id}: {e}")
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_ATB.items():
        print(f"Extrayendo flujo dinámico para: {nombre}...")
        url = obtener_m3u8(video_id)
        
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia" tvg-logo="https://atb.com.bo", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print("    [+] Éxito total.")
        else:
            print("    [-] Bloqueo temporal de IP detectado.")
            # Si falla, colocamos el enlace web oficial CORREGIDO por si el reproductor del usuario sabe procesarlo
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\nhttps://dailymotion.comvideo/{video_id}\n'
            
    # Forzamos la sobreescritura de la lista con los resultados reales
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\nProceso concluido. Canales con streaming directo .m3u8: {enlaces_encontrados}")

if __name__ == "__main__":
    generar_m3u()
