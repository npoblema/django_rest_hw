# users/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from .serializers import UserRegisterSerializer

class RegisterView(APIView):
    @extend_schema(summary="Регистрация пользователя", responses={201: None, 400: None})
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)