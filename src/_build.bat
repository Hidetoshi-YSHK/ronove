call venv\Scripts\activate & ^
rmdir /s /q __pycache__ & ^
rmdir /s /q build & ^
rmdir /s /q dist & ^
del ronove.spec & ^
pyinstaller ^
    main.py ^
    --name ronove ^
    --onefile ^
    --collect-all tkinterdnd2 & ^
python _edit_spec_file.py & ^
pyinstaller ronove.spec
