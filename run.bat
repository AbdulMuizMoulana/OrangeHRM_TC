@echo off
echo -----------------------------------------------------
echo       Running Python Pytest Automation (HEADLESS)
echo -----------------------------------------------------

set HEADLESS=true

IF EXIST venv\Scripts\activate (
    echo Activating virtual environment...
    call venv\Scripts\activate
)

echo Installing dependencies...
pip install -r requirements.txt

echo Running Pytest...
pytest -v --disable-warnings --html=Reports/report.html --self-contained-html

echo -----------------------------------------------------
echo           TEST EXECUTION COMPLETED
echo -----------------------------------------------------
pause
