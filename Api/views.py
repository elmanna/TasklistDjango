from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
import json


# Create your views here.

def Welcome(request):
    return JsonResponse({"welcome": "Welcome To Taskmate Api"})

class Dashboard(View):
    def get(self, request):
        msg = {
            "msg": "welcome ahmad almnna"
        }
        #json_msg = json.dumps(msg)
        return JsonResponse({"msg": "welcome ahmad almnna"})
        
class Login(View):
    def get(self, request):
        # msg = {
        #     "User": "ahmad",
        #     "Password": "jasonDz1"
        # }
        return JsonResponse({
            "User": "ahmad",
            "Password": "jasonDz1"
        })