from django.urls import path
from Core.solicitud.views.categorias.view import *
from Core.solicitud.views.solicitud.view import *

urlpatterns = [
    path('', Base.as_view(), name ='base'),
    path('Solicitud/lista/', SolicitudesListView.as_view(), name = 'Solicitudes_lista'),
    path('Solicitud/add/', SolicitudesCreateView.as_view(), name = 'Solicitudes_crear'),
    path('Solicitud/update/<int:pk>', SolicitudesUpdateView.as_view(), name = 'Solicitudes_editar'),
    path('Solicitud/delete/<int:pk>', SolicitudesDeleteView.as_view(), name = 'Solicitudes_eliminar'),
    path('Categorias/lista/', CategoriasListView.as_view(), name = 'Categorias_lista'),
    path('Categorias/add/', CategoriasCreateView.as_view(), name = 'Categorias_crear'),
    path('Categorias/update/<int:pk>', CategoriasUpdateView.as_view(), name = 'Categorias_editar'),
    path('Categorias/delete/<int:pk>', CategoriasDeleteView.as_view(), name = 'Categorias_eliminar'),
]
