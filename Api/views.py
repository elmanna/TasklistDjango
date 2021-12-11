from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
from .serializers import DashboardSerializer, RegistrationSerializer
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers
from Main.models import Tasks
from .permissions import IsOwner
# Create your views here.

@api_view(['POST',])
def ForgetPassword(request):
    pass

@api_view(['POST',])
def Registration(request):
    if request.method == 'POST':
        serializer = RegistrationSerializer(data=request.data)
        
        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            token = Token.objects.create(user=account).key
            
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = token
        else:
            data = serializer.errors
        
        return Response(data=data)


@api_view(['POST',])
def Logout(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


@api_view(['GET',])
def Version(request):
    version = "0.0.2"
    data = {"version": version}
    return Response(data=data, status=status.HTTP_200_OK)

class IsTokenValid(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response(status=status.HTTP_200_OK)

class Dashboard(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    
    
    def get(self, request, pk=None):
        
        if pk is None:
            tasks = Tasks.objects.all().filter(task_user=request.user.username)
            serializer = DashboardSerializer(tasks, many=True)
            return Response(serializer.data)#
        else:
            try:
                task = Tasks.objects.get(pk=pk)
                serializer = DashboardSerializer(task)
                return Response(serializer.data)
            except Exception:
                return Response(data={"error": "Task does not exist"}, status=status.HTTP_400_BAD_REQUEST)
                
                
    
    def post(self, request, pk=None):
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request, pk=pk)
            return Response(serializer.data)
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        if pk is None:
            return Response(data={"error": "please send a pk of the task to update it"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = DashboardSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(request=request, pk=pk)
            return Response(data=request.data, status=status.HTTP_200_OK)
        
        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk=None):
        if pk is None:
            return Response(data={"error": "please send a pk of the task to delete it"}, status=status.HTTP_400_BAD_REQUEST)
        
        task = Tasks.objects.get(pk=pk)
        task.delete()
        
        return Response(status=status.HTTP_200_OK)