#!/bin/bash

# Quick Setup Script for Equipment Visualizer Project
# FOSSEE Internship Task

echo "========================================="
echo "Equipment Visualizer - Quick Setup"
echo "========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

echo "✅ Python and Node.js found!"
echo ""

# Create project structure
echo "📁 Creating project structure..."
mkdir -p equipment-visualizer/{backend,frontend,desktop}
cd equipment-visualizer

# Backend Setup
echo ""
echo "🔧 Setting up Backend..."
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Create requirements.txt
cat > requirements.txt << 'EOF'
Django==4.2.7
djangorestframework==3.14.0
django-cors-headers==4.3.1
pandas==2.1.3
reportlab==4.0.7
openpyxl==3.1.2
EOF

# Install dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Create Django project
echo "🚀 Creating Django project..."
django-admin startproject equipment_visualizer .
python manage.py startapp api

echo ""
echo "✅ Backend structure created!"
echo "⚠️  Please manually copy the following files:"
echo "   - settings.py to backend/equipment_visualizer/"
echo "   - models.py to backend/api/"
echo "   - serializers.py to backend/api/"
echo "   - views.py to backend/api/"
echo "   - urls.py to backend/equipment_visualizer/"
echo ""
echo "Then run:"
echo "   python manage.py makemigrations"
echo "   python manage.py migrate"
echo "   python manage.py runserver"
echo ""

# Frontend Setup
cd ../frontend
echo "🔧 Setting up Frontend..."

# Create React app
echo "📦 Creating React app (this may take a few minutes)..."
npx create-react-app . --use-npm

# Install additional dependencies
echo "📦 Installing frontend dependencies..."
npm install axios chart.js react-chartjs-2

echo ""
echo "✅ Frontend structure created!"
echo "⚠️  Please manually:"
echo "   - Replace src/App.js with provided code"
echo "   - Replace src/App.css with provided code"
echo "   - Update src/index.js"
echo ""
echo "Then run:"
echo "   npm start"
echo ""

# Desktop Setup
cd ../desktop
echo "🔧 Setting up Desktop App..."

# Create virtual environment
python3 -m venv venv

# Create requirements.txt
cat > requirements.txt << 'EOF'
PyQt5==5.15.10
matplotlib==3.8.2
requests==2.31.0
EOF

echo ""
echo "✅ Desktop structure created!"
echo "⚠️  Please:"
echo "   1. Activate venv: source venv/bin/activate (or venv\\Scripts\\activate on Windows)"
echo "   2. Install dependencies: pip install -r requirements.txt"
echo "   3. Create main.py with provided code"
echo "   4. Run: python main.py"
echo ""

# Create sample CSV
cd ..
echo "📄 Creating sample CSV file..."
cat > sample_equipment_data.csv << 'EOF'
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
HeatExchanger-1,HeatExchanger,150,6.2,130
Pump-2,Pump,132,5.6,118
Valve-2,Valve,58,4,108
Reactor-1,Reactor,140,7.5,140
Pump-3,Pump,125,5.3,115
Condenser-1,Condenser,160,6.8,125
Compressor-2,Compressor,100,8,98
HeatExchanger-2,HeatExchanger,155,6.3,132
Valve-3,Valve,62,4.2,107
Pump-4,Pump,130,5.9,119
Reactor-2,Reactor,145,7.2,138
Condenser-2,Condenser,165,6.9,128
EOF

echo ""
echo "========================================="
echo "✅ Setup Complete!"
echo "========================================="
echo ""
echo "📋 Next Steps:"
echo ""
echo "1. Backend:"
echo "   cd backend"
echo "   source venv/bin/activate  # or venv\\Scripts\\activate on Windows"
echo "   # Copy all backend code files"
echo "   python manage.py makemigrations"
echo "   python manage.py migrate"
echo "   python manage.py runserver"
echo ""
echo "2. Frontend (new terminal):"
echo "   cd frontend"
echo "   # Copy App.js and App.css"
echo "   npm start"
echo ""
echo "3. Desktop (new terminal):"
echo "   cd desktop"
echo "   source venv/bin/activate"
echo "   # Copy main.py"
echo "   python main.py"
echo ""
echo "📝 Sample CSV created: sample_equipment_data.csv"
echo 