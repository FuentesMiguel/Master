from django.db import models
from datetime import datetime

from django.forms import model_to_dict

from Core.solicitante.models import Solicitante

# Create your models here.

class Categorias(models.Model):
	nombre = models.CharField(max_length=25, verbose_name='Nombre', unique=True)
	descipcion = models.CharField(max_length=250, null=False, blank=False, verbose_name='Descripcion')

	class Meta:
		verbose_name = "Categorias"
		verbose_name_plural = "Categorias"
		db_table = 'Categoria_Solicitud'
	
	def toJSON(self):
		item = model_to_dict(self)
		return item

	def __str__(self):
		return str(self.id)


class Solicitudes(models.Model):
	fecha_registro = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
	categoria = models.ForeignKey(Categorias, on_delete=models.CASCADE, verbose_name='id Categoria')
	id_solicitante = models.ForeignKey(Solicitante, on_delete=models.CASCADE, verbose_name= 'id Solicitante')

	EN = 'ENTREGADA'
	ES = 'ESPERA'
	RE = 'RECHAZADA'

	OPTIONS_ON_AN_APPLICATION = [
        (EN, 'Entregada'),
        (ES, 'Espera'),
        (RE, 'Rechazada'),]
	estatus = models.CharField(max_length=9, choices=OPTIONS_ON_AN_APPLICATION, default=ES)

	def toJSON(self):
		item = model_to_dict(self)
		return item

	def __str__(self):
		return '{} {} {}'.format(self.id, self.id_solicitante, self.estatus)