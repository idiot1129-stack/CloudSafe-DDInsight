@echo off

call .venv\Scripts\activate

python -m PyInstaller ^
--onefile ^
--windowed ^
--name DDInsightPro ^
app.py

pause