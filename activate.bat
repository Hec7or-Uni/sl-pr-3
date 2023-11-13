@echo off

rem Nombre del entorno virtual
set nombre_entorno=p3_enviroment

rem Crear el entorno virtual
python -m venv %nombre_entorno%

rem Activar el entorno virtual
call %nombre_entorno%\Scripts\activate

rem Instalar paquetes (puedes agregar más paquetes según tus necesidades)
pip install -r requirements.txt

rem Pausa para mantener la ventana abierta (opcional)
pause
