from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate

# Create your views here.

# def registro(request):
#     return render(request,"registro.html")


def acceder(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            usuario = authenticate(username=nombre, password=password)
            if usuario is not None:
                login(request, usuario)
                messages.success(request, F"Bienvenido de nuevo {nombre}")
                return redirect("listado_productos")
            else:
                messages.error(request, "Los datos son incorrectos")
        else:
            messages.error(request, "Los datos son incorrectos")

    form = AuthenticationForm()
    return render(request, "login.html", {"form": form})


class VistaRegistro(View):
    # noinspection PyMethodMayBeStatic
    def get(self, request):
        form = UserCreationForm()
        return render(request, "registro.html", {"form": form})
    # noinspection PyMethodMayBeStatic

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            nombre = form.cleaned_data.get("username")
            messages.success(request, F"Bienvenido a la plataforma {nombre}")
            login(request, usuario)
            return render(request, "hola.html")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])
            return render(request, "registro.html", {"form": form})


def hola(request):
    return render(request, "hola.html")


def salir(request):
    logout(request)
    messages.success(request, F"Tu sesion se ha cerrado correctamente")
    return render(request, "products/listado.html")
