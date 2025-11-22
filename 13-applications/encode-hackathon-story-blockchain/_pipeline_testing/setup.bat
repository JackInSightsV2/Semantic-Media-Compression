@echo off
REM Setup script for argumentative essay distillation

echo Creating virtual environment...
python -m venv .venv

echo.
echo Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Setup complete!
echo.
echo Next steps:
echo   1. Create .env file with: OPENROUTER_KEY=your_key_here
echo   2. Place a PDF file in the 'data' folder
echo   3. Run: python distill_essay.py
echo.

pause

