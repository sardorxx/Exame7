from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from app.models import UserPasswordManager
from .serializers import UserNameAplicationSerializer, UserSerializer
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, get_user_model
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

User = get_user_model()

@api_view(['POST'])
@permission_classes([AllowAny])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'}, status=400)

    if User.objects.filter(username=username).exists():
        return JsonResponse({'error': 'Username is already taken'}, status=400)

    user = User.objects.create_user(username=username, password=password)
    login(request, user)
    token, created = Token.objects.get_or_create(user=user)

    return JsonResponse({'token': token.key})

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if username is None or password is None:
        return JsonResponse({'error': 'Please provide both username and password'}, status=400)

    user = authenticate(username=username, password=password)

    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=400)

    login(request, user)
    token, created = Token.objects.get_or_create(user=user)

    return JsonResponse({'token': token.key})

@api_view(['POST'])
def logout_view(request):
    request.auth.delete()  # Invalidate the token
    return JsonResponse({'message': 'Logout successful'})


class UserPassManagerlFilterViewSet(viewsets.ModelViewSet):
    queryset = UserPasswordManager.objects.all()
    serializer_class = UserNameAplicationSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name', 'application_type']


@api_view(['GET'])
def Hello_World(request):
    data = {
        'message': 'Hello World'
    }
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def password_type(request):
    if request.method == 'GET':
        data = UserPasswordManager.objects.all()
        serializer = UserNameAplicationSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        serializer = UserNameAplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
