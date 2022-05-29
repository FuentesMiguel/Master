from django.db import models

from datetime import datetime
# Create your models here.

class Municipio(models.Model):
    nombre = models.CharField(max_length=25, verbose_name='Municipios', unique=True)

    class Meta:
        verbose_name = "Municipio"
        verbose_name_plural = "Municipios"

    def __str__(self):
        return str(self.id)

class Parroquia(models.Model):
    id_municipio =models.ForeignKey(Municipio, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=25, verbose_name='Parroquias', unique=True)

    class Meta:
        verbose_name = "Parroquia"
        verbose_name_plural = "Parroquias"

    def __str__(self):
        return str(self.id)
    
class Comuna(models.Model):
    id_parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=25, verbose_name='Comunas', unique=True)

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"

    def __str__(self):
        return str(self.id)
    

class Solicitante(models.Model):
    """
    Description: Model Solicitantes
    """
    fecha_registro = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    estatus = models.BooleanField(default=False)
    cedula = models.CharField(max_length=25, unique=True, verbose_name='Cedula')
    nombre = models.CharField(max_length=25, verbose_name='Nombres')
    apellido = models.CharField(max_length=25, verbose_name='Apellido')
    telefono = models.CharField(max_length=30, verbose_name='Telefono')
    correo_electronico = models.EmailField()
    direccion = models.TextField()
    municipio = models.ForeignKey(Municipio, on_delete=models.CASCADE)
    parroquia = models.ForeignKey(Parroquia, on_delete=models.CASCADE)
    comuna = models.ForeignKey(Comuna, on_delete=models.CASCADE)



    def __str__(self):
        return str(self.id)


    class Meta:
        verbose_name = 'Solicitante'
        verbose_name_plural = 'Solicitantes'
        db_table='Solicitantes'
        ordering = ['-id']