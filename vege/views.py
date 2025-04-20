from django.shortcuts import render,redirect
from .models import *
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout 
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from django.contrib.auth import get_user_model


User = get_user_model()


# Create your views here.

@login_required(login_url="/login/")
def receipes(request):
    if request.method == "POST":
     
        data = request.POST
 
        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')
     
        print(receipe_name)
        print(receipe_desc)  
        print(receipe_img)

        Receipe.objects.create(
            receipe_img = receipe_img,
            receipe_name = receipe_name,
            receipe_desc = receipe_desc,
        )

        return redirect('/receipes/')
    
    queryset = Receipe.objects.filter(is_deleted = False)

    if request.GET.get('search'):
       queryset = queryset.filter(receipe_name__icontains = request.GET.get('search'))


    context = {'receipes' : queryset}
         
    return render(request , 'receipe.html',context)

@login_required(login_url="/login/")
def update_receipe(request , id):
    queryset = Receipe.objects.get(id = id)

    if request.method == "POST":

        data = request.POST

        receipe_img = request.FILES.get('receipe_img')
        receipe_name = data.get('receipe_name')
        receipe_desc = data.get('receipe_desc')

        queryset.receipe_name=receipe_name
        queryset.receipe_desc=receipe_desc

        if receipe_img:
            queryset.receipe_img=receipe_img


        queryset.save()
        return redirect('/receipes/')



    context = {'receipe' : queryset}
    return render(request , 'update_receipe.html',context)

@login_required(login_url="/login/")
def delete_receipe(request , id):
    queryset = Receipe.objects.get(id = id)
    queryset.delete()
    return redirect('/receipes/')


def login_page(request):

    if request.method == "POST":
        
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request,'Invalid Username')
            return redirect('/login/')
        
        user = authenticate(username = username , password = password)

        if user is None:
            messages.error(request , 'Invalid Password')
            return redirect('/login/')
        
        else:
            login(request , user)
            return redirect('/receipes/')
        


    return render(request , 'login.html')
        
def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):

   if request.method == "POST":
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():

            messages.error(request, 'Username already taken')
            return redirect('/register/')
        
        user = User.objects.create(
            first_name = first_name,
            last_name = last_name,
            username = username
        )

        user.set_password(password)
        user.save()

        messages.success(request, 'Account created successfully')

        return redirect('/register/')

        
        
        '''  else:
            user = User.objects.create_user(username=username, password=password)
            messages.success(request, 'Account created successfully')

            login(request, user)
            return redirect('/receipes/') '''
        


   return render(request , 'register.html')     
