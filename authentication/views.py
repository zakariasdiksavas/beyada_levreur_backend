from django.shortcuts import get_object_or_404, render
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from drf_spectacular.utils import extend_schema

# Create your views here.

@api_view(['POST'])
def register_user(request):
    """
    username -- string (required)
    password -- string (required)
    first_name -- string || null
    last_name -- string || null
    is_active -- 0 || 1
    email -- string (exemple@exemple.com) || null
    phone -- string || null
    sites -- array of integers (ids of sites)
    
    """
    data = request.data
    hashed_password = make_password(request.data.get("password"))
    data["password"] = hashed_password
    user_serializer = UserSerializer(data=data)
    if user_serializer.is_valid():
        #Create user extentions
        user_ext_data = {
            "user": user_serializer.data.get("id"),
            "eleveur": request.user.userext.eleveur.id,
            "sites": request.data.get("sites"),
            "phone": request.data.get("phone"),
            }
        user_ext_serializer = UserExtSerializer(data=user_ext_data)
        if user_ext_serializer.is_valid():
            user_serializer.save() #save user
            user_ext_serializer.save() #save user extention
            return Response(user_serializer.data.update(user_ext_serializer.data), status=status.HTTP_201_CREATED)
    return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user(request):
    """
    pk -- url/user id integer (required)/
    """
    user = get_object_or_404(User, id=request.GET.get("id"))
    serializer = UserSerializer(user)
    userext_serializer = UserExtSerializer(data=user.userext)
    return Response(serializer.data.update(userext_serializer.data))
    
    
@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    pk -- url/user id integer (required)/
    """
    user = get_object_or_404(User, id=request.data.get("id"))
    serializer = UserSerializer(user, data=request.data, partial=True)
    if serializer.is_valid():
        #Update user extentions
        instance = UserExt.objects.get(user=user)
        user_ext_data = {
            "sites": request.data.get("sites", instance.sites),
            "phone": request.data.get("phone", instance.phone),
            }
        user_ext_serializer = UserExtSerializer(instance, data=user_ext_data, partial=True)
        if user_ext_serializer.is_valid():
            serializer.save()
            user_ext_serializer.save()
        return Response(serializer.data.update(user_ext_serializer.data), status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request):
    """
    pk -- url/user id integer (required)/
    """
    user = get_object_or_404(User, id=request.data.get("id"))
    try:
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except:
        return Response({"error": "user can't be deleted"},status=status.HTTP_400_BAD_REQUEST)