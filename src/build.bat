call venv\Scripts\activate & ^
rmdir /s /q __pycache__ & ^
rmdir /s /q build & ^
rmdir /s /q dist & ^
pyinstaller main.py --onefile --noconsole --collect-all tkinterdnd2 & ^
ren dist\main.exe ronove.exe