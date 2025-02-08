from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments
from time import strftime
from datetime import datetime


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_direct_sale(request):
    data = request.data
    serializer = DirectSaleSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        # data = serializer.data.copy()
        # data['date'] = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        # data['date'] = data['date'].strftime('%d/%m/%Y')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_direct_sale(request):
    """
    id -- the sale id (int required)
    """
    sale = get_object_or_404(DirectSale, id=request.data.get('id'))
    serializer = DirectSaleSerializer(instance=sale, data=request.data)
    if serializer.is_valid():
        serializer.save()
        # data = serializer.data.copy()
        # data['date'] = datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%SZ')
        # data['date'] = data['date'].strftime('%d-%m-%Y')
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_direct_sale(request):
    """
    id -- the sale id (int required)
    """
    sale = get_object_or_404(DirectSale, id=request.data.get('id'))
    try:
        sale.delete()
    except Exception:
        return Response({"error": "record cannot be deleted"},status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_direct_sales(request):
    client = request.GET.get("client", None)
    user = request.user
    batiments = get_user_batiments(user.userext)
    if client:
        sales = DirectSale.objects.prefetch_related('client', 'betiment', 'batiment__site').filter(client=client, batiment__in=batiments).order_by('-created_at')
        serializer = DirectSaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        sales = DirectSale.objects.select_related('client', 'batiment', 'batiment__site').filter(batiment__in=batiments).order_by('-created_at')
        serializer = DirectSaleSerializer(sales, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
