from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from Core.solicitud.models import*
from Core.solicitud.forms import*
# Create your views here.

class Base(TemplateView):
	template_name = "solicitud/base.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Solicitudes'
		context['url'] = 'Solicitudes'
		context['title_body'] = 'Gestionar Solicitudes'
		return context


class SolicitudesListView(ListView):
	model = Solicitudes
	context_object_name = 'Solicitudes'
	template_name = "solicitud/Lista_Solicitudes.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			data = Solicitudes.objects.get(request.POST[id]).toJSON()
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(e)

	    
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lista de Solicitudes'
		context['url'] = 'Solicitudes'
		context['title_body'] = 'Listado de Solicitudes'
		context['create_url'] = reverse_lazy('solicitud:Solicitudes_crear')
		context['list_url'] = reverse_lazy('solicitud:Solicitudes_lista')
		return context


class SolicitudesCreateView(CreateView):
	model = Solicitudes
	form_class = SolicitudesForm
	template_name = 'solicitud/Solicitudes_Form.html'
	success_url = reverse_lazy('solicitud:Solicitudes_lista')

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'add':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Formulario de Solicitudes'
		context['url'] = 'Solicitudes'
		context['title_body'] = 'Crear una Solicitud'
		context['list_url'] = reverse_lazy('solicitud:Solicitudes_lista')
		context['action'] = 'add'
		return context

class SolicitudesUpdateView(UpdateView):
	model = Solicitudes
	form_class = SolicitudesForm
	template_name = 'solicitud/Solicitudes_Form.html'
	success_url = reverse_lazy('solicitud:Solicitudes_lista')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']
			if action == 'edit':
				form = self.get_form()
				data = form.save()
			else:
				data['error'] = 'No ha ingresado a ninguna opción'
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Editar Solicitud'
		context['url'] = 'Solicitudes'
		context['title_body'] = 'Actulizar una Solicitud'
		context['list_url'] = reverse_lazy('solicitud:Solicitudes_lista')
		context['action'] = 'edit'
		return context

class SolicitudesDeleteView(DeleteView):
	model = Solicitudes
	template_name = 'solicitud/Solicitudes_Delete.html'
	success_url = reverse_lazy('solicitud:Solicitudes_lista')

	def dispatch(self, request, *args, **kwargs):
		self.object = self.get_object()
		return super().dispatch(request, *args, **kwargs)


	def post(self, request, *args, **kwargs):
		data = {}
		try:
			self.object.delete()
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Eliminar Solicitudes'
		context['url'] = 'Solicitudes'
		context['title_body'] = 'Eliminar una Solicitud'
		context['list_url'] = reverse_lazy('solicitud:Solicitudes_lista')
		return context


