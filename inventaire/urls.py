from django.urls import path
from . import views

urlpatterns = [
    path('list-inventaire', views.list_inventaire),
    path('create-inventaire', views.add_inventaire),
    path('update-inventaire', views.update_inventaire),
    path('delete-inventaire', views.delete_inventaire),

]