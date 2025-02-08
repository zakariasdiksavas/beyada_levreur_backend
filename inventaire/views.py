from django.shortcuts import render
from .serializer import InventaireSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from authentication.getters import get_user_batiments
from rest_framework.response import Response
from .models import Inventaire
from django.db.models import Q

# Create your views here.

# TODO Add inventaire

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_inventaire(request):
    """
    batiment - int(required)
    quantity - int(required)
    classe - int(required)
    is_positive - boolean(required)
    date - date(required)
    """
    # TODO Check if they have access for this batiment
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    if not request.data['batiment'] in batiments:
        return Response({'error': 'You are not allowed to create inventaire for this batiment'}, status=status.HTTP_403_FORBIDDEN)
    data = request.data.copy()
    if not data['is_positive']:
        data['quantity'] = -data['quantity']
    serializer = InventaireSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# TODO Update inventaire

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_inventaire(request):
    """
    id - int(required)
    batiment - int(required)
    quantity - int(required)
    classe - int(required)
    is_positive - boolean(required)
    date - date(required)
    """
    # TODO Check if they have access for this batiment
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    if not request.data['batiment'] in batiments:
        return Response({'error': 'You are not allowed to create inventaire for this batiment'}, status=status.HTTP_403_FORBIDDEN)
    data = request.data.copy()
    if not data['is_positive'] and data['quantity'] < 0:
        data['quantity'] = -(data['quantity'])
    elif data['is_positive'] and data['quantity'] < 0:
        data['quantity'] = -(data['quantity'])
    else:
        data['quantity'] = -(data['quantity'])

    try:
        inventaire = Inventaire.objects.get(pk=data['id'])
        serializer = InventaireSerializer(inventaire, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except Inventaire.DoesNotExist:
        return Response({'error' : 'No inventaire match the query given .'}, status=status.HTTP_404_NOT_FOUND)

# TODO Delete inventaire

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_inventaire(request):
    """
    id - int(required)
    """
    try:
        inventaire = Inventaire.objects.get(pk=request.data['id'])
        inventaire.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Inventaire.DoesNotExist:
        return Response({'error' : 'No inventaire match the query given .'}, status=status.HTTP_404_NOT_FOUND)
    
# TODO List inventaire
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_inventaire(request):
    """
        id - int
        batiment - int
        date1 - date
        date2 - date
    """
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    params = request.query_params
    page_number = 10
    inventaire = Inventaire.objects.select_related('batiment', 'batiment__site')
    filter = Q()
    isInitial = True # todo Check if this is the initial request
    is_last = True # todo Check in pagination if this is the last item
    if params.get('batiment'):
        isInitial = False
        batiments = [batiment for batiment in batiments if batiment == int(params.get('batiment'))]
        print(batiments)
    filter &= Q(batiment__in=batiments)
    if params.get('id', None):
        filter &= Q(id__lt=int(params.get('id', None)))
    if params.get('date1') and params.get('date2', None):
        isInitial = False
        filter &= Q(date__range=(params.get('date1', None),params.get('date2', None)))
    elif params.get('date1'):
        isInitial = False
        filter &= Q(date__gte=params.get('date1', None))

    elif params.get('date2', None):
        isInitial = False
        inventaire = inventaire.filter(date__lte=params.get('date2', None))
        filter &= Q(date__lte=params.get('date2'))

    inventaire = inventaire.filter(filter).order_by('-id')
    if (isInitial or params.get('id', None)) and len(inventaire) > 0:
        inventaire = inventaire[:page_number]
        if not inventaire[len(inventaire) - 1].id == Inventaire.objects.filter(filter).first().id:
            is_last = False

    serializer = InventaireSerializer(inventaire, many=True)
    return Response({'data' : serializer.data, 'is_last': is_last})


# # TODO List inventaire
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def list_inventaire(request):
#     params = request.query_params
#     inventaire = Inventaire.objects.prefetch_related('batiment')
#     filter = Q()
#     isInitial = True # todo Check if this is the initial request
#     if params.get('id'):
#         filter &= Q(id__gt=int(params.get('id')))
#     if params.get('batiment'):
#         isInitial = False
#         filter &= Q(batiment=int(params.get('batiment')))
#     if params.get('date1') and params.get('date2'):
#         isInitial = False
#         filter &= Q(date__range=(params.get('date1'),params.get('date2')))
#     elif params.get('date1'):
#         isInitial = False
#         filter &= Q(date__gte=params.get('date1'))

#     elif params.get('date2'):
#         isInitial = False
#         inventaire = inventaire.filter(date__lte=params.get('date2'))
#         filter &= Q(date__lte=params.get('date2'))

#     inventaire = inventaire.filter(filter)
#     if isInitial or params.get('id'):
#         paginator = Pagination()
#         inventaire = inventaire.order_by('-id')
#         pagianate_inventaire = paginator.paginate_queryset(inventaire, request)
#         serializer = InventaireSerializer(pagianate_inventaire, many=True)
#         return paginator.get_paginated_response(serializer.data)