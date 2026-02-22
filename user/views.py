from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
# Create your views here.

def sign_in(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        email = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username= email, password= pass1)
        if user is not None:
            login(request, user) 
            messages.success(request, "Logged in Successfully ") 
            return redirect('/')
        else:
            messages.error(request,'bad credentials ')
            return redirect("signin")
    else:
        return render(request,'auth/signin.html')

def sign_up(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        
        if pass1 != pass2:
           messages.warning(request, "password not match")
           return redirect('/auth/signup')
        elif User.objects.filter(email=email) :
            messages.error(request, "Email Already Exist")
            return redirect('/auth/signup')
        else:
            new_user = User.objects.create_user(username=email,email=email, password=pass1)
            
            new_user.first_name = full_name

            new_user.save()
            messages.success(request, "your account is created ")
            return redirect('/auth/signin')
    else:
        return render(request,'auth/signup.html' )


def dash(request):
    return redirect('home')

def sign_out(request):
    logout(request)
    messages.success(request,"Logged Out")
    return redirect('/auth/signin')
