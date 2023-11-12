from django.shortcuts import get_object_or_404
from .models import Tecnico, Sembradores


def get_user_tecnico(user):
    # Asumiendo que el usuario puede ser un Tecnico o no
    tecnico = get_object_or_404(Tecnico, user_ptr_id=user.id)
    return tecnico
