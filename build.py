import sys
import subprocess

# Build configuration
args = [
    sys.executable, '-m', 'PyInstaller',
    'app/main.py',
    '--onefile',
    '--windowed',
    '--name=SubtitleOverlay',
    '--icon=icon.ico',
    '--add-data=app:app',
    '--hidden-import=websockets',
    '--hidden-import=PyQt6',
]

if __name__ == '__main__':
    subprocess.run(args, check=True)