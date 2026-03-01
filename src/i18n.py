import json
import os

CONFIG_FILE = "config.json"
DEFAULT_LANG = "es"

TRANSLATIONS = {
    "es": {
        "app_title": "YouTube Downloader PRO",
        "tab_downloader": "Descargador",
        "tab_search": "Buscador",
        "downloader_title": "Descargador de Videos",
        "url_label": "URL del Video:",
        "save_label": "Guardar en:",
        "explore_btn": "Explorar...",
        "res_label": "Resolución:",
        "fps_label": "FPS Máximos:",
        "codec_label": "Códec de Video:",
        "lang_label": "Idioma de Audio:",
        "size_label_calculating": "Peso estimado: Calculando...",
        "size_label_unknown": "Peso estimado: Desconocido",
        "size_label_error": "Peso estimado: Error al calcular",
        "size_label_value": "Peso estimado: ~{mb:.1f} MB",
        "status_ready": "Listo para descargar.",
        "btn_download": "Iniciar Descarga",
        "btn_cancel": "Cancelar",
        "search_placeholder": "Ingresa el nombre de un video para buscar...",
        "btn_search": "Buscar",
        "search_results_label": "Resultados de la búsqueda",
        "warning_title": "Aviso",
        "invalid_url": "Por favor ingresa una URL válida.",
        "success_title": "Éxito",
        "download_complete": "Descarga completada:",
        "error_title": "Error",
        "download_error": "Error en la descarga:",
        "status_downloading": "Descargando... {percent}%",
        "status_canceled": "Descarga cancelada.",
        "size_label_dash": "Peso estimado: -",
        "codec_h264": "H.264 (Más compatible)",
        "codec_vp9": "VP9 (Mejor calidad/peso)",
        "codec_any": "Cualquiera",
        "lang_original": "Original/Cualquiera"
    },
    "en": {
        "app_title": "YouTube Downloader PRO",
        "tab_downloader": "Downloader",
        "tab_search": "Search",
        "downloader_title": "Video Downloader",
        "url_label": "Video URL:",
        "save_label": "Save to:",
        "explore_btn": "Browse...",
        "res_label": "Resolution:",
        "fps_label": "Max FPS:",
        "codec_label": "Video Codec:",
        "lang_label": "Audio Language:",
        "size_label_calculating": "Estimated size: Calculating...",
        "size_label_unknown": "Estimated size: Unknown",
        "size_label_error": "Estimated size: Calculation error",
        "size_label_value": "Estimated size: ~{mb:.1f} MB",
        "status_ready": "Ready to download.",
        "btn_download": "Start Download",
        "btn_cancel": "Cancel",
        "search_placeholder": "Enter a video name to search...",
        "btn_search": "Search",
        "search_results_label": "Search Results",
        "warning_title": "Warning",
        "invalid_url": "Please enter a valid URL.",
        "success_title": "Success",
        "download_complete": "Download complete:",
        "error_title": "Error",
        "download_error": "Download error:",
        "status_downloading": "Downloading... {percent}%",
        "status_canceled": "Download canceled.",
        "size_label_dash": "Estimated size: -",
        "codec_h264": "H.264 (Most compatible)",
        "codec_vp9": "VP9 (Best quality/size)",
        "codec_any": "Any",
        "lang_original": "Original/Any"
    },
    "fr": {
        "app_title": "YouTube Downloader PRO",
        "tab_downloader": "Téléchargeur",
        "tab_search": "Recherche",
        "downloader_title": "Téléchargeur de Vidéos",
        "url_label": "URL de la vidéo:",
        "save_label": "Enregistrer sous:",
        "explore_btn": "Parcourir...",
        "res_label": "Résolution:",
        "fps_label": "FPS Max:",
        "codec_label": "Codec vidéo:",
        "lang_label": "Langue audio:",
        "size_label_calculating": "Taille estimée: Calcul...",
        "size_label_unknown": "Taille estimée: Inconnue",
        "size_label_error": "Taille estimée: Erreur de calcul",
        "size_label_value": "Taille estimée: ~{mb:.1f} Mo",
        "status_ready": "Prêt à télécharger.",
        "btn_download": "Lancer le téléchargement",
        "btn_cancel": "Annuler",
        "search_placeholder": "Entrez le nom d'une vidéo à rechercher...",
        "btn_search": "Chercher",
        "search_results_label": "Résultats de recherche",
        "warning_title": "Avertissement",
        "invalid_url": "Veuillez entrer une URL valide.",
        "success_title": "Succès",
        "download_complete": "Téléchargement terminé:",
        "error_title": "Erreur",
        "download_error": "Erreur de téléchargement:",
        "status_downloading": "Téléchargement... {percent}%",
        "status_canceled": "Téléchargement annulé.",
        "size_label_dash": "Taille estimée: -",
        "codec_h264": "H.264 (Plus compatible)",
        "codec_vp9": "VP9 (Meilleure qualité/taille)",
        "codec_any": "N'importe lequel",
        "lang_original": "Original/N'importe lequel"
    },
    "pt": {
        "app_title": "YouTube Downloader PRO",
        "tab_downloader": "Baixador",
        "tab_search": "Pesquisa",
        "downloader_title": "Baixador de Vídeos",
        "url_label": "URL do Vídeo:",
        "save_label": "Salvar em:",
        "explore_btn": "Procurar...",
        "res_label": "Resolução:",
        "fps_label": "FPS Máx:",
        "codec_label": "Codec de Vídeo:",
        "lang_label": "Idioma do Áudio:",
        "size_label_calculating": "Tamanho estimado: Calculando...",
        "size_label_unknown": "Tamanho estimado: Desconhecido",
        "size_label_error": "Tamanho estimado: Erro ao calcular",
        "size_label_value": "Tamanho estimado: ~{mb:.1f} MB",
        "status_ready": "Pronto para baixar.",
        "btn_download": "Iniciar Download",
        "btn_cancel": "Cancelar",
        "search_placeholder": "Digite o nome de um vídeo para pesquisar...",
        "btn_search": "Pesquisar",
        "search_results_label": "Resultados da Pesquisa",
        "warning_title": "Aviso",
        "invalid_url": "Por favor, insira uma URL válida.",
        "success_title": "Sucesso",
        "download_complete": "Download concluído:",
        "error_title": "Erro",
        "download_error": "Erro de download:",
        "status_downloading": "Baixando... {percent}%",
        "status_canceled": "Download cancelado.",
        "size_label_dash": "Tamanho estimado: -",
        "codec_h264": "H.264 (Mais compatível)",
        "codec_vp9": "VP9 (Melhor qualidade/tamanho)",
        "codec_any": "Qualquer",
        "lang_original": "Original/Qualquer"
    },
    "ru": {
        "app_title": "YouTube Downloader PRO",
        "tab_downloader": "Загрузчик",
        "tab_search": "Поиск",
        "downloader_title": "Загрузчик Видео",
        "url_label": "URL видео:",
        "save_label": "Сохранить в:",
        "explore_btn": "Обзор...",
        "res_label": "Разрешение:",
        "fps_label": "Макс. FPS:",
        "codec_label": "Видео Кодек:",
        "lang_label": "Язык аудио:",
        "size_label_calculating": "Ожидаемый размер: Вычисление...",
        "size_label_unknown": "Ожидаемый размер: Неизвестно",
        "size_label_error": "Ожидаемый размер: Ошибка вычисления",
        "size_label_value": "Ожидаемый размер: ~{mb:.1f} МБ",
        "status_ready": "Готов к загрузке.",
        "btn_download": "Начать загрузку",
        "btn_cancel": "Отмена",
        "search_placeholder": "Введите название видео для поиска...",
        "btn_search": "Искать",
        "search_results_label": "Результаты поиска",
        "warning_title": "Внимание",
        "invalid_url": "Пожалуйста, введите действительный URL.",
        "success_title": "Успех",
        "download_complete": "Загрузка завершена:",
        "error_title": "Ошибка",
        "download_error": "Ошибка загрузки:",
        "status_downloading": "Загрузка... {percent}%",
        "status_canceled": "Загрузка отменена.",
        "size_label_dash": "Ожидаемый размер: -",
        "codec_h264": "H.264 (Наиболее совместимый)",
        "codec_vp9": "VP9 (Лучшее качество/размер)",
        "codec_any": "Любой",
        "lang_original": "Оригинал/Любой"
    }
}

class AppConfig:
    def __init__(self):
        self.config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), CONFIG_FILE)
        self.config = {"language": DEFAULT_LANG}
        self.load()

    def load(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.config.update(data)
            except Exception:
                pass

    def save(self):
        try:
            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(self.config, f, indent=4)
        except Exception:
            pass

    def get_lang(self):
        return self.config.get("language", DEFAULT_LANG)

    def set_lang(self, lang):
        self.config["language"] = lang
        self.save()

    def _(self, key):
        lang = self.get_lang()
        if lang not in TRANSLATIONS:
            lang = DEFAULT_LANG
        return TRANSLATIONS[lang].get(key, key)
