from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Cliente, Modelo, Auto, Pedido, DetalleCompra
from .serializer import ClienteSerializer, ModeloSerializer, AutoSerializer, PedidoSerializer, DetalleCompraSerializer
from .filters import ClienteFilter, AutoFilter
from django.shortcuts import render, get_object_or_404, redirect
#from .models import Cliente, Auto
from .forms import ClienteForm, AutoForm
from django.contrib import messages
#from django.shortcuts import render, get_object_or_404, redirect

# Importaciones necesarias para la exportación en CSV
from django.http import HttpResponse
import csv

#vista para registrocliente
def registro_cliente_view(request):
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cuenta')  # Redirige a la cuenta después del registro
    else:
        form = RegistroClienteForm()
    return render(request, 'registro_cliente.html', {'form': form})


# navbar
def navbar(request):
    return render(request, 'partials/navbar.html')


# Vista para exportar datos completos a un archivo CSV:
def exportar_todo_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="datos_completos.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Correo', 'Teléfono', 'Pedido ID', 'Fecha', 'Auto', 'Modelo', 'Color', 'Estado', 'Precio', 'Descuento'])
    
    # Obtener datos relacionados
    for cliente in Cliente.objects.all():
        for pedido in cliente.pedidos.all():
            for detalle in pedido.detalles.all():
                writer.writerow([
                    cliente.nombre,
                    cliente.correo,
                    cliente.telefono,
                    pedido.id,
                    pedido.fecha,
                    detalle.auto.numero_serie,
                    detalle.auto.modelo.modelo,
                    detalle.auto.color,
                    detalle.auto.estado,
                    detalle.precio,
                    detalle.descuento,
                ])
    return response

#Usuario
def cuenta_view(request):
    # Verificar si el usuario autenticado tiene un cliente asociado
    if request.user.is_authenticated and hasattr(request.user, 'cliente'):
        cliente = request.user.cliente
        clientes = Cliente.objects.filter(id=cliente.id)
    else:
        clientes = Cliente.objects.all()  # Mostrar todos los clientes si no está autenticado

    clientes_con_pedidos = []

    # Relacionar clientes con sus pedidos y autos comprados
    for cliente in clientes:
        pedidos = cliente.pedidos.all()  # Pedidos asociados a este cliente
        autos_comprados = [detalle.auto for pedido in pedidos for detalle in pedido.detalles.all()]
        clientes_con_pedidos.append({
            'cliente': cliente,
            'autos': autos_comprados,
        })

    # Procesar formularios de edición o eliminación (tu lógica actual)
    if request.method == 'POST':
        if 'editar' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            cliente = get_object_or_404(Cliente, id=cliente_id)
            form = ClienteForm(request.POST, instance=cliente)
            if form.is_valid():
                form.save()
                return redirect('cuenta')
        elif 'eliminar' in request.POST:
            cliente_id = request.POST.get('cliente_id')
            cliente = get_object_or_404(Cliente, id=cliente_id)
            cliente.delete()
            return redirect('cuenta')

    return render(request, 'cuenta.html', {'clientes_con_pedidos': clientes_con_pedidos})




def crear_usuario(request):
    autos = Auto.objects.filter(estado='disponible')  # Mostrar solo autos disponibles

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        correo = request.POST.get('correo', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        auto_id = request.POST.get('auto_id')

        # Validar que los campos no estén vacíos
        if not nombre or not correo or not telefono:
            messages.error(request, "Todos los campos son obligatorios.")
            return render(request, 'crear.html', {'autos': autos})

        # Crear el cliente
        cliente = Cliente.objects.create(nombre=nombre, correo=correo, telefono=telefono)

        # Asociar un auto si se selecciona
        if auto_id:
            try:
                auto = Auto.objects.get(id=auto_id, estado='disponible')
                pedido = Pedido.objects.create(cliente=cliente, total=auto.modelo.precio)
                DetalleCompra.objects.create(pedido=pedido, auto=auto, precio=auto.modelo.precio)
                auto.estado = 'vendido'
                auto.save()
                messages.success(request, "Cliente y auto creados correctamente.")
            except Auto.DoesNotExist:
                messages.error(request, "El auto seleccionado no está disponible.")
                cliente.delete()  # Eliminar cliente si el auto falla
                return render(request, 'crear.html', {'autos': autos})

        else:
            messages.success(request, "Cliente creado sin auto asociado.")

        return redirect('cuenta')

    return render(request, 'crear.html', {'autos': autos})


#modificamos para que conecte 
def editar_usuario(request, id):
    cliente = get_object_or_404(Cliente, id=id)

    if request.method == 'POST':
        # Actualizar los datos del cliente
        cliente.nombre = request.POST['nombre']
        cliente.correo = request.POST['correo']
        cliente.telefono = request.POST['telefono']
        auto_id = request.POST.get('auto_id')

        # Asociar un auto si se selecciona
        if auto_id:
            # Verificar si el auto está disponible
            auto = get_object_or_404(Auto, id=auto_id, estado='disponible')
            # Crear un pedido sin el campo 'total'
            pedido = Pedido.objects.create(cliente=cliente, auto=auto)
            # Crear el detalle de la compra
            DetalleCompra.objects.create(pedido=pedido, auto=auto, precio=auto.modelo.precio)
            # Cambiar el estado del auto a 'vendido'
            auto.estado = 'vendido'
            auto.save()

        # Guardar los cambios en el cliente
        cliente.save()
        return redirect('cuenta')

    # Obtener los autos disponibles para mostrarlos en el formulario
    autos = Auto.objects.filter(estado='disponible')
    return render(request, 'editar.html', {'cliente': cliente, 'autos': autos, 'auto_seleccionado': None})


def eliminar_usuario(request, id):
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        return redirect('cuenta')
    return render(request, 'eliminar.html', {'cliente': cliente})

def venta_view(request):
    # Si el usuario está autenticado, usamos el cliente asociado
    if request.user.is_authenticated and hasattr(request.user, 'cliente'):
        cliente = request.user.cliente
    else:
    
        cliente = None

    if request.method == 'POST' and 'comprar' in request.POST:
        auto = get_object_or_404(Auto, id=request.POST.get('auto_id'))
        if cliente:
            pedido = Pedido.objects.create(cliente=cliente, total=auto.modelo.precio)
            DetalleCompra.objects.create(pedido=pedido, auto=auto, precio=auto.modelo.precio)
            auto.estado = 'vendido'
            auto.save()
            return redirect('modelo')
        else:
            return redirect('login') 

    autos = Auto.objects.filter(estado='disponible')
    return render(request, 'modelo.html', {'autos': autos})

#auto
def cancelar_auto(request, id):
    auto = get_object_or_404(Auto, id=id)
    if request.method == 'POST':# asegura de sea una solicitud POST
        auto.delete()# Elimina el auto de base de datos
        return redirect('modelo')  # Redirigir a la lista de autos o vista de venta
    return render(request, 'modelo.html', {'auto': auto})

def compra_view(request):
    autos = Auto.objects.filter(estado='disponible') 
    return render(request, 'compra.html', {'autos': autos})

def modelo_view(request):
    
    autos_disponibles = Auto.objects.filter(estado='disponible')
    autos_vendidos = Pedido.objects.select_related('auto', 'cliente').filter(auto__estado='vendido')
    
    return render(request, 'modelo.html', {
        'autos_disponibles': autos_disponibles,
        'autos_vendidos': autos_vendidos
    })

#agregar auto
def agregar_auto(request):
    if request.method == 'POST':
        form = AutoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('modelo')  # Redirigir a la página de venta después de agregar el auto
    else:
        form = AutoForm()

    return

def editar_auto(request, cliente_id):
    try:
        # Buscar el Pedido asociado al cliente
        pedido = Pedido.objects.get(cliente__id=cliente_id)
        auto = pedido.auto  # Auto relacionado al pedido
    except Pedido.DoesNotExist:
        return HttpResponse(f"No se encontró un Pedido para el cliente con ID: {cliente_id}")

    if request.method == 'POST':
        form = AutoForm(request.POST, instance=auto)
        if form.is_valid():
            form.save()
            return redirect('modelo')  # Redirige a la vista de autos
    else:
        form = AutoForm(instance=auto)

    return render(request, 'editar_auto.html', {'form': form, 'cliente': pedido.cliente})

# ViewSets para la API
class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['nombre', 'correo']

class ModeloViewSet(viewsets.ModelViewSet):
    queryset = Modelo.objects.all()
    serializer_class = ModeloSerializer

class AutoViewSet(viewsets.ModelViewSet):
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    filter_backends = [DjangoFilterBackend]
    # filterset_class = AutoFilter
    filterset_fields = ['modelo__modelo', 'color', 'estado']

class PedidoViewSet(viewsets.ModelViewSet):
    queryset = Pedido.objects.all()
    serializer_class = PedidoSerializer



class DetalleCompraViewSet(viewsets.ModelViewSet):
    queryset = DetalleCompra.objects.all()
    serializer_class = DetalleCompraSerializer
    
