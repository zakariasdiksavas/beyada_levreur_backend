from django.urls import path
from . import views

urlpatterns = [
    path('add-command-paiement/', views.create_command_paiement),
    path('update-command-paiement/', views.update_command_paiement),
    path('delete-command-paiement/', views.delete_command_paiement),
    path('get-command-paiements/', views.get_command_paiements),
    
    path('create-client-paiement/', views.create_client_paiement),
    path('update-client-paiement/', views.update_client_paiement),
    path('delete-client-paiement/', views.delete_client_paiement),
    path('get-client-paiements/', views.get_client_paiements),
    
    path('create-direct-sale-paiement/', views.create_direct_sale_paiement),
    path('update-direct-sale-paiement/', views.update_direct_sale_paiement),
    path('delete-direct-sale-paiement/', views.delete_direct_sale_paiement),
    path('get-direct-sale-paiement/', views.get_direct_sale_paiements),
    
    path('add-paiement-try/', views.add_paiement_try),
    path('update-paiement-try/', views.update_paiement_try),
    path('delete-paiement-try/', views.delete_paiement_try),
    path('get-paiement-tries/', views.get_paiement_tries),
    path('update-paiement-status/', views.update_paiment_status),
    
    # ADD PAYMENT PROOF HERE
    path('add-paiement-proof/', views.add_payment_try_proof),
    path('update-paiement-proof/', views.update_payment_try_proof),
    path('delete-paiement-proof/', views.delete_payment_try_proof),

    
    path('get-client-solde/', views.get_client_solde),
    path('get-all-client-solde/', views.get_all_clients_soldes),
]
