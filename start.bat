@echo off
setlocal

REM Check for Python 3
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not found in PATH.
    echo Please install Python 3 and ensure it's added to your PATH.
    goto :error_exit
)

python --version 2>&1 | findstr /C:"Python 3" >nul
if %errorlevel% neq 0 (
    echo Error: Python 3 is required. The installed version is not Python 3.
    echo Please install Python 3.
    goto :error_exit
)
echo Python 3 found.

REM Virtual Environment
if not exist "venv" (
    echo Creating Python 3 virtual environment 'venv'...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo Error: Failed to create virtual environment.
        goto :error_exit
    )
    echo Virtual environment 'venv' created.
) else (
    echo Virtual environment 'venv' already exists.
)

REM Activate Virtual Environment
echo Activating virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo Error: venv\Scripts\activate.bat not found. Cannot activate virtual environment.
    goto :error_exit
)
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo Error: Failed to activate virtual environment.
    goto :error_exit
)
echo Virtual environment activated.

REM Install Dependencies
echo Installing dependencies from requirements.txt...
if not exist "requirements.txt" (
    echo Error: requirements.txt not found.
    call :deactivate_and_exit
)
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error: Failed to install dependencies.
    call :deactivate_and_exit
)
echo Dependencies installed successfully or were already up-to-date.

REM Start Application
echo Starting Docling-webui.py...
REM The 'start' command launches the Python script in a new window, allowing the batch script to continue.
start "Docling WebUI" python Docling-webui.py
if %errorlevel% neq 0 (
    echo Error: Failed to start Docling-webui.py.
    call :deactivate_and_exit
)
echo Docling-webui.py is starting. Check its console output for the exact URL and port.

REM Open Browser
echo Waiting for the server to start...
timeout /t 5 /nobreak >nul

echo Attempting to open http://localhost:7860 in your browser.
echo Please check the console output from Docling-webui.py for the actual address if it's different.
start http://localhost:7860

echo Script finished. The application should be running.
goto :cleanup

:deactivate_and_exit
REM This label is for deactivating venv if it was activated, then exiting.
echo Deactivating virtual environment due to an error...
if defined VIRTUAL_ENV (
    call venv\Scripts\deactivate.bat
)
goto :error_exit

:error_exit
echo Script terminated due to an error.
call :cleanup_exit

:cleanup
REM Clean up and exit script
if defined VIRTUAL_ENV (
    REM Deactivate if the script is ending normally and venv is active
    REM This might not be strictly necessary as the parent cmd prompt will not be affected by 'call activate'
    REM but it's good practice for scripts that might be sourced or have other side effects.
    REM However, for a simple launcher, it might be better to leave the venv active if the user ran the script directly in their cmd.
    REM For now, we'll assume the primary purpose is launching the app, so we won't explicitly deactivate here on normal exit.
    echo Virtual environment is still active in this window if you ran the script directly.
)
endlocal
exit /b 0

:cleanup_exit
endlocal
exit /b 1
