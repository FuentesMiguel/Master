from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import*

class CategoriasForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('nombre', css_class='form-group col-md-6'),
				Column('descipcion', css_class='form-group col-md-6'),
				css_class='form-row'
				),
			)

	class Meta:
		model = Categorias
		fields = '__all__'
		widgets = {
            'nombre':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Nombres'}),
            'descipcion':forms.TextInput(attrs={'class':'form-control','placeholder':'Introduce tus Nombres'}),
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


class SolicitudesForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('fecha_registro', css_class='form-group col-md-3'),
				Column('categoria', css_class='form-group col-md-3'),
				Column('id_solicitante', css_class='form-group col-md-3'),
				Column('estatus', css_class='form-group col-md-3'),
				css_class='form-row'
				),
			)
	class Meta:
		model = Solicitudes
		fields = '__all__'
		widgets = {
		'fecha_registro':forms.DateInput(attrs={'class':'form-control'}),
		'categoria':forms.Select(attrs={'class':'form-control'}),
		'id_solicitante':forms.Select(attrs={'class':'form-control'}),
		'estatus':forms.Select(attrs={'class':'form-control'}),
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