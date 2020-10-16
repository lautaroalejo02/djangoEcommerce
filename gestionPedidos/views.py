from django.shortcuts import render, redirect
from django.http import HttpResponse
from gestionPedidos.models import Articulos, Post
from django.core.mail import send_mail
from django.conf import settings
from gestionPedidos.forms import FormularioContacto, FormularioPost
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
# Create your views here.


def busqueda_productos(request):
    return render(request, "busqueda_productos.html")


def buscar(request):
    if(request.GET["producto"]):

        mensaje = "Articulo buscado: %r" % request.GET["producto"]
        prd = request.GET["producto"]
        if len(prd) > 20:
            mensaje = "Texto demasiado largo"
        else:
            articulos = Articulos.objects.filter(nombre__icontains=prd)
            return render(request, "resultados_busqueda.html", {"articulos": articulos, "query": prd})
    else:
        mensaje = "No has introducido nada"
    return HttpResponse(mensaje)


def crearArticulo(request):
    nombre = request.POST["nombre"]
    seccion = request.POST["seccion"]
    precio = request.POST["precio"]
    art = Articulos.objects.create(
        nombre=nombre, seccion=seccion, precio=precio)
    return render(request, "busqueda_productos.html")


def contacto(request):
    if request.method == "POST":
        miFormulario = FormularioContacto(request.POST)
        if miFormulario.is_valid():
            infoForm = miFormulario.cleaned_data
            send_mail(infoForm['asunto'], infoForm['mensaje'], infoForm.get(
                'email', ''), ['lautitomasalejo@gmail.com'],)
            return render(request, "gracias.html")
    else:
        miFormulario = FormularioContacto()

    return render(request, "formulario_contacto.html", {"form": miFormulario})
# def contacto(request):
#     if request.method=="POST":
#         subject = request.POST["asunto"]
#         message = request.POST["mensaje"] + "" + request.POST["email"]
#         email_from = settings.EMAIL_HOST_USER
#         recipient_list=["lautitomasalejo@gmail.com"]
#         send_mail(subject,message,email_from,recipient_list)
#         return render(request,"gracias.html")
#     return render(request,"contacto.html")


def todos(request):
    articulos = Articulos.objects.all()
    return render(request, "ver_todos.html", {"articulos": articulos})


def index(request):
    return render(request, "index.html")


@login_required(login_url='/accounts/login')
def feedback(request):
    posts1 = Post.objects.all()
    paginator = Paginator(posts1, 3)  # paginacion
    pagina = request.GET.get("page") or 1  # obteniendo la pagina
    posts = paginator.get_page(pagina)  # obtengo los posts en la paina
    current_page = paginator.get_page(pagina)  # Pagina actual
    current_page = int(pagina)
    # MAS 1 PORQUE EL ULTIMO SE EXCLUYE //rango de paginas para ver cuantas hay
    paginas = range(1, posts.paginator.num_pages + 1)
    if request.method == "POST":
        form = FormularioPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.autor_id = request.user.id
            post.save()
            titulo = form.cleaned_data.get("titulo")
            messages.success(request, F"Tu post ha sido creado correctamente")
            return redirect("feedback")
        else:
            for msg in form.error_messages:
                messages.error(request, form.error_messages[msg])

    form = FormularioPost()
    return render(request, "feedback.html", {"form": form, "posts": posts, "paginas": paginas, "current_page": current_page})


def crear_post(request):
    form = FormularioPost()
    return render(request, "crear_post.html", {"form": form})


def eliminar_post(request, post_id):

    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        messages.error(request, "El post no existe")
        return redirect("feedback")
    if post.autor != request.user:
        messages.error(request, "No eres el autor de este post")
        return redirect("feedback")
    post.delete()
    messages.error(request, "EL post ha sido eliminado")
    return redirect("feedback")


def home(request):
    return redirect("listado_productos")
