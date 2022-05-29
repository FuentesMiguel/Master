from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView

from .models import*
from .forms import*
# Create your views here.

class Base(TemplateView):
	template_name = "solicitante/base.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Solicitantes'
		context['url'] = 'Solicitantes'
		context['title_body'] = 'Gestionar Solicitantes'
		return context

class SolicitanteListView(ListView):
	model = Solicitante
	context_object_name = 'Solicitante'
	template_name = "solicitante/Lista_Solicitantes.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
	    return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			data = Solicitante.objects.get(request.POST[id]).toJSON()
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(e)



	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['title'] = 'Lista de Solicitantes'
		context['url'] = 'Solicitantes'
		context['title_body'] = 'Listado de Solicitantes'
		context['create_url'] = reverse_lazy('solicitante:Solicitante_Crear')
		context['list_url'] = reverse_lazy('solicitante:Solicitante_Lista')
		return context

class SolicitanteCreateView(CreateView):
	model = Solicitante
	form_class = SolicitanteForm
	template_name = 'solicitante/Solicitante_Form.html'
	success_url = reverse_lazy('solicitante:Solicitante_Lista')

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
		context['title'] = 'Formulario de Solicitante'
		context['url'] = 'Solicitante'
		context['title_body'] = 'Registrar Solicitante'
		context['list_url'] = reverse_lazy('solicitante:Solicitante_Lista')
		context['action'] = 'add'
		return context