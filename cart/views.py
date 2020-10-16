from django.shortcuts import render, redirect
from products.models import Product
from django.contrib.auth.decorators import login_required
from .cart import Cart
# Create your views here.


def add_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('listado_productos')


def add(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.add(product=product)
    return redirect('cart:pedidos')


def remove_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.remove(product)
    return redirect('cart:pedidos')


def decrement_product(request, product_id):
    cart = Cart(request)
    product = Product.objects.get(id=product_id)
    cart.decrement(product=product)
    return redirect('cart:pedidos')


def clear_cart(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:pedidos')


def pedidos(request):
    return render(request, "cart/pedidos.html")
