"""
Views for Equipment Visualizer API
"""
import pandas as pd
import io
from django.conf import settings
from django.http import HttpResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from .models import Dataset, Equipment
from .serializers import DatasetSerializer, DatasetSummarySerializer, UserSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user"""
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=400)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    
    user = User.objects.create_user(username=username, password=password, email=email)
    token, _ = Token.objects.get_or_create(user=user)
    
    return Response({
        'token': token.key,
        'user': UserSerializer(user).data
    }, status=201)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    """Login user and return token"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    if user:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(user).data
        })
    
    return Response({'error': 'Invalid credentials'}, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=400)
    
    file = request.FILES['file']
    
    try:
        # Read CSV
        df = pd.read_csv(file)
        
        # Strip whitespace from column names
        df.columns = df.columns.str.strip()
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return Response({
                'error': f'Missing columns: {", ".join(missing_columns)}',
                'available_columns': list(df.columns)
            }, status=400)
        
        # Handle potential undefined values
        df = df.dropna(subset=required_columns)
        
        # Calculate statistics
        total_count = len(df)
        avg_flowrate = float(df['Flowrate'].mean())
        avg_pressure = float(df['Pressure'].mean())
        avg_temperature = float(df['Temperature'].mean())
        
        # Equipment type distribution using lodash-style groupby
        type_counts = df['Type'].value_counts().to_dict()
        equipment_type_distribution = {str(k): int(v) for k, v in type_counts.items()}
        
        # Create dataset
        dataset = Dataset.objects.create(
            user=request.user,
            filename=file.name,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature,
            equipment_type_distribution=equipment_type_distribution
        )
        
        # Create equipment records
        equipment_list = []
        for _, row in df.iterrows():
            equipment_list.append(Equipment(
                dataset=dataset,
                equipment_name=str(row['Equipment Name']),
                equipment_type=str(row['Type']),
                flowrate=float(row['Flowrate']),
                pressure=float(row['Pressure']),
                temperature=float(row['Temperature'])
            ))
        
        Equipment.objects.bulk_create(equipment_list)
        
        # Maintain only last 5 datasets
        user_datasets = Dataset.objects.filter(user=request.user)
        if user_datasets.count() > settings.MAX_DATASETS:
            old_datasets = user_datasets[settings.MAX_DATASETS:]
            for old_dataset in old_datasets:
                old_dataset.delete()
        
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data, status=201)
    
    except Exception as e:
        return Response({'error': str(e)}, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_datasets(request):
    """Get all datasets for current user"""
    datasets = Dataset.objects.filter(user=request.user)
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_dataset_detail(request, dataset_id):
    """Get detailed dataset with equipment"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def generate_pdf(request, dataset_id):
    """Generate PDF report for dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        
        # Create PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{dataset.filename}.pdf"'
        
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        title = Paragraph(f"Equipment Analysis Report - {dataset.filename}", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 12))
        
        # Summary Statistics
        summary_text = f"""
        <b>Summary Statistics</b><br/>
        Total Equipment: {dataset.total_count}<br/>
        Average Flowrate: {dataset.avg_flowrate:.2f}<br/>
        Average Pressure: {dataset.avg_pressure:.2f}<br/>
        Average Temperature: {dataset.avg_temperature:.2f}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Equipment Type Distribution
        dist_text = "<b>Equipment Type Distribution:</b><br/>"
        for equip_type, count in dataset.equipment_type_distribution.items():
            dist_text += f"{equip_type}: {count}<br/>"
        elements.append(Paragraph(dist_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Equipment Table
        equipment = dataset.equipment.all()[:20]  # Limit to first 20
        table_data = [['Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']]
        for eq in equipment:
            table_data.append([
                eq.equipment_name,
                eq.equipment_type,
                f"{eq.flowrate:.1f}",
                f"{eq.pressure:.1f}",
                f"{eq.temperature:.1f}"
            ])
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        return response
        
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_dataset(request, dataset_id):
    """Delete a dataset"""
    try:
        dataset = Dataset.objects.get(id=dataset_id, user=request.user)
        dataset.delete()
        return Response({'message': 'Dataset deleted'}, status=204)
    except Dataset.DoesNotExist:
        return Response({'error': 'Dataset not found'}, status=404)