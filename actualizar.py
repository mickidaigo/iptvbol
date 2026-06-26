import requests

CANALES_BOL = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c",
    "Bolivia TV 7.1": "x9nzqpo",
    "Bolivia TV 7.2": "x9ny70y",
    "Red UNO SCZ": "x9n2qyk"
}

def obtener_m3u8(video_id):
    # Endpoint alternativo directo y compatible
    url_api = f"https://dailymotion.com{video_id}"
    
    # Cabeceras estrictas simulando un navegador Chrome actualizado
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9",
        "Referer": "https://www.dailymotion.com/",
        "Origin": "https://www.dailymotion.com"
    }
    
    try:
        response = requests.get(url_api, headers=headers, timeout=15)
        if response.status_code == 200:
            datos = response.json()
            # Intenta buscar la url del stream adaptativo automático
            qualities = datos.get("qualities", {})
            auto_quality = qualities.get("auto", [])
            if auto_quality and isinstance(auto_quality, list):
                url_stream = auto_quality[0].get("url")
                if url_stream:
                    return url_stream
    except Exception as e:
        print(f"Error al conectar con ID {video_id}: {e}")
        return None
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_BOL.items():
        print(f"Consultando señal de: {nombre}...")
        url = obtener_m3u8(video_id)
        if url:
            # Reemplazar caracteres de escape típicos de JSON si aparecen
            url = url.replace("\\/", "/")
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print(f" -> Éxito.")
        else:
            print(f" -> No se pudo extraer la señal (Bloqueo de API).")
    
    # Guardar archivo solo si contiene canales, evita romper el M3U previo si hay error general
    if enlaces_encontrados > 0:
        with open("lista.m3u", "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"Proceso completo. Canales guardados: {enlaces_encontrados}")
    else:
        print("Error crítico: No se capturó ningún canal activo. Archivo no modificado.")

if __name__ == "__main__":
    generar_m3u()
