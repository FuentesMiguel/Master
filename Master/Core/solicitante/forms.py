from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import*

class SolicitanteForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('fecha_registro', css_class='form-group col-md-4'),
				Column('estatus', css_class='form-group col-md-4'),
				Column('cedula', css_class='form-group col-md-4'),
				css_class='form-row'
				),
			Row(
				Column('nombre', css_class='form-group col-md-4 mb-0'),
				Column('apellido', css_class='form-group col-md-4 mb-0'),
				Column('telefono', css_class='form-group col-md-4 mb-0'),
				css_class='form-row'
				),
			Row(
				Column('correo_electronico', css_class='form-group col-md-6 mb-0'),
				Column('direccion', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
				),
			Row(
				Column('municipio', css_class='form-group col-lg-4 mb-0'),
				Column('parroquia', css_class='form-group col-lg-4 mb-0'),
				Column('comuna', css_class='form-group col-lg-4 mb-0'),
				css_class='form-row'
				),
			)

	class Meta:
		model = Solicitante
		fields = '__all__'
		widgets = {
	        'fecha_registro':forms.DateInput(format='%d/%m/%Y', attrs = {'class':'form-control','placeholder':'Fecha de Ingreso'}),
	        'estatus':forms.CheckboxInput(attrs = {'class': 'form-control','placeholder':'Estatus del Solicitante'}),
	        'cedula':forms.TextInput(attrs = {'class': 'form-control','placeholder':'Introduce tus numero de Cedula'}),
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Nombres'}),
	        'apellido':forms.TextInput(attrs = {'class': 'form-control','placeholder':'Introduce tus Apellidos'}),
	        'telefono':forms.TextInput(attrs = {'class': 'form-control','placeholder':'Telefono fijo o de Casa'}),
	        'correo_electronico':forms.EmailInput(attrs = {'class': 'form-control','placeholder':'Introduce correo electronico'}),
            'direccion':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce una brever direccion de tu Domicilio'}),
            'municipio':forms.Select(attrs={'class':'form-control'}),
            'parroquia':forms.Select(attrs={'class':'form-control'}),
            'comuna':forms.Select(attrs={'class':'form-control'})
        }

	def save(self):
		data = {}
		form = super()
		try:
			if form.is_valid():
				form.save()
			else:
				data['error'] = form.errors
		except Exception as e:
			data['error'] = str(e)
		return data

