
from django.contrib.auth import login,logout,authenticate
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import *


def home(request):
    
    books = Book.objects.all()
    context = {'books': books}
    
    if request.user.is_staff:
        
        return render(request, 'book/adminhome.html', context)
    
    else:
        
        return render(request, 'book/home.html', context)
    

def logoutPage(request):
    
    logout(request)
    
    return redirect('/')


def loginPage(request):
    
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
    if user is not None:
        
        print('Working')
        login(request, user)
        
        return redirect('/')
    
    context = {}
    
    return render(request, 'book/login.html', context)


def registerPage(request):
    
    form = CreateUserForm()
    customer_form = CreateCustomerForm()
    
    if request.method.method == 'POST':
        
        form = CreateUserForm(request.POST)
        customer_form = CreateCustomerForm(request.POST)
        
        if form.is_valid() and customer_form.is_valid():
            
            user = form.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            
            return redirect('login')
    
    context = {'form': form, 'customer_form': customer_form}
    
    return render(request, 'book/register.html', context)


def addbook(request):
    
    form = CreateBookForm()
    
    if request.method == 'POST':
        
        form = CreateBookForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
        return redirect('/')
    
    context = {'form' : form}
    
    return render(request, 'book/addbook.html', context)


def viewcart(request):
    
    customers = Customer.objects.filter(user = request.user)

    for customer in customers:
        
        carts = Cart.objects.all()

        for cart in carts:
            if (cart.customer == customer):

                context = {'cart' : cart}

                return render(request, 'book/viewcart.html', context)

        return render(request, 'book/emptycart.html')
    
    
def addtocart(request, primary_key):
    
    book = Book.objects.get(id = primary_key)
    customers = Book.objects.filter(user = request.user)
    request_cart = ''
    
    for c in customers:

        carts = Cart.objects.all()
        
        for cart in carts:
            
            if (cart.customer == c):
                
                request_cart = cart
                
                break
         
        if (request_cart == ''):
            
            request_cart = Cart.objects.create(customer = c)
        
        request_cart.book.add(book)
    
    return redirect('/')
        
            
        





