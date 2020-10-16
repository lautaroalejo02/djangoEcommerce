from django.urls import path
from authentication import views
from .views import *
urlpatterns=[
    path('registro/',VistaRegistro.as_view(),name="registro"),
    path('login/',acceder,name="login"),
    path('hola/',views.hola),
    path('salir/',salir,name="salir"),
]