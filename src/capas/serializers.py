from rest_framework import serializers
from .models import Capas, Atributos, Categoria


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

    def create(self, datos):
        attr = datos.pop("atributos")
        obj =  Capas.objects.create(**datos)
        self.registrar_atributos(obj, attr)
        return obj

    def registrar_atributos(self, obj, attr):
        for i in attr:
            i.update({"capa": obj})
            Atributos.objects.create(**i)

    def update(self, instance, datos):
        attr = datos.pop("atributos")
        instance.atributos.all().delete()
        for key, value in datos.items():
            setattr(instance, key, value)
        self.registrar_atributos(instance, attr)
        instance.save()
        return instance
        


class CategoriasListSerializador(serializers.ModelSerializer):
    detalle = serializers.HyperlinkedIdentityField(view_name='categoria-detail', format='html')
    capas = CapaListSerializador(many=True)
    class Meta:
          model = Categoria
          fields = ("id","nombre","detalle", "descripcion", "eliminable", "capas")  

class CategoriasSerializador(serializers.ModelSerializer):  
    class Meta: 
        model = Categoria
        fields = ("id","nombre","descripcion","eliminable")


    def  create(self, datos):
        categoria = Categoria.objects.create(**datos)
        return categoria
            

    def update(self, instance, datos):
        instance.nombre = datos.get('nombre') 
        instance.descripcion = datos.get('descripcion') 
        instance.save()                
        return instance


