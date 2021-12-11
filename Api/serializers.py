from rest_framework import serializers
from django.contrib.auth.models import User
from Main.models import Tasks#, CustomUser
from datetime import datetime
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

class LoginToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        username = user.username
        email = user.email
        return Response({'username': username, 'email': email, 'token': token.key})

class DashboardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasks
        fields = "__all__"
        extra_kwargs = {
            'task_user': {'read_only': True},
        }
    
    def save(self, request, pk):
    
        if request.method == "POST":
            task_user = request.user.username
            task = self.validated_data["task"]
            
            new_task = Tasks(task_user=task_user, task=task)
            new_task.save()
            return new_task
        
        elif request.method == "PUT":
            task = Tasks.objects.get(pk=pk)
            
            task.task = self.validated_data["task"]
            task.done = self.validated_data["done"]
            task.updated = datetime.now()
            task.save()
            
            return task
            

class RegistrationSerializer(serializers.ModelSerializer):
    password_confirmation = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirmation']
        extra_kwargs = {
            'password_confirmation': {'write_only': True},
        }
        
    def save(self):
        username = self.validated_data['username']
        email = self.validated_data['email']
        password = self.validated_data['password']
        password_confirmation = self.validated_data['password_confirmation']
        
        if password != password_confirmation:
            raise serializers.ValidationError({'error': 'password & confirmation password do not match'})
        
        if User.objects.filter(email=self.validated_data['email']).exists():
            raise serializers.ValidationError({'email': 'this email is already in use'})
        
        account = User(username=username, email=email)
        account.set_password(password)
        account.save()
        
        return account
    
    
    
