"""
Models for Equipment Visualizer API
"""
from django.db import models
from django.contrib.auth.models import User
import os
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FOSSEE.settings')

if not settings.configured:
    settings.configure()

class Dataset(models.Model):
    """Store uploaded datasets"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    total_count = models.IntegerField()
    avg_flowrate = models.FloatField()
    avg_pressure = models.FloatField()
    avg_temperature = models.FloatField()
    equipment_type_distribution = models.JSONField()
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"


class Equipment(models.Model):
    """Store individual equipment records"""
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')
    equipment_name = models.CharField(max_length=255)
    equipment_type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    
    def __str__(self):
        return self.equipment_name