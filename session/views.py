from django.shortcuts import render  ,redirect
from django.contrib.auth import logout , login , authenticate
from .forms import LoginForm , SignUpForm
from django.contrib import messages
from functools import wraps
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# Create your views here.

USER = get_user_model()
group = Group.objects.filter(name = 'Finance Admin')

def isLoggedIn(func):
    @wraps(func)
    def wrapper(request , *args , **kwargs):
        try:
            if request.user.is_authenticated:
                return redirect('home')
        except USER.DoesNotExist:
            pass
        return func(request,*args,**kwargs)
    return wrapper


@isLoggedIn
def Login(request):
    if request.method == 'POST':
        form = LoginForm(data = request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username = username , password = password)
            if user is not None:
                login(request,user)
                messages.success(request,'Login Successful')
                return redirect('home')
            else:
                messages.error(request,'Invalid Username or Password')
    else:
        form = LoginForm()
    return render(request,'login.html',{"form":form})

def Logout(request):
    logout(request)
    return redirect('home')

def SignUp(request):
    if request.method == 'POST':
        form = SignUpForm(data = request.POST,files = request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            user.groups.add(group)
            messages.success(request,'Successfully created your account ')
            return redirect('home')
        else:
            messages.error(request,'Please correctly fillup this form')
        print(form.cleaned_data , form.errors)
    else:
        form = SignUpForm()
    
    return render(request,'signup.html',{"form":form})


        
