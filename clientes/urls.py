from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import editar_auto, registro_cliente_view, ClienteViewSet, ModeloViewSet, AutoViewSet, PedidoViewSet, DetalleCompraViewSet,cuenta_view, venta_view, exportar_todo_csv,crear_usuario, editar_usuario, eliminar_usuario, compra_view, modelo_view, navbar, agregar_auto, cancelar_auto, venta_view, modelo_view, exportar_todo_csv
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
#from .views import agregar_auto, cancelar_auto, venta_view, modelo_view, exportar_todo_csv

# Configuración del router para la API REST.
router = DefaultRouter()
router.register('clientes', ClienteViewSet)
router.register('modelo', ModeloViewSet)
router.register('Auto', AutoViewSet)
router.register('pedidos', PedidoViewSet)
router.register('detalles_compra', DetalleCompraViewSet)


urlpatterns = [
    # Rutas API REST
    path('api/', include(router.urls)),

    #navbar
    path('partials/', navbar, name='navbar' ),


    # Vistas de cuenta y venta
    path('cuenta/', cuenta_view, name='cuenta'),
    path('venta/', venta_view, name='venta'),

    #Cliente
    path('crear/', crear_usuario, name='crear_usuario'),
    path('editar/<int:id>/', editar_usuario, name='editar_usuario'),
    path('eliminar/<int:id>/', eliminar_usuario, name='eliminar_usuario'),
    path('registro/', registro_cliente_view, name='registro_cliente'),

    #Auto
    path('cancelar/<int:id>/', cancelar_auto, name='cancelar_auto'),
    path('modelo/', modelo_view, name='modelo'),  # Vista principal para autos disponibles
    #path('compra/', compra_view, name='compra'),  # Historial de compras
    #path('autos/agregar/', agregar_auto, name='agregar_auto'),
    path('editar/auto/<int:cliente_id>/', editar_auto, name='editar_auto'),
    # Exportar datos a CSV
    path('exportar_datos/', exportar_todo_csv, name='exportar_datos'),

    # Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
