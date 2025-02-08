from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Sum, Case, When, IntegerField
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments
from .functions import *
from base.models import Client
from . import helpers

# Create your views here.

# -------- PAIEMENTS BY COMMANDS --------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_command_paiement(request):
    """
    commande -- id of the command
    amount -- amount of the paiement
    paiement_mode -- int field (1: espese, 2: chèque, 3: LCN)
    date -- date
    """
    data = request.data
    commande = get_object_or_404(Commande, pk=request.data.get("commande"))
    serializer = PaiementByCommandSerializer(data=data)
    response = {}
    if serializer.is_valid():
        serializer.save()
        
        # Add paiement_try
        pay_data = {
                    "amount": data.get("amount", 0),
                    "paiement_mode": data.get("paiement_mode", 1),
                    "status": data.get("status", 1),
                    "paiement_by_command": serializer.data.get("id"),
                    "client": commande.client.id,
                    "date": data.get("date", 0),
                    }
        pay_serializer = PaiementTrySerializer(data=pay_data)
        if pay_serializer.is_valid():
            pay_serializer.save()
            response.update(serializer.data)
            response.update(pay_serializer.data)
            response["id"] = serializer.data["id"]
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_command_paiement(request):
    """
    id -- id of the paiement
    """
    paiement = get_object_or_404(PaiementByCommand, id=request.data.get('id'))
    serializer = PaiementByCommandSerializer(instance=paiement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_command_paiement(request):
    """
    id -- id of the paiement
    """
    paiement = get_object_or_404(PaiementByCommand, id=request.data.get('id'))
    paiement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_command_paiements(request):
    """
    commande -- id of the commande
    """
    commande = request.GET.get("commande")
    paiements = PaiementByCommand.objects.filter(commande=commande)
    serializer = PaiementByCommandSerializer(paiements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# -------- PAIEMENTS BY CLIENTS --------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client_paiement(request):
    """
    client -- id of the client
    amount -- amount of the paiement
    paiement_mode -- int field (1: espese, 2: chèque, 3: LCN)
    """
    data = request.data
    serializer = PaiementByClientSerializer(data=data)
    response = {}
    if serializer.is_valid():
        serializer.save()
        
        # Add paiement_try
        pay_data = {
                    "amount": data.get("amount", 0),
                    "paiement_mode": data.get("paiement_mode", 1),
                    "paiement_by_client": serializer.data.get("id"),
                    "client": request.data.get("client"),
                    }
        pay_serializer = PaiementTrySerializer(data=pay_data)
        if pay_serializer.is_valid():
            pay_serializer.save()
            
            response.update(serializer.data)
            response.update(pay_serializer.data)
            response["id"] = serializer.data.get("id") #update id field with direct sale paiement
            
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client_paiement(request):
    
    paiement = get_object_or_404(PaiementByClient, id=request.data.get('id'))
    serializer = PaiementByClientSerializer(instance=paiement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client_paiement(request):
    paiement = get_object_or_404(PaiementByClient, id=request.data.get('id'))
    paiement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_paiements(request):
    last_date = request.GET.get('last_date', None)
    client = request.GET.get("client")
    
    if last_date:
        paiements = PaiementByClient.objects.filter(client=client, date__lt=last_date).order_by('-id')[:10]
    else:
        paiements = PaiementByClient.objects.filter(client=client).order_by('-id')[:10]

    serializer = PaiementByClientSerializer(paiements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


# -------- PAIEMENTS BY DIRECT SALES --------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_direct_sale_paiement(request):
    """
    direct_sale -- id of the direct sale
    amount -- int : amount paid in MAD
    paiement_mode -- int field (1: espese, 2: chèque, 3: LCN)
    """
    data = request.data
    response = {}
    direct_sale = get_object_or_404(DirectSale, pk=request.data.get("direct_sale"))
    serializer = PaimentByDirectSaleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        
        # Add paiement_try
        pay_data = {
                    "amount": data.get("amount", 0),
                    "paiement_mode": data.get("paiement_mode", 1),
                    "paiement_direct_sale": serializer.data.get("id"),
                    "client": direct_sale.client.id,
                    "date": data.get("date", 0),
                    }
        pay_serializer = PaiementTrySerializer(data=pay_data)
        if pay_serializer.is_valid():
            pay_serializer.save()
            response.update(serializer.data)
            response.update(pay_serializer.data)
            response["id"] = serializer.data.get("id") #update id field with direct sale paiement
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(pay_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_direct_sale_paiement(request):
    """
    id -- id of paiement
    """
    id = request.data.get("id")
    paiement = get_object_or_404(PaimentByDirectSale, id=id)
    serializer = PaimentByDirectSaleSerializer(instance=paiement, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_direct_sale_paiement(request):
    """
    id -- id of paiement
    """
    id = request.GET.get("id")
    paiement = get_object_or_404(PaimentByDirectSale, id=id)
    paiement.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_direct_sale_paiements(request):
    """
    direct_sale_id -- id of sale
    """
    direct_sale = request.GET.get("direct_sale_id", None)
    paiements = PaimentByDirectSale.objects.filter(direct_sale=direct_sale).order_by('-id')
    serializer = PaimentByDirectSaleSerializer(paiements, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



# --------- PAYMENT TRIES -----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_paiement_try(request):
    """
    paiement_by_command -- id of command
    paiement_by_client -- id of client
    paiement_direct_sale -- id of direct sale
    paiement_mode -- int field (1: espese, 2: chèque, 3: LCN, 4: virement)
    amount -- paid amount
    """
    data = request.data
    commande_payment = PaiementByCommand.objects.filter(id=request.data.get("paiement_by_command")).only("commande").last()
    direct_sale_payment = PaimentByDirectSale.objects.filter(id=request.data.get("paiement_direct_sale")).only("direct_sale").last()
    
    if request.data.get("paiement_by_client"):
        client_id = request.data.get("paiement_by_client")
    elif commande_payment:
        client_id = commande_payment.commande.client.id
    elif direct_sale_payment:
        client_id = direct_sale_payment.direct_sale.client.id
        
    data["client"] = client_id
    serializer = PaiementTrySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paiement_try(request):
    """
    id -- id of payment try
    """
    instance = get_object_or_404(PaiementTry, id=request.data.get("id"))
    serializer = PaiementTrySerializer(instance=instance, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_paiement_try(request):
    """
    id -- id of payment try
    """
    instance = get_object_or_404(PaiementTry, id=request.data.get("id"))
    try:
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_paiement_tries(request):
    """
    command -- id of command
    client -- id of client
    direct_sale -- id of direct sale
    """
    paiement_by_command = request.GET.get("command")
    paiement_by_client = request.GET.get("client")
    paiement_direct_sale = request.GET.get("direct_sale")
    
    if paiement_by_command:
        payments = PaiementTry.objects.prefetch_related('proofs').filter(paiement_by_command=paiement_by_command).order_by("-id")
        
    elif paiement_by_client:
        payments = PaiementTry.objects.prefetch_related('proofs').filter(paiement_by_client=paiement_by_client).order_by("-id")
        
    elif paiement_direct_sale:
        payments = PaiementTry.objects.prefetch_related('proofs').filter(paiement_direct_sale=paiement_direct_sale).order_by("-id")
        
    serializer = PaiementTrySerializer(payments, many=True, context={'request': request})
    return Response(serializer.data, status=status.HTTP_200_OK)

# TODO Update paiment status
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_paiment_status(request):
    """
    id -- id of payment try
    status -- int (required)
    """
    paiment = get_object_or_404(PaiementTry, pk=request.data.get('id', ''))
    paiment.status = request.data.get('status', 1)
    paiment.save()
    return Response(status=status.HTTP_204_NO_CONTENT)



# --------- PAYMENT PROOF -----------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_payment_try_proof(request):
    """
    paiement_try -- id of payment try
    file -- uploaded file (allowed_extensions = ['jpg','jpeg','png'])
    """
    file = request.FILES.get('file')
    if not is_image_extension_valid(file):
        return Response({"image format is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    file = resize_image(file, 800)
    data = {
        "paiement_try": request.data.get("paiement_try"),
        "file": file,
    }
    serializer = PaiementProofSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_payment_try_proof(request):
    """
    id -- id of payment proof
    file -- uploaded file (allowed_extensions = ['jpg','jpeg','png'])
    """
    #get instance
    instance = get_object_or_404(PaiementProof, id=request.data.get("id"))
    
    #verify file existance
    file = request.FILES.get('file')
    if not file:
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    #check file extension
    if not is_image_extension_valid(file):
        return Response({"error: image format is not valid"}, status=status.HTTP_400_BAD_REQUEST)
    
    #resize file
    file = resize_image(file, 800)
    data = {
        "paiement_try": request.data.get("paiement_try"),
        "file": file,
    }
    serializer = PaiementProofSerializer(instance=instance, data=data, partial=True)
    if serializer.is_valid():
        instance.file.delete()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_payment_try_proof(request):
    """
    id -- id of payment proof
    """
    #get instance
    instance = get_object_or_404(PaiementProof, id=request.data.get("id"))
    instance.file.delete()
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_payment_try_proofs(request):
    """
    paiement_try -- id of payment try
    """
    paiement_try = request.GET.get("paiement_try")
    paiment_proofs = PaiementProof.objects.filter(paiement_try=paiement_try).order_by("history__history_date")
    serializer = PaiementProofSerializer(paiment_proofs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
    
    

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_solde(request):
    client = get_object_or_404(Client, pk=request.GET.get("client_id"))
    command_paiements = helpers.get_client_command_paiements(client.id)
    client_paiements = helpers.get_client_paiements(client.id)
    direct_sale_paiements = helpers.get_direct_sale_paiements(client.id)
    client_total_credit = helpers.get_all_client_credits(client.id)
    
    response = {
        "client": client.name,
        "pending_paiements": calc_cumul_int(command_paiements.get("amount_status_1"), client_paiements.get("amount_status_1"), direct_sale_paiements.get("amount_status_1")),
        "success_paiements": calc_cumul_int(command_paiements.get("amount_status_2"), client_paiements.get("amount_status_2"), direct_sale_paiements.get("amount_status_2")),
        "failed_paiements": calc_cumul_int(command_paiements.get("amount_status_3"), client_paiements.get("amount_status_3"), direct_sale_paiements.get("amount_status_3")),
        "client_total_credit": client_total_credit,
    }
    
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_clients_soldes(request):
    clients = Client.objects.all()
    response = []
    for client in clients:
        command_paiements = helpers.get_client_command_paiements(client.id)
        client_paiements = helpers.get_client_paiements(client.id)
        direct_sale_paiements = helpers.get_direct_sale_paiements(client.id)
        client_total_credit = helpers.get_all_client_credits(client.id)

        response.append({
            "client": client.name,          
            "pending_paiements": calc_cumul_int(command_paiements.get("amount_status_1"), client_paiements.get("amount_status_1"), direct_sale_paiements.get("amount_status_1")),
            "success_paiements": calc_cumul_int(command_paiements.get("amount_status_2"), client_paiements.get("amount_status_2"), direct_sale_paiements.get("amount_status_2")),
            "failed_paiements": calc_cumul_int(command_paiements.get("amount_status_3"), client_paiements.get("amount_status_3"), direct_sale_paiements.get("amount_status_3")),
            "client_total_credit": client_total_credit,
        })
    return Response(response, status=status.HTTP_200_OK)