from django import forms
from .models import Post
class FormularioContacto(forms.Form):

    asunto = forms.CharField()
    email = forms.EmailField()
    mensaje = forms.CharField()
class FormularioPost(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('categoria','titulo','contenido','imagen')
        