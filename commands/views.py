from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments
from django.db.models.functions import Concat, Cast, ExtractDay, ExtractMonth, ExtractYear, Right
from django.db.models import CharField,Func, Value as V
from time import strftime


# Create your views here.
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_command(request):
    """
    batiment -- id of batiemt int (required)
    client -- id of client int (required)
    quantity -- int (required)
    poids_plateau -- float (default 0)
    pu -- float (required)
    description -- string (required)
    """
    data = request.data
    data["created_by"] = request.user.id
    batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    if data['batiment'] not in batiments:
        return Response({'error': 'You are not allowed to create command for this batiment'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommandeSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_command(request):
    """
    id -- the command id (int required)
    """
    command = get_object_or_404(Commande, id=request.data.get('id'))
    batiments = get_user_batiments(request.user.userext)
    if command.batiment not in batiments:
        return Response({'error': 'You are not allowed to update this command'}, status=status.HTTP_403_FORBIDDEN)
    serializer = CommandeSerializer(command, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_command(request):
    """
    id -- the command id (int required)
    """
    command = get_object_or_404(Commande, id=request.data.get('id'))
    batiments = get_user_batiments(request.user.userext)
    if command.batiment not in batiments:
        return Response({'error': 'You are not allowed to delete this command'}, status=status.HTTP_403_FORBIDDEN)
    command.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_recent_commands(request):
    """
    client -- client
    is_delivered -- is_delivered
    start_date -- start_date
    end_date -- end_date
    last_date -- last_date
    """
    batiments = get_user_batiments(request.user.userext)
    client = request.GET.get('client')
    is_delivered = request.GET.get('is_delivered', False)
    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")
    last_date = request.GET.get("last_date")
    # FILTRER BY CLIENT
    if client:
        if start_date and end_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__gte=start_date,
                                           date__lte=end_date,
                                           client=client
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif start_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__gte=start_date,
                                           client=client
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif end_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__lte=end_date,
                                           client=client
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif last_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           client=client,
                                           date__gt=last_date
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')[:10]
        else:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           client=client
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')[:10]
    
    #NO FILTER
    else:
        if start_date and end_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__gte=start_date,
                                           date__lte=end_date,
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif start_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__gte=start_date
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif end_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                           is_delivered=is_delivered,
                                           date__lte=end_date
                                           ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')
        elif last_date:
            commands = Commande.objects.filter(batiment__in=batiments,
                                               is_delivered=is_delivered,
                                               date__gt=last_date
                                               ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')[:10]
        else:
            commands = Commande.objects.filter(batiment__in=batiments,
                                               is_delivered=is_delivered,
                                               ).annotate(batiment_name=F('batiment__name'),
                                                                               client_name=F('client__name'),
                                                                               site_name=F('batiment__site__name'),
                                                                               site_id=F('batiment__site__id'),
                                                                               ).order_by('-date')[:10]

    
    serializer = CommandeSerializer(commands, many=True)
    return Response(serializer.data)

# TODO Make the command dilivery
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def make_command_dilevery(request):
    """
    command - int (required)
    """
    command_id = request.query_params.get('command')
    if command_id:
        command = Commande.objects.get(pk=command_id)
        command.is_delivered = not command.is_delivered
        command.save()
        return Response({"Message": "command change statut avec success"})
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
# TODO Get list of command no livrer
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def select_command_no_delivery(request):
    # command = Commande.objects.values('id').annotate(value=Concat('client__name', V(' - '), 
    #     'batiment__name', V(' - '), 
    #     Right(Concat(V('0'), Cast(ExtractMonth('date'), CharField())), 2), V('/'),  # Zero-pad month
    #     Right(Concat(V('0'), Cast(ExtractDay('date'), CharField())), 2), V('/'),    
    #     Cast(ExtractYear('date'), output_field=CharField())  
    # ))
    commands = Commande.objects.filter(is_delivered=False).values('id','client__name', 'batiment__name', 'date')
    new_command = []
    for command in commands:
        new_command.append({
            'id': command['id'],
            'value': f"{command['client__name']} {command['batiment__name']} {command['date'].strftime('%d/%m/%Y')}"
        })
    return Response(new_command)