@echo off

REM Check if virtual environment exists, create if not
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists.
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing/updating dependencies...
python -m pip install -q --upgrade pip
pip install -q -r requirements.txt

echo.
echo Starting FastAPI server...
echo.
python -m app.main
