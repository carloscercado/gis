from capas.models import Categoria
from rest_framework import serializers

class CategoriaSerializador(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ("id","nombre","descripcion","eliminable")

    def create(self, datos):
        categoria = Categoria.objects.create(**datos)
        return categoria

    def update(self, instance, datos):
        instance.nombre = datos.get('nombre')
        instance.descripcion = datos.get('descripcion')
        instance.save()
        return instance

class CategoriaListSerializador(serializers.ModelSerializer):
    from .capas import CapaListSerializador
    link = serializers.HyperlinkedIdentityField(view_name='categoria-detail', format='html')
    capas = CapaListSerializador(many=True)
    class Meta:
        model = Categoria
        fields = ("id","nombre","link", "descripcion", "eliminable", "capas")

