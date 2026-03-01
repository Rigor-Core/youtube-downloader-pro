import sys
import os

def search_youtube(query, limit=25, lang="es"):
    """
    Realiza una búsqueda súper rápida en YouTube usando yt-dlp como librería.
    Devuelve una lista de diccionarios con title, id, url, duration y thumbnail.
    """
    results = []
    try:
        import yt_dlp
        
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True,
            'ignoreerrors': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            search_results = ydl.extract_info(f"ytsearch{limit}:{query}", download=False)
            
            if not search_results or 'entries' not in search_results:
                return []
            
            for entry in search_results['entries']:
                if not entry:
                    continue
                try:
                    vid_id = entry.get('id', '')
                    title = entry.get('title', '')
                    duration = entry.get('duration')
                    
                    # Format duration
                    if duration:
                        mins, secs = divmod(int(duration), 60)
                        hours, mins = divmod(mins, 60)
                        if hours > 0:
                            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
                        else:
                            duration_str = f"{mins}:{secs:02d}"
                    else:
                        duration_str = "N/A"
                    
                    if vid_id and title:
                        results.append({
                            'title': title,
                            'thumbnail': f"https://i.ytimg.com/vi/{vid_id}/hqdefault.jpg",
                            'url': f"https://www.youtube.com/watch?v={vid_id}",
                            'duration': duration_str,
                            'id': vid_id
                        })
                except Exception:
                    continue
                
    except Exception as e:
        print(f"[Search API Error] {e}")
        return []

    return results
