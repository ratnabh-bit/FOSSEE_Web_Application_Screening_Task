"""
Serializers for Equipment Visualizer API
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Dataset, Equipment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    equipment = EquipmentSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_type_distribution', 'equipment'
        ]


class DatasetSummarySerializer(serializers.ModelSerializer):
    """Simplified serializer without equipment details"""
    class Meta:
        model = Dataset
        fields = [
            'id', 'filename', 'uploaded_at', 'total_count',
            'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'equipment_type_distribution'
        ]