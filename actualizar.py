import requests

CANALES_ATB = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c"
}

def obtener_m3u8(video_id):
    # Usamos la API de datos oficial solicitando específicamente el parámetro de Live HLS
    url_api = f"https://api.dailymotion.com/video/{video_id}?fields=stream_live_hls_url"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    }
    
    try:
        response = requests.get(url_api, headers=headers, timeout=15)
        if response.status_code == 200:
            datos = response.json()
            url_stream = datos.get("stream_live_hls_url")
            if url_stream:
                return url_stream
            else:
                print(f" -> La API no devolvió stream_live_hls_url para el ID {video_id}. Verifique si está en vivo.")
        else:
            print(f" -> Error de API pública (HTTP {response.status_code}) para ID {video_id}")
    except Exception as e:
        print(f" -> Error de conexión con ID {video_id}: {e}")
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    enlaces_encontrados = 0
    
    for nombre, video_id in CANALES_ATB.items():
        print(f"Consultando API oficial para: {nombre}...")
        url = obtener_m3u8(video_id)
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\n{url}\n'
            enlaces_encontrados += 1
            print("    [+] Enlace obtenido con éxito.")
        else:
            print("    [-] Falló la obtención.")
            
    # Forzamos la escritura para mantener el flujo de GitHub activo
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
    print(f"\nProceso finalizado. Total guardados: {enlaces_encontrados} canales.")

if __name__ == "__main__":
    generar_m3u()
