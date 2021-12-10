rmdir /s /q __pycache__
rmdir /s /q build
rmdir /s /q dist
pyinstaller main.py --onefile --noconsole
ren dist\\main.exe ronove.exe