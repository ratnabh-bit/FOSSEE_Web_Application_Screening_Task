"""
Chemical Equipment Visualizer - Desktop Application
PyQt5 + Matplotlib Desktop Client
"""
import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QLineEdit, QFileDialog, QTableWidget,
    QTableWidgetItem, QMessageBox, QTabWidget, QStackedWidget,
    QListWidget, QListWidgetItem, QGroupBox, QGridLayout
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import json


API_BASE = 'http://localhost:8000/api'


class APIWorker(QThread):
    """Worker thread for API calls"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, func, *args, **kwargs):
        super().__init__()
        self.func = func
        self.args = args
        self.kwargs = kwargs
    
    def run(self):
        try:
            result = self.func(*self.args, **self.kwargs)
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class AuthWidget(QWidget):
    """Authentication Widget"""
    authenticated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        # Title
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Form
        form_layout = QVBoxLayout()
        
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText('Username')
        self.username_input.setMinimumWidth(300)
        form_layout.addWidget(QLabel('Username:'))
        form_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText('Password')
        self.password_input.setEchoMode(QLineEdit.Password)
        form_layout.addWidget(QLabel('Password:'))
        form_layout.addWidget(self.password_input)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText('Email (optional)')
        self.email_input.setVisible(False)
        form_layout.addWidget(QLabel('Email:'))
        form_layout.addWidget(self.email_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        
        self.login_btn = QPushButton('Login')
        self.login_btn.clicked.connect(self.handle_login)
        btn_layout.addWidget(self.login_btn)
        
        self.register_btn = QPushButton('Register')
        self.register_btn.clicked.connect(self.handle_register)
        btn_layout.addWidget(self.register_btn)
        
        form_layout.addLayout(btn_layout)
        
        self.toggle_btn = QPushButton('Switch to Register')
        self.toggle_btn.clicked.connect(self.toggle_mode)
        form_layout.addWidget(self.toggle_btn)
        
        self.status_label = QLabel('')
        self.status_label.setAlignment(Qt.AlignCenter)
        form_layout.addWidget(self.status_label)
        
        layout.addLayout(form_layout)
        self.setLayout(layout)
        
        self.is_register_mode = False
    
    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        if self.is_register_mode:
            self.toggle_btn.setText('Switch to Login')
            self.email_input.setVisible(True)
        else:
            self.toggle_btn.setText('Switch to Register')
            self.email_input.setVisible(False)
    
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            response = requests.post(f'{API_BASE}/login/', json={
                'username': username,
                'password': password
            })
            response.raise_for_status()
            token = response.json()['token']
            self.authenticated.emit(token)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Login failed: {str(e)}')
    
    def handle_register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        email = self.email_input.text()
        
        if not username or not password:
            QMessageBox.warning(self, 'Error', 'Please enter username and password')
            return
        
        try:
            response = requests.post(f'{API_BASE}/register/', json={
                'username': username,
                'password': password,
                'email': email
            })
            response.raise_for_status()
            token = response.json()['token']
            self.authenticated.emit(token)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Registration failed: {str(e)}')


class ChartWidget(QWidget):
    """Widget for displaying matplotlib charts"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure = Figure(figsize=(8, 6))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
    
    def plot_pie(self, data, title):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        labels = list(data.keys())
        values = list(data.values())
        ax.pie(values, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(title)
        self.canvas.draw()
    
    def plot_bar(self, labels, values, title, xlabel, ylabel):
        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(labels, values, color=['#36A2EB', '#FF6384', '#FFCE56'])
        ax.set_title(title)
        ax.set_xlabel(xlabel)
        ax.set_ylabel(ylabel)
        self.canvas.draw()


class MainWidget(QWidget):
    """Main application widget"""
    def __init__(self, token):
        super().__init__()
        self.token = token
        self.datasets = []
        self.selected_dataset = None
        self.init_ui()
        self.load_datasets()
    
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Header
        header = QHBoxLayout()
        title = QLabel('Chemical Equipment Visualizer')
        title.setFont(QFont('Arial', 16, QFont.Bold))
        header.addWidget(title)
        header.addStretch()
        
        logout_btn = QPushButton('Logout')
        logout_btn.clicked.connect(self.logout)
        header.addWidget(logout_btn)
        
        layout.addLayout(header)
        
        # Upload section
        upload_group = QGroupBox('Upload CSV')
        upload_layout = QHBoxLayout()
        
        self.file_label = QLabel('No file selected')
        upload_layout.addWidget(self.file_label)
        
        select_btn = QPushButton('Select File')
        select_btn.clicked.connect(self.select_file)
        upload_layout.addWidget(select_btn)
        
        self.upload_btn = QPushButton('Upload')
        self.upload_btn.clicked.connect(self.upload_file)
        self.upload_btn.setEnabled(False)
        upload_layout.addWidget(self.upload_btn)
        
        upload_group.setLayout(upload_layout)
        layout.addWidget(upload_group)
        
        # Main content
        content = QHBoxLayout()
        
        # Left: Datasets list
        left_panel = QVBoxLayout()
        left_panel.addWidget(QLabel('Dataset History (Last 5)'))
        
        self.dataset_list = QListWidget()
        self.dataset_list.itemClicked.connect(self.load_dataset_details)
        left_panel.addWidget(self.dataset_list)
        
        refresh_btn = QPushButton('Refresh')
        refresh_btn.clicked.connect(self.load_datasets)
        left_panel.addWidget(refresh_btn)
        
        content.addLayout(left_panel, 1)
        
        # Right: Details
        self.tabs = QTabWidget()
        
        # Summary tab
        self.summary_widget = QWidget()
        summary_layout = QVBoxLayout()
        self.summary_labels = QGridLayout()
        summary_layout.addLayout(self.summary_labels)
        summary_layout.addStretch()
        self.summary_widget.setLayout(summary_layout)
        self.tabs.addTab(self.summary_widget, 'Summary')
        
        # Charts tab
        charts_widget = QWidget()
        charts_layout = QVBoxLayout()
        self.pie_chart = ChartWidget()
        self.bar_chart = ChartWidget()
        charts_layout.addWidget(self.pie_chart)
        charts_layout.addWidget(self.bar_chart)
        charts_widget.setLayout(charts_layout)
        self.tabs.addTab(charts_widget, 'Charts')
        
        # Table tab
        self.table_widget = QTableWidget()
        self.tabs.addTab(self.table_widget, 'Equipment Table')
        
        # Actions tab
        actions_widget = QWidget()
        actions_layout = QVBoxLayout()
        
        pdf_btn = QPushButton('Download PDF Report')
        pdf_btn.clicked.connect(self.download_pdf)
        actions_layout.addWidget(pdf_btn)
        
        delete_btn = QPushButton('Delete Dataset')
        delete_btn.clicked.connect(self.delete_dataset)
        actions_layout.addWidget(delete_btn)
        
        actions_layout.addStretch()
        actions_widget.setLayout(actions_layout)
        self.tabs.addTab(actions_widget, 'Actions')
        
        content.addWidget(self.tabs, 2)
        
        layout.addLayout(content)
        self.setLayout(layout)
        
        self.selected_file = None
    
    def select_file(self):
        filename, _ = QFileDialog.getOpenFileName(self, 'Select CSV File', '', 'CSV Files (*.csv)')
        if filename:
            self.selected_file = filename
            self.file_label.setText(filename.split('/')[-1])
            self.upload_btn.setEnabled(True)
    
    def upload_file(self):
        if not self.selected_file:
            return
        
        try:
            with open(self.selected_file, 'rb') as f:
                files = {'file': f}
                headers = {'Authorization': f'Token {self.token}'}
                response = requests.post(f'{API_BASE}/upload/', files=files, headers=headers)
                response.raise_for_status()
            
            QMessageBox.information(self, 'Success', 'File uploaded successfully!')
            self.selected_file = None
            self.file_label.setText('No file selected')
            self.upload_btn.setEnabled(False)
            self.load_datasets()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Upload failed: {str(e)}')
    
    def load_datasets(self):
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE}/datasets/', headers=headers)
            response.raise_for_status()
            self.datasets = response.json()
            
            self.dataset_list.clear()
            for dataset in self.datasets:
                item = QListWidgetItem(f"{dataset['filename']} ({dataset['total_count']} items)")
                item.setData(Qt.UserRole, dataset['id'])
                self.dataset_list.addItem(item)
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load datasets: {str(e)}')
    
    def load_dataset_details(self, item):
        dataset_id = item.data(Qt.UserRole)
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f'{API_BASE}/datasets/{dataset_id}/', headers=headers)
            response.raise_for_status()
            self.selected_dataset = response.json()
            
            self.display_summary()
            self.display_charts()
            self.display_table()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to load dataset: {str(e)}')
    
    def display_summary(self):
        # Clear previous labels
        for i in reversed(range(self.summary_labels.count())):
            self.summary_labels.itemAt(i).widget().setParent(None)
        
        ds = self.selected_dataset
        
        stats = [
            ('Total Count', ds['total_count']),
            ('Avg Flowrate', f"{ds['avg_flowrate']:.2f}"),
            ('Avg Pressure', f"{ds['avg_pressure']:.2f}"),
            ('Avg Temperature', f"{ds['avg_temperature']:.2f}")
        ]
        
        for i, (label, value) in enumerate(stats):
            label_widget = QLabel(f'<b>{label}:</b>')
            value_widget = QLabel(str(value))
            value_widget.setFont(QFont('Arial', 14, QFont.Bold))
            self.summary_labels.addWidget(label_widget, i, 0)
            self.summary_labels.addWidget(value_widget, i, 1)
    
    def display_charts(self):
        ds = self.selected_dataset
        
        # Pie chart - Equipment type distribution
        self.pie_chart.plot_pie(ds['equipment_type_distribution'], 'Equipment Type Distribution')
        
        # Bar chart - Average parameters
        labels = ['Flowrate', 'Pressure', 'Temperature']
        values = [ds['avg_flowrate'], ds['avg_pressure'], ds['avg_temperature']]
        self.bar_chart.plot_bar(labels, values, 'Average Parameters', 'Parameter', 'Value')
    
    def display_table(self):
        equipment = self.selected_dataset['equipment']
        
        self.table_widget.setRowCount(len(equipment))
        self.table_widget.setColumnCount(5)
        self.table_widget.setHorizontalHeaderLabels(['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature'])
        
        for i, eq in enumerate(equipment):
            self.table_widget.setItem(i, 0, QTableWidgetItem(eq['equipment_name']))
            self.table_widget.setItem(i, 1, QTableWidgetItem(eq['equipment_type']))
            self.table_widget.setItem(i, 2, QTableWidgetItem(f"{eq['flowrate']:.1f}"))
            self.table_widget.setItem(i, 3, QTableWidgetItem(f"{eq['pressure']:.1f}"))
            self.table_widget.setItem(i, 4, QTableWidgetItem(f"{eq['temperature']:.1f}"))
        
        self.table_widget.resizeColumnsToContents()
    
    def download_pdf(self):
        if not self.selected_dataset:
            QMessageBox.warning(self, 'Warning', 'Please select a dataset first')
            return
        
        filename, _ = QFileDialog.getSaveFileName(self, 'Save PDF', f"report_{self.selected_dataset['filename']}.pdf", 'PDF Files (*.pdf)')
        if not filename:
            return
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.get(f"{API_BASE}/datasets/{self.selected_dataset['id']}/pdf/", headers=headers)
            response.raise_for_status()
            
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            QMessageBox.information(self, 'Success', 'PDF downloaded successfully!')
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to download PDF: {str(e)}')
    
    def delete_dataset(self):
        if not self.selected_dataset:
            QMessageBox.warning(self, 'Warning', 'Please select a dataset first')
            return
        
        reply = QMessageBox.question(self, 'Confirm', 'Are you sure you want to delete this dataset?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.No:
            return
        
        try:
            headers = {'Authorization': f'Token {self.token}'}
            response = requests.delete(f"{API_BASE}/datasets/{self.selected_dataset['id']}/delete/", headers=headers)
            response.raise_for_status()
            
            QMessageBox.information(self, 'Success', 'Dataset deleted successfully!')
            self.selected_dataset = None
            self.load_datasets()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Failed to delete dataset: {str(e)}')
    
    def logout(self):
        self.close()
        QApplication.quit()


class MainWindow(QMainWindow):
    """Main application window"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chemical Equipment Visualizer')
        self.setGeometry(100, 100, 1200, 800)
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Auth widget
        self.auth_widget = AuthWidget()
        self.auth_widget.authenticated.connect(self.on_authenticated)
        self.stacked_widget.addWidget(self.auth_widget)
        
    def on_authenticated(self, token):
        self.main_widget = MainWidget(token)
        self.stacked_widget.addWidget(self.main_widget)
        self.stacked_widget.setCurrentWidget(self.main_widget)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()