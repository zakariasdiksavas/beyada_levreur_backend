from django.urls import path
from . import views

urlpatterns = [
    path('create-sale/', views.create_direct_sale),
    path('update-sale/', views.update_direct_sale),
    path('delete-sale/', views.delete_direct_sale),
    path('get-recent-sale/', views.get_recent_direct_sales),
]
