from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from .models import UserData, NonceSignRequest
from rest_framework import status
from rest_framework import permissions
from django.conf import settings
from .tasks import *
from django.http import JsonResponse

class IsAdmin(permissions.BasePermission):

    edit_methods = ("PUT", "POST", "CREATE", "DELETE")

    def has_permission(self, request, view):
        return request.user.role == 'Admin'

    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return True
        return False


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class UserView(APIView):
    # permission_classes = (IsAuthenticated, IsAdmin)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def put(self, request):
        # id = self.request.query_params.get('id', None)
        obj = request.user
        if 'password' in request.data.keys():
            obj.set_password(request.data['password'])
            request.data._mutable = True
            request.data.pop('password')
            request.data._mutable = False
        address = request.data.get('address', None)
        if address:
            obj.address = address
        obj.save()
        serializer = UserSerializer(obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def get(self, request):
        id = self.request.query_params.get('id', None)
        if not id:
            objs = UserData.objects.all()
            serialized = UserSerializer(objs, many=True)
            return Response(serialized.data)
        else:
            obj = UserData.objects.get(id=id)
            serialized = UserSerializer(obj)
            return Response(serialized.data)
    
    def delete(self, request):
        id = self.request.query_params.get('id', None)
        if not id:
            return Response(status=status.HTTP_404_NOT_FOUND)
        try:
            obj = UserData.objects.get(id=id)
            obj.delete()
            return Response(status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)


class NonceSignRequestView(APIView):

    def post(self, request):
        res = add.delay(2, 2)
        test = res.get(timeout=1)
        return JsonResponse({
            'response': test
        })
