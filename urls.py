"""
URL Configuration for Equipment Visualizer
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # Authentication
    path('api/register/', views.register, name='register'),
    path('api/login/', views.login, name='login'),
    
    # Dataset operations
    path('api/upload/', views.upload_csv, name='sample_equipment_data'),
    path('api/datasets/', views.get_datasets, name='get_datasets'),
    path('api/datasets/<int:dataset_id>/', views.get_dataset_detail, name='dataset_detail'),
    path('api/datasets/<int:dataset_id>/pdf/', views.generate_pdf, name='generate_pdf'),
    path('api/datasets/<int:dataset_id>/delete/', views.delete_dataset, name='delete_dataset'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)