# Chemical Equipment Parameter Visualizer
## Hybrid Web + Desktop Application

A full-stack application for visualizing and analyzing chemical equipment parameters with both web and desktop interfaces.

## 🎯 Features

- ✅ CSV file upload and parsing
- ✅ Data visualization with charts (Pie, Bar)
- ✅ Summary statistics (count, averages, type distribution)
- ✅ History management (last 5 datasets)
- ✅ PDF report generation
- ✅ User authentication (Register/Login)
- ✅ Both Web (React) and Desktop (PyQt5) frontends
- ✅ Common Django REST API backend

## 📋 Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend (Web) | React.js + Chart.js | Interactive web interface |
| Frontend (Desktop) | PyQt5 + Matplotlib | Desktop application |
| Backend | Django + DRF | REST API server |
| Data Handling | Pandas | CSV processing & analytics |
| Database | SQLite | Dataset storage |
| Reports | ReportLab | PDF generation |

## 📁 Project Structure

```
equipment-visualizer/
├── backend/
│   ├── equipment_visualizer/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── admin.py
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── index.js
│   └── package.json
├── desktop/
│   ├── main.py
│   └── requirements.txt
├── sample_equipment_data.csv
└── README.md
```

## 🚀 Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm or yarn

### 1. Backend Setup (Django)

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create Django project structure
django-admin startproject equipment_visualizer .
python manage.py startapp api

# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

The backend will run on `http://localhost:8000`

### 2. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd frontend

# Create React app (if starting fresh)
npx create-react-app .

# Install dependencies
npm install

# Start development server
npm start
```

The web app will open at `http://localhost:3000`

### 3. Desktop App Setup (PyQt5)

```bash
# Navigate to desktop directory
cd desktop

# Create virtual environment (if not already created)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run desktop application
python main.py
```

## 📝 Usage

### Web Application

1. **Register/Login**: Create an account or login
2. **Upload CSV**: Select and upload a CSV file with equipment data
3. **View Data**: Browse through your dataset history
4. **Visualize**: View charts and statistics
5. **Export**: Download PDF reports
6. **Manage**: Delete old datasets

### Desktop Application

1. **Launch**: Run `python main.py`
2. **Authenticate**: Login with your credentials
3. **Upload**: Select CSV file and upload
4. **Explore**: Switch between tabs (Summary, Charts, Table, Actions)
5. **Export**: Download PDF reports
6. **Manage**: Delete datasets

## 📊 CSV Format

Your CSV file should have the following columns:

| Column Name | Type | Description |
|-------------|------|-------------|
| Equipment Name | String | Name of the equipment |
| Type | String | Equipment type (Pump, Valve, etc.) |
| Flowrate | Float | Flow rate value |
| Pressure | Float | Pressure value |
| Temperature | Float | Temperature value |

### Sample Data

```csv
Equipment Name,Type,Flowrate,Pressure,Temperature
Pump-1,Pump,120,5.2,110
Compressor-1,Compressor,95,8.4,95
Valve-1,Valve,60,4.1,105
```

## 🔐 Authentication

The application uses Token-based authentication:

- Register a new user via `/api/register/`
- Login via `/api/login/`
- Token is stored and used for subsequent API requests

## 🔌 API Endpoints

### Authentication
- `POST /api/register/` - Register new user
- `POST /api/login/` - Login user

### Datasets
- `POST /api/upload/` - Upload CSV file
- `GET /api/datasets/` - Get all datasets
- `GET /api/datasets/<id>/` - Get dataset details
- `GET /api/datasets/<id>/pdf/` - Download PDF report
- `DELETE /api/datasets/<id>/delete/` - Delete dataset

## 🎨 Features Explained

### 1. CSV Upload & Parsing
- Robust CSV parsing with Pandas
- Whitespace handling
- Missing value detection
- Column validation

### 2. Data Analytics
- Total equipment count
- Average flowrate, pressure, temperature
- Equipment type distribution
- Statistical summaries

### 3. Visualization
- **Web**: Interactive Chart.js charts
- **Desktop**: Matplotlib charts
- Pie charts for distribution
- Bar charts for comparisons

### 4. History Management
- Stores last 5 datasets per user
- Auto-deletion of older datasets
- Quick access to recent uploads

### 5. PDF Reports
- Professional report generation
- Summary statistics
- Equipment type distribution
- Detailed equipment table

## 🛠️ Development

### Running Tests

```bash
# Backend tests
cd backend
python manage.py test

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Frontend build
cd frontend
npm run build

# Deploy static files
cd ../backend
python manage.py collectstatic
```

## 📦 Dependencies

### Backend
- Django 4.2.7
- Django REST Framework 3.14.0
- django-cors-headers 4.3.1
- pandas 2.1.3
- reportlab 4.0.7

### Frontend
- React 18.2.0
- axios 1.6.2
- chart.js 4.4.0
- react-chartjs-2 5.2.0

### Desktop
- PyQt5 5.15.10
- matplotlib 3.8.2
- requests 2.31.0

## 🎥 Demo Video

Create a 2-3 minute demo video showing:
1. User registration/login
2. CSV file upload
3. Data visualization (both web and desktop)
4. PDF report generation
5. Dataset management

## 🚀 Deployment

### Web Deployment (Optional)

Deploy on platforms like:
- **Heroku**: Backend + Frontend
- **Vercel**: Frontend only
- **Railway**: Full stack
- **PythonAnywhere**: Backend only

## 🤝 Contributing

This is an internship screening task project. For the actual submission:

1. Push code to GitHub repository
2. Include this README
3. Create demo video (2-3 minutes)
4. Submit via: https://forms.gle/rEgLy6fQU1UgdB5LA

## 📄 License

This project is created for FOSSEE Internship screening purposes.

## 👤 Author

Ratnabh Asati
FOSSEE Internship Applicant

## 📧 Contact

For questions or issues, contact: [Your Email]

---

**Note**: Make sure both Django backend (port 8000) and React frontend (port 3000) are running simultaneously for the web application to work properly. The desktop app only needs the Django backend running.

