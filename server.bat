@echo off

python main.py
echo "main.py finished"

python replace.py
echo "replace.py finished"

python stats.py
echo "stats.py finished"

rem Set the browser variable to the path to Firefox if available
set BROWSER=
set FF_PATH=C:\Program Files\Mozilla Firefox\firefox.exe
if exist "%FF_PATH%" set BROWSER="%FF_PATH%"

rem Open the URL in Firefox if available, or Chrome if not
if not %BROWSER% == "" (
  %BROWSER% "http://localhost:8000/script.html"
) else (
  start chrome "http://localhost:8000/script.html"
)

rem Start the Python HTTP server
python -m http.server
