import subprocess
import sys

def search_youtube(query, limit=25, lang="es"):
    """
    Realiza una búsqueda súper rápida en YouTube usando el CLI de yt-dlp.
    Devuelve una lista de diccionarios con title, id, url, duration y thumbnail.
    """
    results = []
    try:
        # Petición a yt-dlp: ID ||| Título ||| Duración
        cmd = [
            sys.executable, '-m', 'yt_dlp', 
            f'ytsearch{limit}:{query}', 
            '--flat-playlist', 
            '--print', '%(id)s|||%(title)s|||%(duration_string)s',
            '--no-warnings',
            '--ignore-errors'
        ]
        
        # Ocultar ventana emergente en Windows
        startupinfo = None
        if sys.platform == 'win32':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        process = subprocess.Popen(
            cmd, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            text=True, 
            encoding='utf-8', 
            errors='ignore',
            startupinfo=startupinfo
        )
        
        stdout, _ = process.communicate()
        
        if not stdout:
            return []

        lines = stdout.strip().split('\n')
        for line in lines:
            try:
                parts = line.split('|||')
                if len(parts) >= 2:
                    vid_id = parts[0].strip()
                    title = parts[1].strip()
                    duration = parts[2].strip() if len(parts) > 2 else "N/A"
                    
                    if vid_id and title:
                        results.append({
                            'title': title,
                            'thumbnail': f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg",
                            'url': f"https://www.youtube.com/watch?v={vid_id}",
                            'duration': duration,
                            'id': vid_id
                        })
            except Exception:
                continue
                
    except Exception as e:
        print(f"[Search API Error] {e}")
        return []

    return results
