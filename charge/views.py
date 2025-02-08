from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments

# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_charge(request):
    """
    command -- the command id (int required)
    driver -- the driver id (int required)
    quantity -- quantity (int)
    eggs_produced_at -- the date the eggs were produced (date required)
    datetime -- the date and time the charge was made (datetime required)
    change -- the qty of change (int)
    """
    data = request.data
    serializer = ChargeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_charge(request):
    """
    id -- the charge id (int required)
    """
    charge = get_object_or_404(Charge, id=request.data.get('id'))
    batiments = get_user_batiments(request.user.UserExt)
    if charge.commande.batiment not in batiments:
        return Response({'error': 'You are not allowed to update this charge'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ChargeSerializer(charge, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_charge(request):
    """
    id -- the charge id (int required)
    """
    charge = get_object_or_404(Charge, id=request.data.get('id'))
    batiments = get_user_batiments(request.user.UserExt)
    if charge.commande.batiment not in batiments:
        return Response({'error': 'You are not allowed to delete this charge'}, status=status.HTTP_403_FORBIDDEN)
    charge.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_single_charge(request):
    """
    id -- the charge id (int required)
    """
    charge = get_object_or_404(Charge, id=request.GET.get('id'))
    batiments = get_user_batiments(request.user.UserExt)
    if charge.commande.batiment not in batiments:
        return Response({'error': 'You are not allowed to view this charge'}, status=status.HTTP_403_FORBIDDEN)
    serializer = ChargeSerializer(charge)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_charges_by_command(request):
    """
    command_id -- the command id (int required)
    """
    command_id = request.GET.get('command_id')
    charges = Charge.objects.filter(commande=command_id)
    # charges = Charge.objects.all()

    serializer = ChargeSerializer(charges, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_charges_by_driver(request):
    """
    driver_id -- the driver id (int required)
    """
    driver_id = request.GET.get('driver_id')
    charges = Charge.objects.filter(commande=driver_id)
    serializer = ChargeSerializer(charges, many=True)
    return Response(serializer.data)