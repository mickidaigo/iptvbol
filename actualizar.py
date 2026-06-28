<?php
// Configurar cabeceras para que el reproductor IPTV reconozca el archivo M3U
header('Content-Type: application/vnd.apple.mpegurl; charset=utf-8');
header('Content-Disposition: inline; filename="atb_bolivia.m3u"');

// Diccionario con los canales de ATB y sus IDs de Dailymotion
$canales_atb = [
    "ATB La Paz" => "x84eirw",
    "ATB Cochabamba" => "x89sfvo",
    "ATB Santa Cruz" => "x84t82c"
];

function obtener_m3u8_real($video_id) {
    // URL del reproductor integrado
    $url_embed = "https://dailymotion.com" . $video_id . "?autoplay=1&mute=1";
    
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url_embed);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
    curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
    curl_setopt($ch, CURLOPT_TIMEOUT, 15);
    
    // Fingir que somos un navegador móvil real para evitar bloqueos
    curl_setopt($ch, CURLOPT_HTTPHEADER, [
        "User-Agent: Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Mobile Safari/537.36",
        "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language: es-ES,es;q=0.8",
        "Referer: https://atb.com.bo",
        "Origin: https://atb.com.bo"
    ]);
    
    $html = curl_exec($ch);
    curl_close($ch);
    
    if ($html) {
        // Buscar la URL del m3u8 maestro dentro del código de la página
        if (preg_match('/"type":"application\\\\\/x-mpegURL","url":"([^"]+)"/', $html, $matches)) {
            // Limpiar los caracteres de escape de la URL extraída
            $url_m3u8 = str_replace('\/', '/', $matches[1]);
            return urldecode($url_m3u8);
        }
    }
    return null;
}

// Iniciar la estructura de la lista de canales
echo "#EXTM3U\n";

foreach ($canales_atb as $nombre => $video_id) {
    $url_streaming = obtener_m3u8_real($video_id);
    
    if ($url_streaming) {
        // Si el hosting web extrae el enlace con éxito, se añade a la lista
        echo '#EXTINF:-1 tvg-id="' . $video_id . '" tvg-name="' . $nombre . '" group-title="Bolivia" tvg-logo="https://atb.com.bowp-content/uploads/2023/04/logo-atb.png", ' . $nombre . "\n";
        echo $url_streaming . "\n";
    } else {
        // Enlace de respaldo bien formateado en caso de caída temporal
        echo '#EXTINF:-1 tvg-id="' . $video_id . '" tvg-name="' . $nombre . '" group-title="Bolivia", ' . $nombre . "\n";
        echo "https://dailymotion.com" . $video_id . "\n";
    }
}
?>
