import PyInstaller.__main__
import sys
import os

if sys.platform != "win32":
    print("This build script is for Windows only.")
    sys.exit(1)

# List of heavy external binaries to bundle
binaries = [
    ('bin/ffmpeg.exe', 'bin'),
    ('bin/ffprobe.exe', 'bin')
]

# Convert binaries list to PyInstaller arguments
binary_args = []
for src, dst in binaries:
    binary_args.extend(['--add-binary', f'{src};{dst}'])

print("Starting PyInstaller compilation...")

PyInstaller.__main__.run([
    'run.py',
    '--name=YouTubeDownloaderPRO',
    '--windowed',
    '--onefile',
    '--clean',
    '--upx-dir=bin',
    
    # Exclude unused libraries to save space
    '--exclude-module=matplotlib',
    '--exclude-module=scipy',
    '--exclude-module=pandas',
    '--exclude-module=numpy',
    '--exclude-module=PyQt5',
    '--exclude-module=PySide2',
    '--exclude-module=unittest',
    '--exclude-module=pydoc',
    '--exclude-module=doctest',
    '--exclude-module=argparse',
    '--exclude-module=tkinter.test',
    
    *binary_args
])

print("Build complete!")
