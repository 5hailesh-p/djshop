from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def sign_in(request):

    if request.method == 'POST':
        email = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username= email, password= pass1)

        if user is not None:
            login(request, user)
        else:
            messages.error('bad credentials ')

    return render(request,'auth/signin.html')

def sign_up(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # if pass1 == pass2:

        print(email, full_name)

        new_user = User.objects.create_user(email,pass1)
        new_user.username = email
        new_user.first_name = full_name

        new_user.save()
        messages.success(request, "your account is created ")
        redirect('auth/signin')

    return render(request,'auth/signup.html' )


def dash(request):
    return render(request,'index.html')

def sign_out(request):
    return render(request,'index.html')
