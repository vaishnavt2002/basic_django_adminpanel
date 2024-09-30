from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth import logout
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache



# Create your views here.
@never_cache
def user_login(request):
    if request.user.is_superuser:
        return redirect(admin_home) 
    elif request.user.is_authenticated:
        return redirect(user_home)
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

@never_cache
def user_signup(request):
    if request.user.is_superuser:
        return redirect(admin_home) 
    elif request.user.is_authenticated:
        return redirect(user_home)
        
    if request.POST:
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if User.objects.filter(username=uname).exists():
                user_data = {'username': uname, 'email': email}
                return render(request, 'signup.html', {'errors': 'Username already exists', 'userdata': user_data})
        elif User.objects.filter(email=email).exists():
                user_data = {'username': uname, 'email': email}
                return render(request, 'signup.html', {'errors': 'Email already exists', 'userdata': user_data})
        if password!=confirm_password:
            user_data = {'username': uname, 'email': email}
            return render(request,'signup.html',{'errors':'password is not matching','userdata': user_data})
        else:
            try:
                validate_password(password)
            except ValidationError as e:
                user_data = {'username': uname, 'email': email}
                return render(request, 'signup.html', {'password_error': e.messages,'userdata': user_data})
            my_user=User.objects.create_user(uname,email,password)
            my_user.save()
            return redirect('login')
    return render(request,'signup.html')

@never_cache
def user_home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return render(request,'home.html')
    else:
        return redirect(user_login)

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')

@never_cache
def admin_home(request):
    if request.user.is_superuser:
        if request.method == 'GET':
            search = request.GET.get('searchvalue', '')
            if search:
                users = User.objects.filter(is_superuser=False, username__icontains=search)
            else:
                users = User.objects.filter(is_superuser=False)
        
        return render(request, 'admin.html', {'users': users,'search':search})
    
    elif request.user.is_authenticated:
        return redirect(user_home)
    else:
        return redirect(user_login)


@never_cache
def admin_user_edit(request,id):
    if request.user.is_superuser:
        user_details=User.objects.get(id=id)
        return render(request,'adminedit.html',{'user_details':user_details})
    elif request.user.is_authenticated:
        return redirect(user_home)
    else:
        return redirect(user_login)

def admin_user_edit_post(request):
    if request.user.is_superuser:
        if request.POST:
            id=request.POST.get('id')
            username=request.POST.get('username')
            email=request.POST.get('email')
            user_details=User.objects.get(id=id)
            user_details.username=username
            user_details.email=email
            user_details.save()
            return redirect(admin_home)
    elif request.user.is_authenticated:
        return redirect(user_home)
    else:
        return redirect(user_login)
        
@never_cache
def admin_add_user(request):
    if request.user.is_superuser:
        if request.POST:
            uname=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            confirm_password=request.POST.get('confirm_password')
            if User.objects.filter(username=uname).exists():
                user_data = {'username': uname, 'email': email}
                return render(request, 'adminadd.html', {'errors': 'Username already exists', 'userdata': user_data})
            elif User.objects.filter(email=email).exists():
                user_data = {'username': uname, 'email': email}
                return render(request, 'adminadd.html', {'errors': 'Email already exists', 'userdata': user_data})
            if password!=confirm_password:
                user_data={'username':uname,'email':email}
                return render(request,'adminadd.html',{'errors':'password is not matching','userdata':user_data})
            else:
                try:
                    validate_password(password)
                except ValidationError as e:
                    user_data={'username':uname,'email':email}
                    return render(request, 'adminadd.html', {'password_error': e.messages,'userdata':user_data})
                my_user=User.objects.create_user(uname,email,password)
                my_user.save()
                return redirect(admin_home)
        
        return render(request,'adminadd.html')
    elif request.user.is_authenticated:
        return redirect(user_home)
    else:
        return redirect(user_login)
    
@never_cache
def admin_delete_user(request,id):
    if request.user.is_superuser:
        user_details=User.objects.get(id=id)
        user_details.delete()
        return redirect(admin_home)
    elif request.user.is_authenticated:
        return redirect(user_home)
    else:
        return redirect(user_login)
