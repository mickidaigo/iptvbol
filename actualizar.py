import requests
import os

CANALES_BOL = {
    "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c",
    "Bolivia TV 7.1": "x9nzqpo",
    "Bolivia TV 7.2": "x9ny70y",
    "Red UNO SCZ": "x9n2qyk"
}

def obtener_m3u8(video_id):
    url_api = f"https://dailymotion.com{video_id}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        response = requests.get(url_api, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json().get("qualities", {}).get("auto", [{}])[0].get("url")
    except Exception:
        return None
    return None

def generar_m3u():
    contenido = "#EXTM3U\n"
    for nombre, video_id in CANALES_BOL.items():
        url = obtener_m3u8(video_id)
        if url:
            contenido += f'#EXTINF:-1 tvg-id="{video_id}" tvg-name="{nombre}" group-title="Bolivia", {nombre}\n{url}\n'
    
    # Guarda el archivo en la carpeta raíz
    with open("lista.m3u", "w", encoding="utf-8") as f:
        f.write(contenido)
    print("Lista M3U actualizada con éxito.")

if __name__ == "__main__":
    generar_m3u()
