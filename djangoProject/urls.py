import requests
from django.http import HttpResponse
from django.urls import path

def demo(request):
    return HttpResponse("wulala!~")

urlpatterns = [
    path('demo/', demo),
]
