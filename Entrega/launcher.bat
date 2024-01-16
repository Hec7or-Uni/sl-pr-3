@echo off
setlocal

:: Verificar si Python está instalado
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python no está instalado. Por favor, instale Python antes de continuar.
    pause
    exit /b 1
)

echo Preparando entorno, por favor espere

:: Ruta completa a tu requirements.txt
set REQ_PATH=.\BuscaTuVideojuego

:: Ruta donde se creará el entorno virtual
set VENV_PATH=.\env

:: Ruta al pip del entorno virtual
set PIP="%VENV_PATH%\Scripts\pip.exe"


:: Crear el entorno virtual
echo Creando entorno virtual en %VENV_PATH% si es necesario ...
python -m venv "%VENV_PATH%"

:: Activar el entorno virtual
echo Activando entorno virtual ...
call "%VENV_PATH%\Scripts\activate.bat"

:: Instalar las dependencias de tu aplicación
echo Instalando dependencias si es necesario ...
%PIP% install -r "%REQ_PATH%\requirements.txt" > nul 2>&1

:: Preparando la configuración rápida
echo Perparando la configuracion para un entorno rápido
echo Copia el contenido del fichero COPIAR.txt
timeout /nobreak /t 2 >nul
start notepad.exe ".\BuscaTuVideojuego\COPIAR.txt"
pause
echo Abriendo fichero donde hay que copiar el contenido de COPIAR.txt... (Acuerdate de guardar el fichero)
timeout /nobreak /t 2 >nul
cd BuscaTuVideojuego\Database-MSDOS\DOSBox-0.74
DOSBox.exe -editconf notepad.exe -editconf %SystemRoot%\system32\notepad.exe -editconf %WINDIR%\notepad.exe
pause
taskkill /IM notepad.exe /F

:: Ejecutar la aplicación Flask y esperar a que termine 
cd ..\..
echo Lanzando Busca tu videojuego ...
start /wait python ".\app.py"
taskkill /IM DOSBox.exe /F

endlocal