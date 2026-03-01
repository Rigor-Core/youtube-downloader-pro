import os
import yt_dlp
import threading
from .utils import clean_text

class YoutubeDownloader:
    def __init__(self, progress_callback=None, finished_callback=None, error_callback=None):
        self.progress_callback = progress_callback
        self.finished_callback = finished_callback
        self.error_callback = error_callback
        self.is_downloading = False
        self.cancel_requested = False

    def _progress_hook(self, d):
        if self.cancel_requested:
            raise Exception("Descarga cancelada por el usuario.")
            
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            
            if total_bytes > 0:
                percent = (downloaded / total_bytes) * 100
            else:
                raw_percent = d.get('_percent_str', '0%')
                percent_str = clean_text(raw_percent).replace('%', '')
                try:
                    percent = float(percent_str)
                except ValueError:
                    percent = 0.0
            
            speed = clean_text(d.get('_speed_str', 'N/A'))
            eta = clean_text(d.get('_eta_str', 'N/A'))
            filename = d.get('filename', '')
            
            if self.progress_callback:
                self.progress_callback(percent, speed, eta, filename)



    def download_video(self, url, download_path, resolution="1080", fps="60", codec="avc", app_lang="es"):
        self.is_downloading = True
        self.cancel_requested = False
        
        # Build the format string based on user settings
        # Video: max height <= resolution, max fps <= fps, preferred codec
        # Audio: best audio available
        
        # Codec logic: 'avc' indicates H264 (standar), 'vp9' indicates VP9 etc.
        # Fallback to ANY video codec if the specific one (like 'avc') is not available, avoiding 
        # a complete failure where it just downloads a pre-merged webm (often English/audio only).
        
        format_list = []
        if codec != "any":
            # 1. First try: Best video with specific codec + preferred audio
            format_list.append(f"bestvideo[height<={resolution}][fps<={fps}][vcodec^={codec}]+bestaudio")
        
        # 2. Fallback: Any video codec + preferred audio
        format_list.append(f"bestvideo[height<={resolution}][fps<={fps}]+bestaudio")
        
        # 3. Final Fallback: Best combined format
        format_list.append(f"best[height<={resolution}]")
        
        format_str = "/".join(format_list)
        
        ydl_opts = {
            'format': format_str,
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'progress_hooks': [self._progress_hook],
            'nocolor': True,
            'quiet': False,
            'no_warnings': False,
            'ignoreerrors': True,
            'extractor_args': {'youtube': [f'lang={app_lang}', 'player_client=web']}
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            if self.finished_callback:
                self.finished_callback()
                
        except Exception as e:
            if "Descarga cancelada" in str(e):
                if self.error_callback:
                    self.error_callback("La descarga fue cancelada.")
            else:
                if self.error_callback:
                    self.error_callback(f"Error al descargar: {str(e)}")
        finally:
            self.is_downloading = False
            self.cancel_requested = False

    def start_download_thread(self, url, download_path, resolution, fps, codec, app_lang="es"):
        if self.is_downloading:
            if self.error_callback:
                self.error_callback("Ya hay una descarga en curso.")
            return

        thread = threading.Thread(
            target=self.download_video,
            args=(url, download_path, resolution, fps, codec, app_lang),
            daemon=True
        )
        thread.start()
        
    def cancel_download(self):
        if self.is_downloading:
            self.cancel_requested = True
