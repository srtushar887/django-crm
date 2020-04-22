from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout

# Create your views here.

from .models import *
from .forms import OrderForm,CreateUserForm
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_users,admin_only

@unauthenticated_user
def loginPage(request):
        if request.method == 'POST':
            username =request.POST.get('username')
            password =request.POST.get('password')
            
            user = authenticate(request, username=username,password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request,'Username or password is incorrect')
                return redirect('loginPage')
        else:
            return render(request,'accounts/login.html')

@unauthenticated_user
def register(request):
    if request.user.is_authenticated():
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = UserCreationForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                gorup = Group.objects.get(name='customer')
                user.groups.add(gorup)
                messages.success(request,'Account was created For' + user)
                return redirect('login')

    context = {
       'form' : form
    }
    return render(request,'accounts/register.html',context)


def logoutUser(request):
    logout(request)
    return redirect('loginPage')

@login_required(login_url='loginPage')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    
    total_customer = customers.count()
    total_order = orders.count()
    deliver = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    context = {
        'orders' : orders,
        'customers' : customers,
        'total_customer': total_customer,
        'total_order' : total_order,
        'deliver':deliver,
        'pending':pending

    }
    return render(request,'accounts/dashboard.html',context)
@login_required(login_url='loginPage')
def products(request):
    products = Product.objects.all();
    return render(request,'accounts/products.html',{'products':products})
@login_required(login_url='loginPage')
def customer(request,pk_test):
    customer = Customer.objects.get(id=pk_test)

    orders = customer.order_set.all()
    order_count = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context ={
        'customer' : customer,
        'orders':orders,
        'order_count':order_count,
        'myFilter' : myFilter
    }
    return render(request,'accounts/customer.html',context)
@login_required(login_url='loginPage')
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form = OrderForm(initial={'customer' : customer})
    if request.method == 'POST':
       # form = OrderForm(request.POST)
       formset = OrderFormSet(request.POST,instance=customer)
       if formset.is_valid():
           formset.save()
           return redirect('home')

    context = {

        'formset':formset
    }
    return render(request, 'accounts/order_form.html',context)
@login_required(login_url='loginPage')
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
       form = OrderForm(request.POST,instance=order)
       if form.is_valid():
           form.save()
           return redirect('home')

    context = {
        'form': form
    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='loginPage')
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)


    if request.method == 'POST':
        order.delete()
        return redirect('home')


    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)