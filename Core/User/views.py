from datetime import datetime
from django.http import JsonResponse

from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group

from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import (CreateView, DeleteView, FormView,
                                  ListView, TemplateView, UpdateView, View)
from django.views.decorators.csrf import csrf_protect
from Core.mixins import *
from Core.User.forms import *
from Core.User.models import *
from Core.User.utils import get_user_tecnico

# Create your views here.


class UserListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = User
    permission_required = 'view_user'
    template_name = "usuario/Usuarios_lista.html"

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in User.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)

                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios'
        context['url'] = 'Usuarios'
        context['title_body'] = 'Listado de Usuarios'
        context['date_now'] = datetime.now()
        context['create_url'] = reverse_lazy('user:User_crear')
        context['list_url'] = reverse_lazy('user:User_lista')

        return context


class UserCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/Usuarios_form.html'
    permission_required = 'add_user'
    success_url = reverse_lazy('user:User_lista')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Formulario de Usuarios'
        context['url'] = 'Usuarios'
        context['title_body'] = 'Formulario de Usuarios'
        context['list_url'] = reverse_lazy('user:User_lista')
        context['action'] = 'add'
        return context

    def update(self):
        pass


class UserUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = User
    form_class = UserForm
    template_name = 'usuario/Usuarios_form.html'
    permission_required = 'change_user'
    success_url = reverse_lazy('user:User_lista')

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
        context['title'] = 'Editar de Usuarios'
        context['url'] = 'Usuarios'
        context['title_body'] = 'Editar Usuarios'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = User
    template_name = 'usuario/Usuarios_delete.html'
    permission_required = 'delete_user'
    success_url = reverse_lazy('user:User_lista')

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
        context['title'] = 'Eliminar de Usuarios'
        context['url'] = 'Usuarios'
        context['title_body'] = 'Eliminar un Usuario'
        context['list_url'] = reverse_lazy('user:User_lista')
        return context


class UserChangeGropus(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk'])
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('app:dashboard'))


class UserProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'usuario/Profile.html'
    success_url = reverse_lazy('app:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

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
        context['title'] = 'Editar Perfil'
        context['url'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class UserChangePasswordView(LoginRequiredMixin, FormView):
    model = User
    form_class = PasswordChangeForm
    template_name = 'usuario/Change_password.html'
    success_url = reverse_lazy('login:login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['class'] = 'form-control'
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['class'] = 'form-control'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['class'] = 'form-control'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Password'
        context['url'] = 'Password'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


# USUARIOS SEMBRADORES

class DashboardS(LoginRequiredMixin, TemplateView):
    template_name = 'sembrador/Profiles.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil del Sembrador'
        context['title_body'] = 'Perfil'

        context['user_is_sembrador'] = self.request.user.groups.filter(
            name='Sembradores').exists()
        return context


class ListarSembradorView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):

    model = Sembradores
    template_name = 'sembrador/Sembrador_lista.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for sembrador in Sembradores.objects.all():
                    item = sembrador.toJSON()

                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)

        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Lista de Sembradores'
        context['date_now'] = datetime.now()
        context['create_url'] = reverse_lazy('user:Sembrador_crear')

        return context


class CrearSembradorView(CreateView):
    model = Sembradores
    form_class = SembradorCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('login:login')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

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
        context['title'] = 'Formulario del Sembrador'
        context['title_body'] = 'Formulario del Sembrador'
        context['list_url'] = reverse_lazy('login:login')
        context['action'] = 'add'

        return context

    def update(self):
        pass


class SembradorProfileView(UpdateView):
    model = Sembradores
    form_class = SembradorProfileForm
    template_name = 'form.html'
    success_url = reverse_lazy('app:dashboard')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        response_data = {'success': True}

        try:
            sembrador = Sembradores.objects.get(pk=request.user.id)
            sembrador.cedula = data['cedula']
            sembrador.cedula_agraria = data['cedula_agraria']
            sembrador.codigo_asonaproyuca = data['codigo_asonaproyuca']
            sembrador.telefono_personal = data['telefono_personal']
            sembrador.telefono_casa = data['telefono_casa']
            sembrador.direccion = data['direccion']
            sembrador.fecha_nacimiento = datetime.strptime(
                data['fecha_nacimiento'], '%Y-%m-%d')
            sembrador.edad = data['edad']
            sembrador.estado_civil = data['estado_civil']
            sembrador.profesion_ocupacion = data['profesion_ocupacion']
            sembrador.sexo = data['sexo']
            sembrador.logue_complete = True

            # NUEVOS CAMPOS
            # sembrador.google_maps_url = data['google_maps_url']

            # sembrador.estado = data['estado']
            # sembrador.municipio = data['municipio']
            # sembrador.parroquia = data['parroquia']

            # sembrador.nombre_unidad = data['nombre_unidad']

            # Datos del Conyuge
            sembrador.conyuge_nombre = data['conyuge_nombre']
            sembrador.conyuge_apellido = data['conyuge_apellido']
            sembrador.conyuge_cedula = data['conyuge_cedula']
            sembrador.conyuge_edad = data['conyuge_edad']
            sembrador.conyuge_sexo = data['conyuge_sexo']
            sembrador.conyuge_telefono_fijo = data['conyuge_telefono_fijo']
            sembrador.conyuge_telefono_celular = data['conyuge_telefono_celular']

            # Datos de la dircción de Habitación
            sembrador.direccion_habitacion_estado = data['direccion_habitacion_estado']
            sembrador.direccion_habitacion_municipio = data['direccion_habitacion_municipio']
            sembrador.direccion_habitacion_parroquia = data['direccion_habitacion_parroquia']
            sembrador.direccion_habitacion_caserio = data['direccion_habitacion_caserio']
            sembrador.direccion_habitacion_sector = data['direccion_habitacion_sector']
            sembrador.direccion_habitacion_ciudad_cercana = data['direccion_habitacion_ciudad_cercana']
            sembrador.direccion_habitacion_punto_referencia = data[
                'direccion_habitacion_punto_referencia']
            sembrador.direccion_habitacion_direccion = data['direccion_habitacion_direccion']

            sembrador.save()
            return redirect('app:dashboard')

        except Tecnico.DoesNotExist:
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Completar Perfil del Sembrador'
        context['url'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


# USUARIOS TECNICOS

class Dashboard(LoginRequiredMixin, TemplateView):
    template_name = 'tecnico/Profiles.html'

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Perfil del Tecnico'
        context['title_body'] = 'Perfil'
        context['user_is_tecnico'] = self.request.user.groups.filter(
            name='Tecnicos').exists()
        context['user_is_sembrador'] = self.request.user.groups.filter(
            name='Sembradores').exists()
        return context


class ListarTecnicosView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Tecnico
    # Ajusta la plantilla según tu estructura
    template_name = 'tecnico/Tecnicos_lista.html'

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
                data = []
                position = 1
                for tecnico in Tecnico.objects.all():
                    item = tecnico.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    # Método para obtener los datos del contexto (puede variar según tu lógica)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Usuarios Tecnicos'
        context['url'] = 'Tecnicos'
        context['title_body'] = 'Listado de Usuarios Tecnicos'
        context['date_now'] = datetime.now()
        context['create_url'] = reverse_lazy('user:Tecnico_crear')
        context['list_url'] = reverse_lazy('user:Tecnico_Listar')

        return context


class CrearTecnicoView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Tecnico
    form_class = TecnicoCreationForm
    template_name = 'form.html'
    success_url = reverse_lazy('user:User_lista')

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            print(action)
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
        context['title'] = 'Formularion del Tecnico'
        context['url'] = 'Formulario Tecnico'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context

    def form_valid(self, form):
        # Guarda el formulario y crea un usuario
        response = super().form_valid(form)

        # Autentica al nuevo usuario
        username = form.cleaned_data['username']
        # asegúrate de tener los campos correctos
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)

        if user is not None:
            login(self.request, user)

        return response


class TecnicoProfileView(UpdateView):
    model = Tecnico
    form_class = TecnicoProfileForm  # Asegúrate de especificar el formulario correcto
    template_name = 'form.html'
    success_url = reverse_lazy('app:dashboard')

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = request.POST
        # deber acomodar este response data siempore esta retornando "succes true"
        response_data = {'success': True}
        try:
            tecnico = Tecnico.objects.get(pk=request.user.id)
            tecnico.cedula = data['cedula']
            tecnico.estado = data['estado']
            tecnico.first_name = data['first_name']
            tecnico.last_name = data['last_name']
            tecnico.oficina = data['oficina']
            tecnico.profesion = data['profesion']
            tecnico.telefono = data['telefono']
            tecnico.logue_complete = True
            tecnico.save()
            return JsonResponse(response_data)

        except Tecnico.DoesNotExist:
            return JsonResponse(response_data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Completar Perfil del Tecnico'
        context['url'] = 'Perfil'
        context['list_url'] = self.success_url
        context['action'] = 'edit'

        user_tecnico = get_user_tecnico(self.request.user)
        context['mostrar_sidebar'] = user_tecnico.logue_complete

        return context
