from django.urls import path
from .import views

urlpatterns = [
    path('create-charge/', views.create_charge),
    path('update-charge/', views.update_charge),
    path('delete-charge/', views.delete_charge),
    path('get-single-charge/', views.get_single_charge),
    path('get-charges-by-commands/', views.get_charges_by_command),
]
