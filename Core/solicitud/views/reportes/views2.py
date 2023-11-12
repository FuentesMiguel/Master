from django.views import View
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
from Core.solicitud.Crearpdf2 import crear_pdf2


def generarpdf(request
               ):
    ruta_template = '/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/seguimiento.html'

    # me los trae mira la consola
    # ya vi
    # Crea un diccionario con los datos recuperados
# vocacion tierra trae multiples valores cabe recalcar!!!!!!!!!!
    info = {


    }

    # Llama a la función para generar el PDF
    crear_pdf2(ruta_template, info)

    # Devuelve una respuesta HTTP apropiada (puede ser un redireccionamiento o un mensaje de éxito)
    with open('/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/seguimiento.pdf', 'rb') as pdf_file:
        response = HttpResponse(
            pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename=reporte.pdf'
        return response


def vista_previa_pdf(request):
    pdf_url = '/home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/seguimiento.pdf'
    # /home/miguel/Escritorio/Master/Core/solicitud/templates/reportes/
    return render(request, 'seguimiento.html', {'pdf_url': pdf_url})
