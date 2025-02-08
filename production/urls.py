from django.urls import path
from . import views

urlpatterns = [
    path('add-production/', views.add_production, name='production'),
    path('update-production/', views.update_production, name='production'),
    path('delete-production/', views.delete_production, name='production'),
    path('get-production/', views.get_productions, name='production'),
    
    path('get-stock/', views.get_stock),
    path('get-stock-client/', views.get_stock_by_client),
]
