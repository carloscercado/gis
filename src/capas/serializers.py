from rest_framework import serializers
from .models import Capas, Atributos


class AtributoSerializador(serializers.ModelSerializer):

    class Meta:
        model = Atributos
        fields = ("id", "nombre", "tipo","descripcion", )


class CapaListSerializador(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='capas-detail', format='html')
    class Meta:
        model = Capas
        fields = ("id", "nombre", "detalle")

class CapaSerializador(serializers.ModelSerializer):
    atributos = AtributoSerializador(many=True)
    class Meta:
        model = Capas
        fields = ("id", "nombre", "atributos")

class PuntoSerializador(serializers.ModelSerializer):
    geo = serializers.JSONField(source="geom.json", required=False)
    class Meta:
        model = Capas
        exclude = ("geom",)

class PoligonoSerializador(serializers.ModelSerializer):
    poligono = serializers.CharField(source="geom.json", required=False)
    tipo = serializers.CharField(required=False)
    class Meta:
        model = Capas
        exclude = ("geom",)

class LineaSerializador(serializers.ModelSerializer):
    lineas = serializers.JSONField(required=False)
    tipo = serializers.CharField(required=False)
    class Meta:
        model = Capas
        exclude = ("geom",)


