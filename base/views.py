from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from django.shortcuts import get_object_or_404
from authentication.getters import get_user_batiments

# Create your views here.
# -------- ELEVEUR --------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_eleveur(request):
    """
    name -- name of the eleveur (required)
    address -- address of the eleveur
    phone -- phone number of the eleveur
    email -- email of the eleveur
    """
    data = request.data
    serializer = EleveurSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_eleveur(request):
    """
    id -- id of the eleveur (required)
    """
    eleveur = get_object_or_404(Eleveur, id=request.data.get("id"))
    serializer = EleveurSerializer(eleveur, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_eleveur(request):
    """
    id -- id of the eleveur (required)
    """
    eleveur = get_object_or_404(Eleveur, id=request.data.get("id"))
    eleveur.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_eleveurs(request):
    eleveurs = Eleveur.objects.all()
    serializer = EleveurSerializer(eleveurs, many=True)
    return Response(serializer.data)


# -------- BATIMENT --------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_batiemnt(request):
    """
    name -- name of the batiment (required)
    site -- site id (required)
    """
    data = request.data
    serializer = BatimentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_batiment(request):
    """
    id -- id of the batiment (required)
    """
    batiment = get_object_or_404(Batiment, id=request.data.get("id"))
    
    # batiments = [batiment.id for batiment in get_user_batiments(request.user.userext)]
    # if batiment not in batiments:
    #     return Response(status=status.HTTP_403_FORBIDDEN)
    
    serializer = BatimentSerializer(instance=batiment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_batiment(request):
    """
    id -- id of the batiment (required)
    """
    batiment = get_object_or_404(Batiment, id=request.data.get("id"))
    batiment.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_batiments(request):
    """
    site_id -- site id (required)
    """
    site_id = request.GET.get('site_id')  
    batiments = Batiment.objects.filter(site=site_id)
    serializer = BatimentSerializer(batiments, many=True)
    return Response(serializer.data)


# -------- SITE --------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_site(request):
    """
    name -- name of the site (required)
    address -- address of the site
    """
    data = request.data
    data["eleveur"] = request.user.userext.eleveur.id
    serializer = SiteSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_site(request):
    """
    id -- id of the site (required)
    """
    site = get_object_or_404(Site, id=request.data.get("id"))
    serializer = SiteSerializer(site, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_site(request):
    """
    id -- id of the site (required)
    """
    site = get_object_or_404(Site, id=request.data.get("id"))
    site.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_sites(request):
    sites = Site.objects.filter(eleveur=request.user.userext.eleveur).order_by("-name")
    if len(sites) == 0:
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = SiteSerializer(sites, many=True)
    return Response(serializer.data)

# -------- CLIENT --------

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_client(request):
    """
    eleveur -- eleveur id (required)
    name -- name of the client (required)
    address -- address of the client
    phone -- phone number of the client
    email -- email of the client
    """
    data = request.data
    data["eleveur"] = request.user.userext.eleveur.id
    serializer = ClientSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_client(request):
    """
    id -- id of the client (required)
    """
    client = get_object_or_404(Client, id=request.data.get("id"))
    serializer = ClientSerializer(client, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_client(request):
    """
    id -- id of the client (required)
    """
    client = get_object_or_404(Client, id=request.data.get("id"))
    client.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_clients(request):
    eleveur = request.user.userext.eleveur
    clients = eleveur.clients.all()
    serializer = ClientSerializer(clients, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def bind_client_to_batiment(request):
    """
    client -- client id (required)
    batiment -- batiment id (required)
    is_linked -- boolean [1 || 0] (default False)
    """
    data = request.data
    data["is_linked"] = bool(request.data.get("is_linked", 0))
    serializer = ClientBatimentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_batiments_with_binded_clients(request):
    clients = Client.objects.filter(eleveur=request.user.userext.eleveur).order_by("name")
    batiments = Batiment.objects.filter(site__eleveur=request.user.userext.eleveur)
    response = []
    for client in clients:
        binded_client_batiment = []
        for batiment in batiments:
            binded = ClientBatiment.objects.filter(client=client, batiment=batiment).values("batiment__name", "batiment__id", "is_linked").order_by("created_at").last()
            if binded and binded.get("is_linked"):
                binded_client_batiment.append({
                    "name":  binded.get("batiment__name"),
                    "id": binded.get("batiment__id"),
                })
        
        response.append({
            "client": client.name,
            "id": client.id,
            "binded_to": binded_client_batiment
        })
    return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_select_options(request):
    sites = request.user.userext.sites.all()
    response = []
    for site in sites:
        response.append({
                         "id": site.id,
                         "name": site.name,
                         "batiments": site.batiments.all().values('id', 'name')
                         })
        
    return Response(response)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_client_select_options(request):
    response = request.user.userext.eleveur.clients.filter(is_active=True).values('id', 'name')
    return Response(response, status=status.HTTP_200_OK)