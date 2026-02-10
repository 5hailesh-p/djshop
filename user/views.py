from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from .forms import SignupForm
# Create your views here.

def sign_in(request):
    return render(request,'auth/signin.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user)
            return redirect('/')
    else:
        form = SignupForm()

    return render(request,'auth/signup.html',{'form':form})


def dash(request):
    return render(request,'index.html')

def sign_out(request):
    return render(request,'index.html')
