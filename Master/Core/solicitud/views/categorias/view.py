from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import *

from Core.solicitud.models import*
from Core.solicitud.forms import*
# Create your views here.


class CategoriasListView(ListView):
	model = Categorias
	context_object_name = 'Categorias'
	template_name = "solicitud/Lista_Categorias.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			data = Categorias.objects.get(request.POST[id]).toJSON()
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(e)


	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lista de Categorias'
		context['url'] = 'Categorias'
		context['title_body'] = 'Listado de Tipos de Solicitudes'
		context['create_url'] = reverse_lazy('solicitud:Categorias_crear')
		context['list_url'] = reverse_lazy('solicitud:Categorias_lista')

		return context


class CategoriasCreateView(CreateView):
	model = Categorias
	form_class = CategoriasForm
	template_name = 'solicitud/Categorias_Form.html'
	success_url = reverse_lazy('solicitud:Categorias_lista')

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
		context['title'] = 'Formulario de Categorias'
		context['url'] = 'Categorias'
		context['title_body'] = 'Crear una Categotia'
		context['list_url'] = reverse_lazy('solicitud:Categorias_lista')
		context['action'] = 'add'
		return context


class CategoriasUpdateView(UpdateView):
	model = Categorias
	form_class = CategoriasForm
	template_name = 'solicitud/Categorias_Form.html'
	success_url = reverse_lazy('solicitud:Categorias_lista')

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
		context['title'] = 'Editar Categorias'
		context['url'] = 'Categorias'
		context['title_body'] = 'Actualizar una Categotia'
		context['list_url'] = reverse_lazy('solicitud:Categorias_lista')
		context['action'] = 'edit'
		return context


class CategoriasDeleteView(DeleteView):
	model = Categorias
	template_name = 'solicitud/Categorias_Delete.html'
	success_url = reverse_lazy('solicitud:Categorias_lista')

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
		context['title'] = 'Eliminar Categorias'
		context['url'] = 'Categorias'
		context['title_body'] = 'Crear una Categotia'
		context['list_url'] = reverse_lazy('solicitud:Categorias_lista')
		return context


