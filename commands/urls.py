from django.urls import path
from . import views

urlpatterns = [
    path('create-command/', views.create_command),
    path('update-command/', views.update_command),
    path('delete-command/', views.delete_command),
    path('get-recent-commands/', views.get_recent_commands),
    path('make-command-dilevery/', views.make_command_dilevery),
    path('select-command/', views.select_command_no_delivery),

]
