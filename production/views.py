from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments
from django.db.models import Sum
from commands.models import Commande
from charge.models import Charge
from direct_sales.models import DirectSale
from inventaire.models import Inventaire


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_production(request):
    """
    batiment -- id of batiment (required)
    normal -- int
    double_jaune -- int
    blanc -- int
    sale -- int
    casse -- int
    elimine -- float
    triage -- int
    poids_plateau -- float
    tare_alveole -- float
    production_date -- date
    """
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    if request.data["batiment"] not in batiments:
        return Response({'message': 'No batiments found'}, status=status.HTTP_404_NOT_FOUND)
    data = request.data
    data["created_by"] = request.user.id
    serializer = ProductionSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_production(request):
    user = request.user.userext
    production = get_object_or_404(Production, id=request.data.get("id"))
    batiments = get_user_batiments(user)
    if production.batiment not in batiments:
        return Response({'message': 'No batiments found'}, status=status.HTTP_404_NOT_FOUND)
    serializer = ProductionSerializer(production, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_production(request):
    user = request.user.userext
    production = get_object_or_404(Production, id=request.data.get("id"))
    batiments = get_user_batiments(user)
    if production.batiment not in batiments:
        return Response({'message': 'No batiments found'}, status=status.HTTP_404_NOT_FOUND)
    production.delete()
    return Response({'message': 'Production deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_productions(request):
    """
    batiment_id -- int (required)
    last_date -- date (optional)
    start_date -- date (optional)
    end_date -- date (optional)
    """
    last_date = request.GET.get('last_date')
    batiment_id = request.GET.get('batiment_id')
    
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    batiments = [int(batiment.id) for batiment in get_user_batiments(request.user.userext)]
    if int(batiment_id) not in batiments:
        return Response({'message': 'No batiments found'}, status=status.HTTP_404_NOT_FOUND)
    
    #FILTRE ----
    if start_date and end_date:
        productions = Production.objects.filter(batiment=batiment_id, production_date__range=[start_date, end_date]).order_by('-production_date')
    elif start_date:
        productions = Production.objects.filter(batiment=batiment_id, production_date__gte=start_date).order_by('-production_date')
    elif end_date:
        productions = Production.objects.filter(batiment=batiment_id, production_date__lte=end_date).order_by('-production_date')
    elif last_date:
        productions = Production.objects.filter(batiment=batiment_id, production_date__gte=last_date).order_by('-production_date')[:10]
    else:
        productions = Production.objects.filter(batiment=batiment_id).order_by('-production_date')[:50]

    serializer = ProductionSerializer(productions, many=True)
    return Response(serializer.data)



# TODO Get stock
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stock(request):
    list_classe = {
        1: "normal",
        2: "double_jaune",
        3: "blanc",
        4: "sale",
        5: "casse",
        6: "elimine",
        7: "triage",
    }
    # TODO 1- Get all batiment IDs related to this user
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    # TODO 2- Get command and charge related to the batiment and calcul sum of each one, we did that in one query to increase the performances
    commands = Commande.objects.filter(batiment__in=batiments)\
    .prefetch_related('charges')\
    .values('classe', 'charges__classe')\
    .annotate(command_sum=Sum('quantity'), charge_sum=Sum('charges__quantity'))


    # TODO 3- Fetch all production sums
    production_data = Production.objects.filter(batiment__in=batiments).aggregate(
        **{list_classe[key]: Sum(list_classe[key]) for key in list_classe}
    )
    # TODO 4- Fetch all direct sales sums
    direct_sale_data = DirectSale.objects.filter(batiment__in=batiments).values('classe').annotate(sum=Sum('quantity'))
    # TODO 5- Fetch all inventaire sums
    inventaire_data = Inventaire.objects.filter(batiment__in=batiments).values('classe').annotate(sum=Sum('quantity'))

    # TODO 6- Convert Commande and charge and direct sale queryset to a dictionary
    commande_dict = {item["classe"]: item["command_sum"] or 0 for item in commands}
    charge_dict = {item["charges__classe"]: item["charge_sum"] for item in commands}
    direct_sale_dict = {item["classe"]: item["sum"] for item in direct_sale_data}
    inventaire_dict = {item["classe"]: item["sum"] for item in inventaire_data}
    # TODO 7- Calculate stock
    reel_stock = {
        list_classe[key]: (production_data.get(list_classe[key]) or 0) 
        - (charge_dict.get(key) or 0) 
        - (direct_sale_dict.get(key) or 0) 
        + (inventaire_dict.get(key) or 0)
        for key in list_classe
    }
    provision_stock = {
        list_classe[key]: (production_data.get(list_classe[key]) or 0) 
        - (commande_dict.get(key) or 0)  
        - (direct_sale_dict.get(key) or 0) 
        + (inventaire_dict.get(key) or 0)
        for key in list_classe
    }

    return Response({
        "reel_stock": reel_stock,
        "provision_stock": provision_stock
    })


    

# TODO Get stock by client
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_stock_by_client(request):
    """
        client -- int (required)
    """
    list_classe = {
        1: "normal",
        2: "double_jaune",
        3: "blanc",
        4: "sale",
        5: "casse",
        6: "elimine",
        7: "triage",
    }
    client = request.query_params.get('client')
    if client:
        # TODO 1- Get command and charge related to the batiment and calcul sum of each one, we did that in one query to increase the performances
        commands = Commande.objects.filter(client=client)\
        .prefetch_related('charges')\
        .values('classe', 'charges__classe')\
        .annotate(command_sum=Sum('quantity'), charge_sum=Sum('charges__quantity'))
        # TODO 2- Convert Commande queryset to a dictionary
        commande_dict = {item["classe"]: item["command_sum"] for item in commands}
        charge_dict = {item["charges__classe"]: item["charge_sum"] for item in commands}
        # TODO 3- Prepare the output
        stock_client = {
            list_classe[key]: (commande_dict.get(key) or 0 ) - (charge_dict.get(key) or 0)
            for key in list_classe
        }
        return Response(stock_client)
