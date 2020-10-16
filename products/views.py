from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Product
from cart.cart import Cart
# Create your views here.
# @login_required(login_url='/accounts/login')


def listado_productos(request):
    cart = Cart(request)
    products = Product.objects.all()
    return render(request, "products/listado.html", {"products": products})
