import os
import re
from pathlib import Path

def clean_text(text):
    """Remove ANSI escape sequences from text."""
    if not text:
        return ""
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text).strip()

def get_default_downloads_folder():
    """Get the path to the system's default Downloads folder."""
    try:
        # Cross-platform way to get the default downloads folder
        downloads_path = str(Path.home() / "Downloads")
        if os.path.exists(downloads_path):
            return downloads_path
    except Exception:
        pass
    
    # Fallback to local 'downloads' folder
    fallback = os.path.join(os.getcwd(), 'downloads')
    if not os.path.exists(fallback):
        os.makedirs(fallback)
    return fallback
