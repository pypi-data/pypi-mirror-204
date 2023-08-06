@echo off

rem Change the current working directory to the directory of the batch script
cd /d %~dp0

rem Check if Python is installed
python --version > nul 2>&1
if errorlevel 1 (
    echo Python needs to be installed for this script to work
    pause
    exit /b 1
)

rem Check if .venv folder exists
if not exist .venv (

    echo Virtual environment not found. Creating a new virtual environment.
    rem Create a virtual environment in .venv
    python -m venv .venv
    rem Activate the virtual environment
    call .venv\Scripts\activate.bat

    echo Installing dependencies
    rem Install flit and the project dependencies
    pip install flit
    flit install --pth-file

    deactivate

)

echo Activating virtual environment

rem Activate the virtual environment
call .venv\Scripts\activate.bat

rem Run the streamlit app
python -m streamlit run About.py