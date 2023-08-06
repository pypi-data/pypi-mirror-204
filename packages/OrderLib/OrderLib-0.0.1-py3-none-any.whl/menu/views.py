from django.shortcuts import render, redirect, get_object_or_404
from . import models
from django.contrib.auth.models import User
from .models import Cupcake, UserInfo , Newcake
from .forms import CupcakeForm, UserSignUpForm, LoginForm, UserForm, NewcakeForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages, auth
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views import generic
from bootstrap_modal_forms.mixins import PassRequestMixin
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.hashers import make_password
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

# Shared Views

def loginView(request):
    # Define a context dictionary
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/cupcake/list')
        else:
            return HttpResponse ("Username or Password is incorrect!!!")

    return render (request,'login.html')


def registerView(request):
    form = UserForm()
    context = {'form': form}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password = make_password(password)
        a = User.objects.create_user(username, email, password)
        a.save()
        messages.success(request, 'Account was created successfully')
        return render(request,"menu/login.html", context )
    else:
        messages.error(request, 'Registration fail, try again later')
        return render(request,"menu/register.html", context )
        
def logoutView(request):
    logout(request)
    return redirect('/')


def cake_list(request):
    cakes = Cupcake.objects.all().order_by('-createdAt')
    context = {"cakes": cakes}
    return render(request,"menu/list.html",context)

def cupcake_detail(request,pk):
    cake = get_object_or_404(Cupcake,pk=pk)
    context = {"cake": cake}
    return render(request,"menu/detail.html",context)
    
def newcake_detail(request,pk):
    newcake = get_object_or_404(Newcake,pk=pk)
    context = {"newcake": newcake}
    return render(request,"menu/customcake.html",context)# # Create your views here.
    
def new_cake(request):
    if request.method == "POST":
        form = NewcakeForm(request.POST,request.FILES)
        if form.is_valid():
            newcake = form.save(commit=False)
            newcake.createdAt = timezone.now()
            newcake.writer = request.user
            newcake.save()
            return redirect('menu/customcake.html', pk=newcake.pk)
    else:
        form = NewcakeForm()
    context = {'form':form}
    return render(request,"menu/cakes_new.html",context)

@login_required
def cake_new(request):
    current_user = request.user
    if request.method == 'POST':
                name = request.POST.get("name")
                price = request.POST.get("price")
                weight = request.POST.get("weight")
                writer = request.POST.get("writer")
                image = request.POST.get("image")
                writer = request.POST.get("writer")
                print(name)
                print(price)
                print(weight)
                print(writer)
                print(image)
                newcake = Newcake(name=name, price=price, weight=weight,image=image ,writer=writer)
                newcake.save()
                print(newcake)
    return render(request,"menu/cakes_new.html" , {'current_user': current_user})

@login_required
def customcakeView(request):
    if request.user.is_authenticated:
       current_user = request.user
       newcake = Newcake.objects.filter(writer=request.user.id).values()
       return render(request,"menu/ccake.html" , {'newcake' : newcake})
    