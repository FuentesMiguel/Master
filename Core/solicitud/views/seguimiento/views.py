from django.http import JsonResponse
from datetime import datetime
from dal import autocomplete
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View, FormView, TemplateView
from django.urls import reverse_lazy

from Core.solicitud.models import *
from Core.solicitud.forms import *


class ListarSeguimientoView(ListView):
    model = Seguimiento
    # Ajusta la plantilla según tu estructura
    template_name = 'seguimiento/seguimiento_Lista.html'

    # Asegúrate de que esta vista requiera el inicio de sesión y los permisos adecuados
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    # Método para manejar las solicitudes POST (puede variar según tu lógica)
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = list(Seguimiento.objects.all().values(
                    'Sembrador_user__id',  # Acceso a campos relacionados
                    'Sembrador_user__username',
                    'Sembrador_user__first_name',
                    'Sembrador_user__last_name',
                    'Sembrador_user__cedula',
                    'nombre_unidad'
                ))
                print(Seguimiento.nombre_unidad)
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Método para obtener los datos del contexto (puede variar según tu lógica)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Seguimientos'
        context['url'] = 'Seguimientos'
        context['title_body'] = 'Listado de Seguimientos'
        context['date_now'] = datetime.now()
        context['create_url'] = reverse_lazy('solicitud:Crear_Seguimiento')
        context['list_url'] = reverse_lazy('solicitud:Listar_Seguimiento')

        return context


class SeguimientoCreateView(CreateView):
    model = Seguimiento
    form_class = SeguimientoForm
    template_name = 'seguimi/seguimi.html'
    success_url = reverse_lazy('user:User_lista')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                if form.is_valid():
                    form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Formulario de Usuarios'
        context['url'] = 'Usuarios'
        context['title_body'] = 'Formulario de Usuarios'
        context['list_url'] = reverse_lazy('user:User_lista')
        context['action'] = 'add'
        return context
