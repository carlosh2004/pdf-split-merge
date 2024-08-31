@echo off
setlocal

REM Definir el nombre del entorno virtual y el archivo de requisitos
set "VENV_DIR=venv"
set "REQUIREMENTS_FILE=requirements.txt"

REM Verificar si el entorno virtual ya existe
if not exist "%VENV_DIR%\Scripts\python.exe" (
    echo Creando entorno virtual...
    call python -m venv %VENV_DIR%
)

REM Activar el entorno virtual
call %VENV_DIR%\Scripts\activate.bat

REM Instalar los requisitos si el archivo requirements.txt ha cambiado
if exist "%REQUIREMENTS_FILE%" (
    echo Instalando dependencias...
    call pip install --upgrade -r %REQUIREMENTS_FILE%
    call python.exe -m pip install --upgrade pip
) else (
    echo El archivo %REQUIREMENTS_FILE% no se encuentra.
)

REM Ejecutar el script principal
python main.py

endlocal
