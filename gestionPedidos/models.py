from django.db import models
from django.contrib.auth.models import User #REPRESENTA AUTH USER
import os
# Create your models here.
# Django le da un enfoque totalmente orientado a POO
# Debemos crear clases por cada tabla

class Clientes(models.Model):
    #campos y tipos de datos de table
    nombre=models.CharField(max_length=30)
    direccion = models.CharField(max_length=50 , verbose_name="La direccion")#Con verbose elegimos como queremos que se muestre el campo en el panel de administracion
    email = models.EmailField(blank=True,null=True)
    tfno = models.CharField(max_length = 12)

    def __str__(self):
        return self.nombre

class Articulos(models.Model):
    nombre = models.CharField(max_length=30)
    seccion = models.CharField(max_length=20)
    precio = models.IntegerField()
    imagen = models.ImageField(upload_to='servicios') #Elijo la carpeta donde guardar las imagenes si no existe esa carpeta django la creara

    def __str__(self): #Con esto ya en la consola nos va a devolver la tupla con valores en formato string y no solo un objeto
        return self.nombre
class Pedidos(models.Model):
    numero = models.IntegerField()
    fecha = models.DateField()
    precio = models.IntegerField(default=0)
    entregado = models.BooleanField()
    producto = models.ForeignKey(Articulos,null=True,on_delete=models.SET_NULL)
    customer = models.ForeignKey(Clientes,null=True,on_delete=models.SET_NULL)
  
    
class Categoria(models.Model):
    nombre= models.CharField(max_length=100,null=False,unique=True,verbose_name='Nombre')
    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'categorias'
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['id']
class Post(models.Model):
    autor = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE)
    titulo = models.CharField(max_length = 100,null=False,verbose_name='Titulo')
    contenido = models.TextField(verbose_name='Contanos que te parecio')
    imagen = models.ImageField(upload_to='servicios/%Y/%m/%d',null=True,blank=True,verbose_name='Subi una foto del producto!')
    fecha_alta = models.DateTimeField(auto_now_add=True,verbose_name='Fecha alta')
    def delete(self,*args,**kwargs): #ELIMINAR IMAGEN AL ELIMINAR UN REGISTRO QUE CONTENGA UNA 
        if os.path.isfile(self.imagen.path):
            os.remove(self.imagen.path)
        super(Post,self).delete(*args,**kwargs)
    def __str__(self):
        return self.titulo
    class Meta:
        db_table = 'posts'
        verbose_name = 'Post'
        verbose_name_plural = 'Posts'
        ordering = ['id']