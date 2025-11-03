@echo off
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting FastAPI server...
echo.
python -m app.main

