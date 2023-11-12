# Importaciones
import json
from django.utils.timesince import timesince
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from Core.chats.models import *

# Vista para listar salas
class SalaListView(LoginRequiredMixin, ListView):   
    model = Sala

    # Decorador para deshabilitar CSRF (creo que no lo ajustare)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    # Manejar la solicitud POST
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            # Acción solicitada (en el front-end deberías enviar esta información)
            action = request.POST['action']
            
            # Crear sala privada
            if action == 'create_private_room':
                message_list = []  # Lista para almacenar mensajes
                user = User.objects.values('username', 'id').get(id=request.POST['id'])
                username = user['username']
                name = f'{self.request.user}-{username}'
                usuario_actual = request.user
                
                # Verificar si la sala ya existe
                sala_exist = Sala.objects.filter(usuario_sala__usuario=usuario_actual).filter(usuario_sala__usuario=user['id']).first()
                
                if sala_exist:
                    print('SI EXISTE LA SALA')
                    # Obtener mensajes de la sala existente
                    message = Mensaje.objects.filter(sala_id=sala_exist.id)
                    for m in message[0:15]:
                        item = {
                            'body': m.contenido,
                            'date_joined': timesince(m.fecha),
                            'image': m.usuario.get_image(),
                            'first_user': m.usuario_id,
                            'second_user': usuario_actual.id,
                            'message_id': m.id,
                            'editado': m.editado
                        }
                        message_list.append(item)
                    return JsonResponse({'sala_id': sala_exist.id, 'message_list': message_list}, safe=False)
                else:
                    print('NO EXISTE')
                    # Crear sala y enlazar usuarios
                    sala = Sala.objects.create(
                        nombre=name,
                        tipo_sala='PRIVADA'
                    )
                    users = [{'user': usuario_actual.id}, {'user': user['id']}]
                    for i in users:
                        Usuario_sala.objects.create(
                            usuario_id=int(i['user']),
                            sala_id=int(sala.id)
                        )    
                    return JsonResponse({'sala_id': sala.id}, safe=False)               
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)
