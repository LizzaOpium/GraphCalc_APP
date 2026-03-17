@echo off
echo Устанавливаю зависимости...
pip install -r requirements.txt

echo Собираю GraphCalc.exe...
pyinstaller ^
  --onefile ^
  --windowed ^
  --name=GraphCalc ^
  --add-data "core;core" ^
  --add-data "ui;ui" ^
  main.py

echo.
echo Готово! Файл: dist\GraphCalc.exe
pause
