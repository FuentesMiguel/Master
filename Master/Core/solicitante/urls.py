from django.urls import path
from .views import*

urlpatterns = [
    path('', Base.as_view(), name ='base'),
    path('Solicitante/lista/', SolicitanteListView.as_view(), name = 'Solicitante_Lista'),
    path('Solicitante/crear/', SolicitanteCreateView.as_view(), name = 'Solicitante_Crear'),
    ]