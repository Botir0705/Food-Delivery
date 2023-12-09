from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import LogInForm, NewUserForm
from django.contrib import messages
from .models import Category, Restaurant, Food, CartFood
from django.contrib.auth.decorators import login_required


@login_required(login_url='log_in')
def index(request):
    restaurants = Restaurant.objects.all()[::-1]
    cart_items = CartFood.objects.filter(user=request.user)
    total_items = sum([cart_item.quantity for cart_item in cart_items])
     
    return render(request, 'app/index.html', {'restaurants': restaurants, 'total_items': total_items})


@login_required(login_url='log_in')
def restaurant(request, pk):
    restaurant = Restaurant.objects.get(pk=pk)
    foods = Food.objects.filter(restaurant=restaurant)
    categories = Category.objects.all()
    context = {
        'restaurant': restaurant,
        'foods': foods,
        'categories': categories
    }
    return render(request, 'app/detail.html', context)


@login_required(login_url='log_in')
def categories(request, id):
    category = Category.objects.get(id=id)
    category_restaurants = Restaurant.objects.filter(categories=category)
    return render(request, 'app/category.html', {'category_restaurants': category_restaurants, 'category':category})


@login_required(login_url='log_in')
def halal(request):
    return render(request, 'app/halal.html')


@login_required(login_url='log_in')
def cart(request):
    cart_items = CartFood.objects.filter(user=request.user)
    total_price = sum([cart_item.quantity * cart_item.food.price for cart_item in cart_items])
    total_items = sum([cart_item.quantity for cart_item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    }
    return render(request, 'app/cart.html', context)


@login_required(login_url='log_in')
def add_to_cart(request, pk):
    food = Food.objects.get(pk=pk)
    cart_food, created = CartFood.objects.get_or_create(food=food, user=request.user)
    if not created:
        cart_food.quantity += 1
        cart_food.save()
    return redirect('cart')
    

@login_required(login_url='log_in')
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartFood, pk=pk, user=request.user)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


@login_required(login_url='log_in')
def checkout(request):
    cart_items = CartFood.objects.filter(user=request.user)
    total_price = sum([cart_item.quantity * cart_item.food.price for cart_item in cart_items])
    total_items = sum([cart_item.quantity for cart_item in cart_items])
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
        'total_items': total_items
    }
    return render(request, 'app/checkout.html', context)


def sign_up(request):
    form = NewUserForm()
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('log_in')
        else:
                messages.error(request,"Invalid username or password.")
    else:
        messages.error(request, 'Invalid username or password')
    context = {
        'form': form
    }
    return render(request, 'app/sign_up.html', context)
    


def log_in(request):
    form = LogInForm()
    if request.method == 'POST':
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'app/login.html', {'form': form})


def log_out(request):
    logout(request)
    return redirect('log_in')