from django.views import View
from django.http import HttpResponse
from django.template import loader
from Core.solicitud.models import Inspeccion, VocacionTierra, Material_vivienda
from Core.User.models import Sembradores, Tecnico
from django.shortcuts import render
from Core.solicitud.CrearPdf import crear_pdf


def generar_pdf(request, id
                ):
    ruta_template = '/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/hola.html'
    inspeccion_actual = Inspeccion.objects.get(id=id)
# sold/generar_pdf/1/
    sembrador_id = inspeccion_actual.Sembrador_user.id
    sembrador = Sembradores.objects.get(id=sembrador_id)

    tecnico_id = inspeccion_actual.tecnico.id
    tecnico = Tecnico.objects.get(id=tecnico_id)

    vocacion_tierra = inspeccion_actual.vocacion_tierra.all()

    material_vivienda = inspeccion_actual.material_vivienda.all()

    electricidad = inspeccion_actual.electricidad.all()

    # me los trae mira la consola
    # ya vi
    # Crea un diccionario con los datos recuperados
# vocacion tierra trae multiples valores cabe recalcar!!!!!!!!!!
    info = {
        'sembrador': sembrador,
        'tecnico': tecnico,
        'inspeccion_actual': inspeccion_actual,
        'vocacion_tierra': vocacion_tierra,
        'material_vivienda': material_vivienda,
        'electricidad': electricidad

    }

    # Llama a la función para generar el PDF
    crear_pdf(ruta_template, info)

    # Devuelve una respuesta HTTP apropiada (puede ser un redireccionamiento o un mensaje de éxito)
    with open('/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/hola.pdf', 'rb') as pdf_file:
        response = HttpResponse(
            pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=reporte.pdf'
        return response


def vista_previa_pdf(request):
    pdf_url = '/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/hola.pdf'
    # /home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/
    return render(request, 'hola.html', {'pdf_url': pdf_url})
