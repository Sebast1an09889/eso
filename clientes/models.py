from django.db import models

# Modelo para almacenar la información del cliente
class Cliente(models.Model):
    nombre = models.CharField(max_length=100)  # Nombre del cliente
    correo = models.EmailField(unique=True)    # Correo único
    telefono = models.CharField(max_length=15)  # Teléfono del cliente

    def __str__(self):
        return self.nombre

# Modelo para definir características de un modelo de auto
class Modelo(models.Model):
    modelo = models.CharField(
        max_length=255,
        choices=[
            ('Ford Fiesta', 'Ford Fiesta'),
            ('Ferrari', 'Ferrari'),
            ('Lotus', 'Lotus')
        ],
        default='Ford Fiesta'
    )  # Nombre del modelo del auto
    marca = models.CharField(max_length=255)  # Marca del auto
    año = models.PositiveIntegerField(default=2000)  # Año de fabricación
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del auto

    def __str__(self):
        return self.modelo

# Modelo para representar autos individuales en el sistema
class Auto(models.Model):
    numero_serie = models.CharField(max_length=50, unique=True)  # Número de serie único
    modelo = models.ForeignKey(Modelo, on_delete=models.CASCADE, related_name='autos')  # Relación con el modelo de auto
    anio = models.PositiveIntegerField()  # Año específico del auto
    color = models.CharField(max_length=30)  # Color del auto
    estado = models.CharField(
        max_length=10,
        choices=[('disponible', 'Disponible'), ('vendido', 'Vendido')],
        default='disponible'
    )  # Estado actual del auto

    def __str__(self):
        return f"{self.modelo.modelo} ({self.numero_serie})"

# Modelo para registrar los pedidos realizados por los clientes
class Pedido(models.Model):
    auto = models.OneToOneField('Auto', on_delete=models.CASCADE)  # Auto vendido en el pedido
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, related_name='pedidos')  # Cliente que realiza el pedido
    fecha = models.DateTimeField(auto_now_add=True)  # Fecha en que se realiza el pedido

    def __str__(self):
        return f"Pedido de {self.cliente} - Auto ID: {self.auto.id if self.auto else 'No asignado'}"

# Modelo para los detalles específicos de una compra dentro de un pedido
class DetalleCompra(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name='detalles')  # Relación con el pedido
    auto = models.OneToOneField(Auto, on_delete=models.CASCADE, related_name='detalle_compra')  # Auto comprado
    precio = models.DecimalField(max_digits=10, decimal_places=2)  # Precio del auto
    descuento = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Descuento aplicado

    def __str__(self):
        return f"Detalle {self.id} - Pedido: {self.pedido.id} - Auto: {self.auto.numero_serie}"
