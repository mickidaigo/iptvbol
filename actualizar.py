<?php
// Configurar cabeceras para que el reproductor IPTV reciba un archivo M3U8 válido
header('Content-Type: application/vnd.apple.mpegurl; charset=utf-8');
header('Content-Disposition: inline; filename="atb_bolivia.m3u"');

// Diccionario con los canales de ATB y sus respectivos IDs de Dailymotion
$canales_atb = [
  "ATB La Paz": "x84eirw",
    "ATB Cochabamba": "x89sfvo",
    "ATB Santa Cruz": "x84t82c",
    "Bolivia TV 7.1": "x9nzqpo",
    "Bolivia TV 7.2": "x9ny70y",
    "Red UNO SCZ": "x9n2qyk"
];

function obtener_m3u8_real($video_id) {
    // Simular el reproductor embebido tal como lo hace el script de Python
    $url_embed = "https://dailymotion.com" . $video_id . "?autoplay=1&mute=1";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url_embed);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    
    // Cabeceras idénticas a las de Python para simular un dispositivo móvil real
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept: */*",
        "Accept-Language: es-419,es;q=0.9",
        "Referer: https://atb.com.bo",
        "Origin: https://atb.com.bo"
    ]);
    
    $html = curl_exec($ch);
    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);
    
    if ($http_code === 200 && $html) {
        // Expresión regular principal para extraer la URL del streaming master
        if (preg_match('/"type":"application\\\\\/x-mpegURL","url":"([^"]+)"/', $html, $matches)) {
            $url_m3u8 = str_replace('\/', '/', $matches[1]);
            return urldecode($url_m3u8);
        }
        
        // Expresión regular secundaria (Respaldo directo de CDN)
        if (preg_match('/https:\/\/www\.dailymotion\.com\/cdn\/manifest\/video\/[^"\']+/', $html, $matches_alt)) {
            return str_replace('\/', '/', $matches_alt[0]);
        }
    }
    return null;
}

// Imprimir cabecera de la lista IPTV
echo "#EXTM3U\n";

foreach ($canales_atb as $nombre => $video_id) {
    $url_final = obtener_m3u8_real($video_id);
    
    // Solo añadimos el canal si se extrajo la URL dinámica real con éxito
    if ($url_final) {
        echo '#EXTINF:-1 tvg-id="' . $video_id . '" tvg-name="' . $nombre . '" group-title="Bolivia" tvg-logo="https://atb.com.bowp-content/uploads/2023/04/logo-atb.png", ' . $nombre . "\n";
        echo $url_final . "\n";
    }
}
?>
