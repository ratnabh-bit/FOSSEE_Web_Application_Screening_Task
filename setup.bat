@echo off
echo =========================================
echo Equipment Visualizer - Quick Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js is not installed. Please install Node.js 14 or higher.
    pause
    exit /b 1
)

echo [+] Python and Node.js found!
echo.

REM Create project structure
echo [*] Creating project structure...
mkdir equipment-visualizer
cd equipment-visualizer
mkdir backend frontend desktop

REM Backend Setup
echo.
echo [*] Setting up Backend...
cd backend

REM Create virtual environment
python -m venv venv

REM Create requirements.txt
(
echo Django==4.2.7
echo djangorestframework==3.14.0
echo django-cors-headers==4.3.1
echo pandas==2.1.3
echo reportlab==4.0.7
echo openpyxl==3.1.2
) > requirements.txt

REM Activate and install
call venv\Scripts\activate.bat
echo [*] Installing backend dependencies...
pip install -r requirements.txt

REM Create Django project
echo [*] Creating Django project...
django-admin startproject equipment_visualizer .
python manage.py startapp api

echo.
echo [+] Backend structure created!
echo [!] Please manually copy the following files:
echo    - settings.py to backend\equipment_visualizer\
echo    - models.py to backend\api\
echo    - serializers.py to backend\api\
echo    - views.py to backend\api\
echo    - urls.py to backend\equipment_visualizer\
echo.
echo Then run:
echo    python manage.py makemigrations
echo    python manage.py migrate
echo    python manage.py runserver
echo.

REM Frontend Setup
cd ..\frontend
echo [*] Setting up Frontend...
echo [*] Creating React app (this may take a few minutes)...
call npx create-react-app . --use-npm

echo [*] Installing frontend dependencies...
call npm install axios chart.js react-chartjs-2

echo.
echo [+] Frontend structure created!
echo [!] Please manually:
echo    - Replace src\App.js with provided code
echo    - Replace src\App.css with provided code
echo    - Update src\index.js
echo.
echo Then run:
echo    npm start
echo.

REM Desktop Setup
cd ..\desktop
echo [*] Setting up Desktop App...

REM Create virtual environment
python -m venv venv

REM Create requirements.txt
(
echo PyQt5==5.15.10
echo matplotlib==3.8.2
echo requests==2.31.0
) > requirements.txt

echo.
echo [+] Desktop structure created!
echo [!] Please:
echo    1. Activate venv: venv\Scripts\activate.bat
echo    2. Install dependencies: pip install -r requirements.txt
echo    3. Create main.py with provided code
echo    4. Run: python main.py
echo.

REM Create sample CSV
cd ..
echo [*] Creating sample CSV file...
(
echo Equipment Name,Type,Flowrate,Pressure,Temperature
echo Pump-1,Pump,120,5.2,110
echo Compressor-1,Compressor,95,8.4,95
echo Valve-1,Valve,60,4.1,105
echo HeatExchanger-1,HeatExchanger,150,6.2,130
echo Pump-2,Pump,132,5.6,118
echo Valve-2,Valve,58,4,108
echo Reactor-1,Reactor,140,7.5,140
echo Pump-3,Pump,125,5.3,115
echo Condenser-1,Condenser,160,6.8,125
echo Compressor-2,Compressor,100,8,98
echo HeatExchanger-2,HeatExchanger,155,6.3,132
echo Valve-3,Valve,62,4.2,107
echo Pump-4,Pump,130,5.9,119
echo Reactor-2,Reactor,145,7.2,138
echo Condenser-2,Condenser,165,6.9,128
) > sample_equipment_data.csv

echo.
echo =========================================
echo [+] Setup Complete!
echo =========================================
echo.
echo Next Steps:
echo.
echo 1. Backend:
echo    cd backend
echo    venv\Scripts\activate.bat
echo    # Copy all backend code files
echo    python manage.py makemigrations
echo    python manage.py migrate
echo    python manage.py runserver
echo.
echo 2. Frontend (new terminal):
echo    cd frontend
echo    # Copy App.js and App.css
echo    npm start
echo.
echo 3. Desktop (new terminal):
echo    cd desktop
echo    venv\Scripts\activate.bat
echo    # Copy main.py
echo    python main.py
echo.
echo Sample CSV created: sample_equipment_data.csv
echo.
echo Don't forget to:
echo    - Record demo video (2-3 minutes)
echo    - Push to GitHub
echo    - Submit at: https://forms.gle/rEgLy6fQU1UgdB5LA
echo.
echo Good luck!
echo.
pause