from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import logout

def user_logout(request):
    logout(request)
    return redirect('login')
from django.contrib.auth.decorators import login_required
# Create your views here.
def user_login(request):
    if request.POST:
        uname=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=uname,password=password)
        if user is not None:
            login(request,user)
            if request.user.is_superuser:
                return redirect(admin_home)
            else:
                return redirect('home')
        else:
            return render(request,'login.html',{'error':'invalid username or password'})
    return render(request,'login.html')

def user_signup(request):
    if request.POST:
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password!=confirm_password:
            return render(request,'signup.html',{'error':'password is not matching'})
        else:
            my_user=User.objects.create_user(uname,email,password)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')

@login_required(login_url='/')
def user_home(request):
    return render(request,'home.html')

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required(login_url='/')
def admin_home(request):
    if request.user.is_superuser:
        users = User.objects.filter(is_superuser=False)
        return render(request,'admin.html',{'users':users})

def admin_user_edit(request,id):
    if request.user.is_superuser:
        user_details=User.objects.get(id=id)
        return render(request,'adminedit.html',{'user_details':user_details})

def admin_user_edit_post(request):
    if request.user.is_superuser:
        if request.POST:
            id=request.POST.get('id')
            print(id)
            username=request.POST.get('username')
            print(username)
            email=request.POST.get('email')
            user_details=User.objects.get(id=id)
            user_details.username=username
            user_details.email=email
            user_details.save()
            return redirect(admin_home)
    