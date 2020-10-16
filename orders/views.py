from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
# PARA PODER RENDERIZAR UNA CADENA COMO UN STRING
from django.template.loader import render_to_string
from django.utils.html import strip_tags  # PARA LA INFORMACION
# NOS PERMITE DEFINIR UNA FUNCION QUE NOS VA A PERMITIR SACAR INFORMACION EN FORMA DE LISTADO
from django.views.generic.list import ListView
from django.views.generic import DetailView
from .models import Order, OrderLine
from cart.cart import Cart

# Create your views here.


def process_order(request):
    order = Order.objects.create(user=request.user, completed=True)
    cart = Cart(request)
    order_lines = list()
    # ITERO POR LOS ITEMS DEL CARRITO Y VOY AGREGANDOLOS A LA VARIABLE order_lines que es una lista
    for key, value in cart.cart.items():
        order_lines.append(
            OrderLine(product_id=key,
                      quantity=value["quantity"],
                      user=request.user,
                      order=order
                      )
        )
    # CREA VARIAS COSAS EN LA BASE DE DATOS EN LUGAR DE IR EN UN BUCLE
    OrderLine.objects.bulk_create(order_lines)

    # TODO ENVIAR CORREO AL CLIENTE
    send_order_email(
        order=order,
        order_lines=order_lines,
        username=request.user.username,
        user_email=request.user.email

    )
    cart.clear()
    messages.success(request, "El pedido se ha creado correctamente")
    return redirect("listado_productos")


def send_order_email(**kwargs):
    subject = "Gracias por tu pedido"
    html_message = render_to_string("orders/nuevo_pedido.html", {
        "order": kwargs.get("order"),
        "order_lines": kwargs.get("order_lines"),
        "username": kwargs.get("username")})
    plain_message = strip_tags(html_message)
    from_email = 'lautitomasalejo@gmail.com'
    to = kwargs.get("user_email")
    send_mail(subject, plain_message, from_email,
              [to], html_message=html_message)
