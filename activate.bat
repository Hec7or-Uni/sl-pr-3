@echo off
setlocal

echo Preparando entorno, por favor espere

:: Ruta completa a tu requirements.txt
set REQ_PATH=.

:: Ruta donde se creará el entorno virtual
set VENV_PATH=.\env

:: Ruta al pip del entorno virtual
set PIP="%VENV_PATH%\Scripts\pip.exe"


:: Crear el entorno virtual
echo Creando entorno virtual en %VENV_PATH% ...
python -m venv "%VENV_PATH%"

:: Activar el entorno virtual
echo Entorno virtual creado ...
call "%VENV_PATH%\Scripts\activate.bat"

:: Instalar las dependencias de tu aplicación
echo Instalando dependencias ...
%PIP% install -r "%REQ_PATH%\requirements.txt" > nul 2>&1

endlocal