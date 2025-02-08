from django.urls import path
from . import views


urlpatterns = [
    path('create-eleveur/', views.create_eleveur),
    path('update-eleveur/', views.update_eleveur),
    path('delete-eleveur/', views.delete_eleveur),
    path('list-eleveurs/', views.list_eleveurs),
    
    path('create-batiment/', views.create_batiemnt),
    path('update-batiment/', views.update_batiment),
    path('delete-batiment/', views.delete_batiment),
    path('list-batiments/', views.list_batiments),
    
    path('create-site/', views.create_site),
    path('update-site/', views.update_site),
    path('delete-site/', views.delete_site),
    path('list-sites/', views.list_sites),
    
    path('create-client/', views.create_client),
    path('update-client/', views.update_client),
    path('delete-client/', views.delete_client),
    path('list-clients/', views.list_clients),
    
    path('bind-client-to-batiment/', views.bind_client_to_batiment),
    path('get-clients-with-binded-batiments/', views.get_batiments_with_binded_clients),
    
    path('get-select-options/', views.get_select_options),
    path('get-clients-select-options/', views.get_client_select_options),
]
