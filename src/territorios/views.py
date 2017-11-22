from rest_framework import viewsets
from .models import Estado
from .serializadores import EstadoSerializador

class EstadoRecurso(viewsets.ModelViewSet):
    queryset = Estado.objects.all()
    serializer_class = EstadoSerializador
