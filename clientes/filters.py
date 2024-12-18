from django_filters import rest_framework as filters
from .models import Cliente, Auto

class ClienteFilter(filters.FilterSet):
    # Filtros para buscar clientes por nombre o correo.
    nombre = filters.CharFilter(lookup_expr='icontains')
    correo = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Cliente
        fields = ['nombre', 'correo']

class AutoFilter(filters.FilterSet):
    # Filtros para buscar autos por modelo, color o estado.
    modelo = filters.CharFilter(field_name='modelo__modelo', lookup_expr='icontains')
    color = filters.CharFilter(lookup_expr='icontains')
    estado = filters.ChoiceFilter(choices=[('disponible', 'Disponible'), ('vendido', 'Vendido')])

    class Meta:
        model = Auto
        fields = {'modelo': ['exact'],
                'color': ['icontains'],
                'estado': ['exact'],}
