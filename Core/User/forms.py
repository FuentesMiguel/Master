from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML, Div
from django.contrib.auth.models import Group

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .models import *
from Core.User.choice import *


class GroupForm(forms.Form):
    name = forms.CharField(label='Nombre del Grupo', max_length=100)
    # Agrega más campos según tus necesidades


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('username', css_class='form-group col-md-4'),
                Column('email', css_class='form-group col-md-8'),
                css_class='form-row'
            ),
            Row(
                Column('password', css_class='form-group col-md-8'),
                Column('user_permissions', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('groups', css_class='form-group col-md-4'),
                Column('last_login', css_class='form-group col-md-4'),
                Column('date_joined', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('is_superuser', css_class='form-group col-md-4'),
                Column('is_staff', css_class='form-group col-md-4'),
                Column('is_active', css_class='form-group col-md-4'),
                Column('imagen', css_class='form-group col-md-12'),
                css_class='form-row'
            ),


        )

    class Meta:
        model = User
        fields = 'password', 'last_login', 'is_superuser', 'groups', 'user_permissions', 'username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'date_joined', 'imagen'
        widgets = {
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Password'}),
            'last_login': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_superuser': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-control', 'style': 'font-size: 9px'}),
            'groups': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'user_permissions': forms.SelectMultiple(attrs={'class': 'form-control select2'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Apellidos'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electronico'}),
            'is_staff': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-control'}),
            'is_active': forms.CheckboxInput(attrs={'type': 'checkbox', 'class': 'form-control'}),
            'date_joined': forms.DateTimeInput(attrs={'type': 'date', 'class': 'form-control'}),
            'imagen': forms.FileInput(attrs={'placeholder': 'Seleccione Imagen ...', }),
        }

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                for g in self.cleaned_data['groups']:
                    u.groups.add(g)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class UserProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                Column('username', css_class='form-group col-md-12'),
                Column('email', css_class='form-group col-md-12'),
                Column('password', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = User
        fields = 'first_name', 'last_name', 'username', 'email', 'password', 'imagen'
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Apellidos'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electronico'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Password'}),
        }
        exclude = ['is_superuser', 'is_staff', 'is_active',
                   'user_permissions', 'last_login', 'date_joined', 'groups']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = User.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class RegistroForm(UserCreationForm):

    class Meta:
        model = Sembradores
        fields = (
            'username',
            'email',
            'codigo_asonaproyuca',
            'password1',
            'password2',
        )
        widgets = {
            'username': forms.TextInput(attrs={'id': 'id_username'}),
            'email': forms.EmailInput(attrs={'id': 'id_email'}),
            'codigo_asonaproyuca': forms.TextInput(attrs={'id': 'id_codigo_asonaproyuca'}),
            'password1': forms.PasswordInput(render_value=True, attrs={'id': 'id_password1'}),
            'password2': forms.PasswordInput(render_value=True, attrs={'id': 'id_password2'}),
        }


# FORMULARIO DE SEMBRADORES

"""class DatosConyugeForm(forms.ModelForm):
    class Meta:
        model = DatosConyuge
        fields = '__all__'


class DireccionHabitacionForm(forms.ModelForm):
    class Meta:
        model = DireccionHabitacion
        fields = '__all__'
"""


class SembradorCreationForm(forms.ModelForm):

    password_confirmation = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirma tu Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4'),
                Column('password', css_class='form-group col-md-4'),
                Column('password_confirmation',
                       css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-12'),

                css_class='form-row'
            ),

        )

    class Meta:
        model = Sembradores
        fields = 'username', 'email', 'password', 'password_confirmation'

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electronico'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Password'}),
            'logue_complete': forms.HiddenInput(),

        }

        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'first_name', 'last_name',
                   'date_joined', 'is_staff', 'is_active', 'imagen', 'cedula', 'estado', 'oficina', 'profesion', 'telefono', 'conyuge', 'direccion_habitacion']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = Sembradores.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                group_name = 'Sembradores'
                group, created = Group.objects.get_or_create(name=group_name)
                u.groups.add(group)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class SembradorProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4'),
                Column('password', css_class='form-group col-md-4'),
                Column('email', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-4'),
                Column('last_name', css_class='form-group col-md-4'),
                Column('cedula', css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('codigo_asonaproyuca', css_class='form-group col-md-6'),
                Column('cedula_agraria', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('telefono_personal', css_class='form-group col-md-3'),
                Column('telefono_casa', css_class='form-group col-md-3'),
                Column('direccion', css_class='form-group col-md-6'),
                css_class='form-row'
            ),
            Row(
                Column('fecha_nacimiento', css_class='form-group col-md-4'),
                Column('edad', css_class='form-group col-md-2'),
                Column('estado_civil', css_class='form-group col-md-2'),
                Column('profesion_ocupacion', css_class='form-group col-md-2'),
                Column('sexo', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            # Row(
            #    Column('estado', css_class='form-group col-md-4'),
            #    Column('municipio', css_class='form-group col-md-4'),
            #    Column('parroquia', css_class='form-group col-md-4'),
            #   Column('nombre_unidad', css_class='form-group col-md-12'),
            #    css_class='form-row'
            # ),
            HTML(
                '<h1 class="text-center mb-4 mt-4" style="color: green;"> DATOS DEL CÓNYUGE</h1>'),
            Row(
                Column('conyuge_cedula', css_class='form-group col-md-4'),
                Column('conyuge_nombre', css_class='form-group col-md-4'),
                Column('conyuge_apellido', css_class='form-group col-md-4'),
            ),
            Row(
                Column('conyuge_telefono_fijo',
                       css_class='form-group col-md-4'),
                Column('conyuge_telefono_celular',
                       css_class='form-group col-md-4'),
                Column('conyuge_edad', css_class='form-group col-md-2'),
                Column('conyuge_sexo', css_class='form-group col-md-2'),
                css_class='form-row'
            ),
            HTML(
                '<h1 class="text-center mb-4 mt-4" style="color: green;">Dirección de Habitación del (Solicitante o Persona Jurídica)</h1>'),
            Row(
                Column('direccion_habitacion_estado',
                       css_class='form-group col-md-3'),
                Column('direccion_habitacion_municipio',
                       css_class='form-group col-md-3'),
                Column('direccion_habitacion_parroquia',
                       css_class='form-group col-md-3'),
                Column('direccion_habitacion_caserio',
                       css_class='form-group col-md-3'),
                Column('direccion_habitacion_sector',
                       css_class='form-group col-md-6'),
                Column('direccion_habitacion_ciudad_cercana',
                       css_class='form-group col-md-6'),
                Column('direccion_habitacion_punto_referencia',
                       css_class='form-group col-md-12'),
                Column('direccion_habitacion_direccion',
                       css_class='form-group col-md-12'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Sembradores
        fields = '__all__'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Nombre de Usuario'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Contraseña'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electrónico'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Número de Cédula'}),
            'codigo_asonaproyuca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Número de Código de Asonaproyuca'}),
            'cedula_agraria': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Número de Cédula Agraria'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Apellidos'}),
            'telefono_personal': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Número de Teléfono Personal'}),
            'telefono_casa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Número de Teléfono (Casa)'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Dirección a Detalle'}),
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control', 'placeholder': 'Selecciona tu Fecha de Nacimiento'}),
            'edad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Edad'}),
            'estado_civil': forms.Select(attrs={'class': 'form-control select2', 'placeholder': 'Selecciona tu Estado Civil'}),
            'profesion_ocupacion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Profesión u Ocupación'}),
            'sexo': forms.Select(attrs={'class': 'form-control select2', 'placeholder': 'Selecciona tu Sexo'}),

            # 'estado': forms.Select(attrs={'id': 'estado', 'class': 'form-control, select2', 'placeholder': 'Selecciona el estado'}),
            # 'municipio': forms.Select(attrs={'id': 'municipio', 'class': 'form-control, select2', 'placeholder': 'Selecciona el municipio'}),
            # 'parroquia':  forms.Select(attrs={'id': 'parroquia', 'class': 'form-control, select2', 'placeholder': 'Selecciona la parroquia'}),

            # 'nombre_unidad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre de la Unidad de Produccion'}),



            'conyuge_nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el nombre del cónyuge'}),
            'conyuge_apellido':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el apellido del cónyuge'}),
            'conyuge_cedula':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce la cédula del cónyuge'}),
            'conyuge_edad': forms.NumberInput(attrs={'class': 'form-control select2', 'placeholder': 'Introduce la edad del cónyuge'}),
            'conyuge_sexo': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Introduce el sexo del cónyuge'}),
            'conyuge_telefono_fijo':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el teléfono fijo del cónyuge'}),
            'conyuge_telefono_celular':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el teléfono celular del cónyuge'}),

            'direccion_habitacion_estado': forms.Select(attrs={'id': 'estado', 'class': 'form-control, select2', 'placeholder': 'Selecciona el estado'}),
            'direccion_habitacion_municipio': forms.Select(attrs={'id': 'municipio', 'class': 'form-control, select2', 'placeholder': 'Selecciona el municipio'}),
            'direccion_habitacion_parroquia':  forms.Select(attrs={'id': 'parroquia', 'class': 'form-control, select2', 'placeholder': 'Selecciona la parroquia'}),
            'direccion_habitacion_caserio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el caserío de la dirección de habitación'}),
            'direccion_habitacion_sector':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el sector de la dirección de habitación'}),
            'direccion_habitacion_ciudad_cercana': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce la ciudad cercana de la dirección de habitación'}),
            'direccion_habitacion_punto_referencia':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce el punto de referencia de la dirección de habitación'}),

            'direccion_habitacion_direccion':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce la dirección detallada de habitación'}),
        }
        exclude = ['is_superuser', 'is_staff', 'is_active', 'google_maps_url',
                   'groups', 'user_permissions', 'last_login', 'date_joined', 'groups', 'fecha_registro', 'fecha_actualizacion']


# FORMULARIO DE TECNICO


class TecnicoCreationForm(forms.ModelForm):
    password_confirmation = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Confirma tu Password'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-md-4'),
                Column('password', css_class='form-group col-md-4'),
                Column('password_confirmation',
                       css_class='form-group col-md-4'),
                css_class='form-row'
            ),
            Row(
                Column('email', css_class='form-group col-md-12'),

                css_class='form-row'
            ),

        )

    class Meta:
        model = Tecnico
        fields = 'username', 'email', 'password', 'password_confirmation', 'logue_complete'
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electronico'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Password'}),
            'logue_complete': forms.HiddenInput(),

        }

        exclude = ['last_login', 'is_superuser', 'groups', 'user_permissions', 'first_name', 'last_name',
                   'date_joined', 'is_staff', 'is_active', 'imagen', 'cedula', 'estado', 'oficina', 'profesion', 'telefono']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirmation = cleaned_data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise forms.ValidationError("Las contraseñas no coinciden.")

        return cleaned_data

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                pwd = self.cleaned_data['password']
                u = form.save(commit=False)
                if u.pk is None:
                    u.set_password(pwd)
                else:
                    user = Tecnico.objects.get(pk=u.pk)
                    if user.password != pwd:
                        u.set_password(pwd)
                u.save()
                u.groups.clear()
                group_name = 'Tecnicos'
                group, created = Group.objects.get_or_create(name=group_name)
                u.groups.add(group)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


class TecnicoProfileForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column('cedula', css_class='form-group col-md-6'),
                Column('estado', css_class='form-group col-md-6'),
                Column('oficina', css_class='form-group col-md-12'),
                Column('profesion', css_class='form-group col-md-12'),
                Column('telefono', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
            Row(
                Column('first_name', css_class='form-group col-md-6'),
                Column('last_name', css_class='form-group col-md-6'),
                Column('username', css_class='form-group col-md-12'),
                Column('email', css_class='form-group col-md-12'),
                Column('password', css_class='form-group col-md-12'),
                Column('imagen', css_class='form-group col-md-12'),
                css_class='form-row'
            ),
        )

    class Meta:
        model = Tecnico
        fields = '__all__'
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Nro de Cédula'}),
            'estado': forms.Select(choices=ESTADOS_VENEZUELA_CHOICES, attrs={'class': 'form-control', 'id': 'estado'}),
            'oficina': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce Ofina a la que pertenece'}),
            'profesion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce Profesion'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Nro de Telefono'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Nombres'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tus Apellidos'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Introduce tu Correo Electronico'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class': 'form-control', 'placeholder': 'Introduce tu Password'}),
            'logue_complete': forms.HiddenInput(),
            'imagen': forms.FileInput(),
        }
        exclude = ['is_superuser', 'is_staff', 'is_active',
                   'groups', 'user_permissions', 'last_login', 'date_joined', 'groups']

    def save(self):
        data = {}
        form = super()
        try:
            if form.is_valid():
                print(data)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data
