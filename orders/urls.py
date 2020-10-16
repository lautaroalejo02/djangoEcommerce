from django.urls import path
from .views import *


urlpatterns = [
    path('process_order/', process_order, name='process_order'),


]
