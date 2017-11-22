from rest_framework import serializers
from .models import Estado
class EstadoSerializador(serializers.ModelSerializer):

    class Meta:
        model = Estado
        fields = ("__all__")