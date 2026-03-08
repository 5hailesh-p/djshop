from django.shortcuts import render,redirect
from django.http import HttpResponse

# Create your views here.
def payment(request): 
    return HttpResponse('this is payment page')