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


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserLoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            return Response({'error': 'Invalid credentials'}, status=401)


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
