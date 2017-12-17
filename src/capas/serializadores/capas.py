from capas.models import Capas, Atributos
from rest_framework import serializers
from .categorias import CategoriaSerializador
from capas.capa import CapaImporter


class AtributoSerializador(serializers.ModelSerializer):
    class Meta:
        model = Atributos
        fields = ("id", "nombre", "tipo","descripcion", )

class CapaListSerializador(serializers.ModelSerializer):
    link = serializers.HyperlinkedIdentityField(view_name='capas-detail', format='html')
    categoria = CategoriaSerializador()
    #atributos = AtributoSerializador(many=True)
    class Meta:
        model = Capas
        fields = ("id", "nombre", "categoria", "link")

class CapaSerializador(serializers.ModelSerializer):
    atributos = AtributoSerializador(many=True)
    class Meta:
        model = Capas
        fields = ("id", "nombre","categoria", "atributos")

    def create(self, datos):
        attrs = datos.pop("atributos")
        nombre = datos.pop("nombre").replace('.', '_').replace(" ", "_").lower()
        obj =  Capas.objects.create(**datos, nombre=nombre)
        self.registrar_atributos(obj, attrs)
        importer = CapaImporter(None, obj.nombre, obj.categoria_id, verificar_nombre=False)
        importer.desde_tabla(obj)
        return obj

    def registrar_atributos(self, obj, attrs):
        for i in attrs:
            i.update({"capa": obj})
            Atributos.objects.create(**i)

    def update(self, instance, datos):
        attrs = datos.pop("atributos")
        instance.atributos.all().delete()
        for key, value in datos.items():
            setattr(instance, key, value)
        self.registrar_atributos(instance, attrs)
        instance.nombre.replace('.', '_').replace(" ", "_").lower()
        instance.save()
        return instance

