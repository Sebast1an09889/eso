from django import forms
from .models import Cliente, Auto
from django import forms
from django.contrib.auth.models import User
from .models import Cliente

class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono']  


class RegistroClienteForm(forms.ModelForm):
    username = forms.CharField(required=False)  # Opcional para usuario
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo', 'telefono', 'username', 'password']

    def save(self, commit=True):
        cliente = super().save(commit=False)
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = User.objects.create_user(username=username, password=password)
            cliente.user = user

        if commit:
            cliente.save()
        return cliente


class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = ['numero_serie', 'modelo', 'anio', 'color', 'estado']  
