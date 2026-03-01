import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
import urllib.request
import threading
from io import BytesIO
from PIL import Image

from .downloader import YoutubeDownloader
from .utils import get_default_downloads_folder
from .search import search_youtube
from .i18n import AppConfig

# Set Dark Theme and color scheme
ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.cfg = AppConfig()
        
        self.root.title(self.cfg._("app_title"))
        self.root.geometry("900x720")
        
        # Configure grid for expansion
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        
        self.current_download_path = tk.StringVar(value=get_default_downloads_folder())
        self.url_var = tk.StringVar()
        self.resolution_var = tk.StringVar(value="1080")
        self.fps_var = tk.StringVar(value="60")
        self.display_codec_var = tk.StringVar(value=self.cfg._("codec_h264"))
        
        self.codec_map = {
            self.cfg._("codec_h264"): "avc",
            self.cfg._("codec_vp9"): "vp9",
            self.cfg._("codec_any"): "any"
        }
        
        self.lang_map = {
            self.cfg._("lang_original"): "any"
        }
        self.display_lang_var = tk.StringVar(value=self.cfg._("lang_original"))
        
        # Debounce timer for size estimation
        self._size_timer = None
        self.url_var.trace_add("write", self._schedule_size_estimation)
        self.resolution_var.trace_add("write", self._schedule_size_estimation)
        
        self._build_ui()
        
        self.downloader = YoutubeDownloader(
            progress_callback=self._on_progress,
            finished_callback=self._on_finished,
            error_callback=self._on_error
        )

    def _build_ui(self):
        # Header frame for Settings Gear
        self.header_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 0))
        self.header_frame.grid_columnconfigure(0, weight=1)
        
        # Add Settings Gear Button in the top right
        self.settings_btn = ctk.CTkButton(
            self.header_frame, 
            text="⚙", 
            width=30, 
            height=30, 
            font=ctk.CTkFont(size=18), 
            command=self._open_language_settings
        )
        self.settings_btn.grid(row=0, column=1, sticky="e", padx=(0, 10))

        # Create a Tabview to separate Downloader and Search
        self.tabview = ctk.CTkTabview(self.root, width=860, height=660)
        self.tabview.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.root.grid_rowconfigure(1, weight=1)
        
        self.tabview.add(self.cfg._("tab_downloader"))
        self.tabview.add(self.cfg._("tab_search"))
        
        self._build_downloader_tab(self.tabview.tab(self.cfg._("tab_downloader")))
        self._build_search_tab(self.tabview.tab(self.cfg._("tab_search")))
        
        # Rigor-Core Watermark
        watermark = ctk.CTkLabel(self.root, text="Rigor-Core", text_color="gray50", font=ctk.CTkFont(size=12, weight="bold"))
        watermark.place(relx=0.02, rely=0.98, anchor="sw")

    def _open_language_settings(self):
        # Mini settings window to change language
        settings_win = ctk.CTkToplevel(self.root)
        settings_win.title("Idioma / Language")
        settings_win.geometry("300x200")
        settings_win.attributes("-topmost", True)
        
        ctk.CTkLabel(settings_win, text="Select Language:", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        lang_var = tk.StringVar(value=self.cfg.get_lang())
        langs = {"Español": "es", "English": "en", "Français": "fr", "Português": "pt", "Русский": "ru"}
        
        def apply_lang():
            selected = lang_var.get()
            self.cfg.set_lang(selected)
            settings_win.destroy()
            messagebox.showinfo("Reinicio requerido", "Please restart the app to apply language changes \nPor favor reinicia la aplicación para aplicar los cambios.")
            
        cbox = ctk.CTkOptionMenu(settings_win, variable=lang_var, values=list(langs.keys()))
        # map code back to display name
        rev_langs = {v: k for k, v in langs.items()}
        cbox.set(rev_langs.get(self.cfg.get_lang(), "Español"))
        
        # On change, set the var to code
        def on_select(val):
            lang_var.set(langs[val])
        cbox.configure(command=on_select)
        cbox.pack(pady=10)
        
        ctk.CTkButton(settings_win, text="Apply", command=apply_lang).pack(pady=20)

    def _build_downloader_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        
        # Title
        title_label = ctk.CTkLabel(parent, text=self.cfg._("downloader_title"), font=ctk.CTkFont(size=24, weight="bold"))
        title_label.grid(row=0, column=0, padx=20, pady=(20, 30), sticky="nw")

        # URL Input Frame
        url_frame = ctk.CTkFrame(parent, fg_color="transparent")
        url_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        url_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(url_frame, text=self.cfg._("url_label"), width=120, anchor="e").grid(row=0, column=0, padx=(0, 10))
        url_entry = ctk.CTkEntry(url_frame, textvariable=self.url_var, placeholder_text="https://www.youtube.com/watch?v=...")
        url_entry.grid(row=0, column=1, sticky="ew")

        # Download Path Frame
        path_frame = ctk.CTkFrame(parent, fg_color="transparent")
        path_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        path_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(path_frame, text=self.cfg._("save_label"), width=120, anchor="e").grid(row=0, column=0, padx=(0, 10))
        path_entry = ctk.CTkEntry(path_frame, textvariable=self.current_download_path, state="disabled")
        path_entry.grid(row=0, column=1, sticky="ew", padx=(0, 10))
        explore_btn = ctk.CTkButton(path_frame, text=self.cfg._("explore_btn"), width=100, command=self._choose_folder)
        explore_btn.grid(row=0, column=2)

        # Settings Frame (Quality, FPS, Codec)
        settings_frame = ctk.CTkFrame(parent)
        settings_frame.grid(row=3, column=0, padx=20, pady=20, sticky="ew")
        for i in range(6):
            settings_frame.grid_columnconfigure(i, weight=1)

        # Resolution
        ctk.CTkLabel(settings_frame, text=self.cfg._("res_label")).grid(row=0, column=0, padx=10, pady=15, sticky="e")
        self.res_cb = ctk.CTkOptionMenu(settings_frame, variable=self.resolution_var, values=["4320", "2160", "1440", "1080", "720", "480", "360"], width=100)
        self.res_cb.grid(row=0, column=1, padx=10, pady=15, sticky="w")
        
        # FPS
        ctk.CTkLabel(settings_frame, text=self.cfg._("fps_label")).grid(row=0, column=2, padx=10, pady=15, sticky="e")
        fps_cb = ctk.CTkOptionMenu(settings_frame, variable=self.fps_var, values=["60", "30"], width=100)
        fps_cb.grid(row=0, column=3, padx=10, pady=15, sticky="w")

        # Codec
        ctk.CTkLabel(settings_frame, text=self.cfg._("codec_label")).grid(row=0, column=4, padx=10, pady=15, sticky="e")
        codec_cb = ctk.CTkOptionMenu(settings_frame, variable=self.display_codec_var, values=list(self.codec_map.keys()), width=200)
        codec_cb.grid(row=0, column=5, padx=10, pady=15, sticky="w")
        
        # Row 1: Audio Language and Estimated Size
        ctk.CTkLabel(settings_frame, text=self.cfg._("lang_label")).grid(row=1, column=0, padx=10, pady=15, sticky="e")
        self.lang_cb = ctk.CTkOptionMenu(settings_frame, variable=self.display_lang_var, values=list(self.lang_map.keys()), width=200)
        self.lang_cb.grid(row=1, column=1, columnspan=3, padx=10, pady=15, sticky="w")
        
        self.size_label = ctk.CTkLabel(settings_frame, text=self.cfg._("size_label_dash"), text_color="gray")
        self.size_label.grid(row=1, column=4, columnspan=2, padx=10, pady=15, sticky="w")

        # Progress Section Frame
        progress_frame = ctk.CTkFrame(parent, fg_color="transparent")
        progress_frame.grid(row=4, column=0, padx=20, pady=20, sticky="ew")
        
        self.status_label = ctk.CTkLabel(progress_frame, text=self.cfg._("status_ready"), anchor="w")
        self.status_label.pack(fill="x", pady=(0, 10))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(fill="x")
        self.progress_bar.set(0)
        
        self.details_label = ctk.CTkLabel(progress_frame, text="", text_color="gray", anchor="e")
        self.details_label.pack(fill="x", pady=(5, 0))

        # Main Download Button
        self.download_btn = ctk.CTkButton(parent, text=self.cfg._("btn_download"), font=ctk.CTkFont(size=16, weight="bold"), height=50, command=self._start_download)
        self.download_btn.grid(row=5, column=0, padx=20, pady=30, sticky="ew")

    def _build_search_tab(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(1, weight=1)

        # Search Input
        search_top_frame = ctk.CTkFrame(parent, fg_color="transparent")
        search_top_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        search_top_frame.grid_columnconfigure(0, weight=1)

        self.search_var = tk.StringVar()
        search_entry = ctk.CTkEntry(search_top_frame, textvariable=self.search_var, placeholder_text=self.cfg._("search_placeholder"), height=40)
        search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        
        search_entry.bind("<Return>", lambda event: self._perform_search())
        
        self.search_btn = ctk.CTkButton(search_top_frame, text=self.cfg._("btn_search"), height=40, command=self._perform_search)
        self.search_btn.grid(row=0, column=1)

        # Results scrollable frame
        self.results_frame = ctk.CTkScrollableFrame(parent, label_text=self.cfg._("search_results_label"))
        self.results_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

    def _schedule_size_estimation(self, *args):
        if self._size_timer:
            self.root.after_cancel(self._size_timer)
        self._size_timer = self.root.after(1000, self._estimate_size)
        
    def _estimate_size(self):
        url = self.url_var.get().strip()
        target_res = int(self.resolution_var.get()) # Use target_res for filtering
        if not url or ("youtube.com" not in url and "youtu.be" not in url):
            self.size_label.configure(text=self.cfg._("size_label_dash"))
            return
            
        self.size_label.configure(text=self.cfg._("size_label_calculating"))
        
        def fetch_size():
            try:
                import yt_dlp
                app_lang = self.cfg.get_lang()
                ydl_opts = {
                    'quiet': True, 
                    'no_warnings': True,
                    'extractor_args': {'youtube': [f'lang={app_lang}', 'player_client=web']}
                }
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    formats = info.get('formats', [])
                    
                    # --- Extract available resolutions dynamically ---
                    available_resolutions = set()
                    for f in formats:
                        h = f.get('height')
                        if f.get('vcodec') != 'none' and h:
                            available_resolutions.add(h)
                    
                    if available_resolutions:
                        # Sort descending strings of resolutions
                        sorted_res = [str(r) for r in sorted(list(available_resolutions), reverse=True)]
                        
                        # Update the UI combobox dynamically
                        def update_res_ui():
                            # Save current selection
                            current_res = self.resolution_var.get()
                            self.res_cb.configure(values=sorted_res)
                            # If current selection is no longer valid for this video, pick the highest available
                            if current_res not in sorted_res:
                                self.resolution_var.set(sorted_res[0])
                        
                        self.root.after(0, update_res_ui)
                    # --------------------------------------------------
                    # --- Extract available languages dynamically ---
                    available_langs = set()
                    for f in formats:
                        language = f.get('language')
                        # Check strictly for audio tracks and non-null language strings
                        if f.get('acodec') != 'none' and f.get('vcodec') == 'none' and language:
                            available_langs.add(language)

                    # Allowed language prefixes (Spanish, English, French, Portuguese, Russian)
                    allowed_prefixes = ('es', 'en', 'fr', 'pt', 'ru')
                    # Dictionary mapping full technical tags to human-readable ones
                    lang_displays = {
                        'es': 'Español', 'en': 'Inglés', 'fr': 'Francés', 
                        'pt': 'Portugués', 'ru': 'Ruso'
                    }

                    new_lang_map = {self.cfg._("lang_original"): "any"}
        # Filter and build the readable map
                    for lang_code in available_langs:
                        if lang_code.startswith(allowed_prefixes):
                            prefix = lang_code[:2]
                            fancy_name = lang_displays.get(prefix, prefix.upper())
                            # Extra details if available (e.g. es-419 -> Español (es-419))
                            if len(lang_code) > 2:
                                fancy_name += f" ({lang_code})"
                            new_lang_map[fancy_name] = lang_code

                    self.lang_map = new_lang_map

                    # Update the UI combobox dynamically
                    def update_lang_ui():
                        current_lang_display = self.display_lang_var.get()
                        display_options = list(self.lang_map.keys())
                        self.lang_cb.configure(values=display_options)
                        
                        # Preserve selection if it still exists in the new mapping, otherwise fallback
                        if current_lang_display not in display_options:
                            self.display_lang_var.set(self.cfg._("lang_original"))

                    self.root.after(0, update_lang_ui)
                    # --------------------------------------------------                    
                    
                    v_size = 0
                    a_size = 0

                    videos = [f for f in formats if f.get('vcodec') != 'none' and f.get('height') and f.get('height') <= target_res]
                    if videos:
                        best_v = sorted(videos, key=lambda x: x.get('height', 0))[-1]
                        v_size = best_v.get('filesize') or best_v.get('filesize_approx') or 0
                        
                    audios = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
                    if audios:
                        best_a = sorted(audios, key=lambda x: x.get('abr', 0))[-1]
                        a_size = best_a.get('filesize') or best_a.get('filesize_approx') or 0
                        
                    total_bytes = v_size + a_size
                    if total_bytes > 0:
                        mb = total_bytes / (1024 * 1024)
                        self.root.after(0, lambda m=mb: self.size_label.configure(text=self.cfg._("size_label_value").format(mb=m)))
                    else:
                        self.root.after(0, lambda: self.size_label.configure(text=self.cfg._("size_label_unknown")))
            except Exception as e:
                import traceback
                traceback.print_exc() # Added stack trace
                self.root.after(0, lambda: self.size_label.configure(text=self.cfg._("size_label_error")))
                
        threading.Thread(target=fetch_size, daemon=True).start()

    def _choose_folder(self):
        folder = filedialog.askdirectory(initialdir=self.current_download_path.get(), title="Seleccionar carpeta de descargas")
        if folder:
            self.current_download_path.set(folder)

    def _start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showwarning(self.cfg._("warning_title"), self.cfg._("invalid_url"))
            return

        download_path = self.current_download_path.get()
        resolution = self.resolution_var.get()
        fps = self.fps_var.get()
        display_codec = self.display_codec_var.get()
        codec = self.codec_map.get(display_codec, "avc")
        
        audio_lang = self.lang_map.get(self.display_lang_var.get(), "any")

        # Configure download button for cancel toggle
        self.download_btn.configure(text=self.cfg._("btn_cancel"), command=self._cancel_download)
        self.progress_bar.set(0)
        self.status_label.configure(text=self.cfg._("status_ready"))
        self.details_label.configure(text="...")
        
        # Switch to download tab automatically
        self.tabview.set(self.cfg._("tab_downloader"))

        self.downloader.start_download_thread(url, download_path, resolution, fps, codec, audio_lang, app_lang=self.cfg.get_lang())

    def _on_progress(self, percent, speed, eta, filename):
        def update_ui():
            self.progress_bar.set(percent / 100.0)
            self.status_label.configure(text=self.cfg._("status_downloading").format(percent=f"{percent:.1f}"))
            self.details_label.configure(text=f"{speed} | ETA: {eta}")
        self.root.after(0, update_ui)

    def _on_finished(self):
        def finish_ui():
            self.status_label.configure(text=self.cfg._("download_complete"))
            self.details_label.configure(text="")
            self.progress_bar.set(1.0)
            self.download_btn.configure(text=self.cfg._("btn_download"), command=self._start_download)
            messagebox.showinfo(self.cfg._("success_title"), self.cfg._("download_complete"))
        self.root.after(0, finish_ui)

    def _on_error(self, message):
        def error_ui():
            self.status_label.configure(text=f"{self.cfg._('error_title')}", text_color="red")
            self.details_label.configure(text=message)
            self.download_btn.configure(text=self.cfg._("btn_download"), command=self._start_download) # Reset button state
            messagebox.showerror(self.cfg._("error_title"), f"{self.cfg._('download_error')}\n{message}")
        self.root.after(0, error_ui)
        
    def _cancel_download(self):
        self.downloader.cancel_download()
        self.status_label.configure(text=self.cfg._("status_canceled"), text_color="orange")
        self.download_btn.configure(state="disabled") # Disable button temporarily while cancelling
        # The downloader's error_callback will eventually be called with a cancellation message,
        # which will then re-enable the button and reset its text.
        
    def _perform_search(self):
        query = self.search_var.get().strip()
        if not query:
            return
            
        self.is_searching = True
        self.search_btn.configure(state="disabled")
        self._animate_search_button()
        
        # Clear previous results
        for widget in self.results_frame.winfo_children():
            widget.destroy()
            
        thread = threading.Thread(target=self._search_thread, args=(query,), daemon=True)
        thread.start()
        
    def _animate_search_button(self, count=0):
        if not getattr(self, 'is_searching', False):
            self.search_btn.configure(text=self.cfg._("btn_search"), state="normal")
            return
            
        dots = "." * (count % 4)
        self.search_btn.configure(text=f"{self.cfg._('btn_search')}{dots}")
        self.root.after(400, self._animate_search_button, count + 1)
        
    def _search_thread(self, query):
        results = search_youtube(query, limit=60, lang=self.cfg.get_lang())
        self.root.after(0, self._render_search_results, results)
        
    def _render_search_results(self, results):
        self.is_searching = False
        self.search_btn.configure(state="normal", text=self.cfg._("btn_search"))
        
        if not results:
            ctk.CTkLabel(self.results_frame, text="No results / Sin resultados.").grid(row=0, column=0, pady=20, padx=20)
            return
            
        # Configure layout inside results frame to 3 columns
        for i in range(3):
            self.results_frame.grid_columnconfigure(i, weight=1)
            
        for idx, result in enumerate(results):
            row = idx // 3
            col = idx % 3
            self._create_result_card(result, row, col)

    def _create_result_card(self, result, row, col):
        card_frame = ctk.CTkFrame(self.results_frame, fg_color=("gray85", "gray20"))
        card_frame.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        card_frame.grid_columnconfigure(0, weight=1)
        
        # Load thumbnail asynchronously
        thumb_label = ctk.CTkLabel(card_frame, text="[Cargando...]", width=160, height=120)
        thumb_label.grid(row=0, column=0, padx=10, pady=(10, 5))
        
        def fetch_image():
            try:
                req = urllib.request.Request(result['thumbnail'], headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req) as u:
                    raw_data = u.read()
                im = Image.open(BytesIO(raw_data))
                im.thumbnail((160, 120)) # Resize to fit
                photo = ctk.CTkImage(light_image=im, dark_image=im, size=(160, 120))
                self.root.after(0, lambda: thumb_label.configure(image=photo, text=""))
            except Exception as e:
                print(f"Error loading image: {e}")
                
        threading.Thread(target=fetch_image, daemon=True).start()
        
        # Title and Duration
        title = result.get('title', 'Sin título')
        if len(title) > 45: title = title[:42] + "..."
            
        title_label = ctk.CTkLabel(card_frame, text=title, font=ctk.CTkFont(size=13, weight="bold"), wraplength=200, justify="center")
        title_label.grid(row=1, column=0, padx=10, pady=(5, 0))
        
        duration = result.get('duration', 'N/A')
        dur_label = ctk.CTkLabel(card_frame, text=f"Duración: {duration}", font=ctk.CTkFont(size=12), text_color="gray")
        dur_label.grid(row=2, column=0, padx=10, pady=(0, 5))
        
        # Download Button
        def on_download_click():
            self.url_var.set(result['url'])
            self.tabview.set(self.cfg._("tab_downloader"))
            
        dl_btn = ctk.CTkButton(card_frame, text=self.cfg._("btn_download"), width=120, command=on_download_click)
        dl_btn.grid(row=3, column=0, padx=10, pady=(5, 10))
