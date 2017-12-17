from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos.collections import MultiPolygon, MultiLineString
from rest_framework.exceptions import ValidationError

class Categoria(models.Model):
    nombre =  models.CharField(max_length=30, unique=True)
    descripcion =  models.CharField(max_length=80, null=True)

    @property
    def eliminable(self):
        return not self.capas.all().exists()

class Capas(models.Model):
    nombre = models.CharField(max_length=30)
    categoria = models.ForeignKey(Categoria, related_name="capas",
                                  on_delete=models.CASCADE)

class Atributos(models.Model):
    PUNTO = 'Point'
    POLIGONO = 'Polygon'
    POLIGONO_MULTIPLE = 'MultiPolygon'
    PUNTO_MULTIPLE = 'MultiPoint'
    LINEA = 'LineString'
    TEXTO = 'Text'
    ENTERO = 'Int'
    FLOTANTE = 'Float'
    LINEA_MULTIPLE = 'MultiLineString'

    TIPO_CHOICES = (
        (PUNTO, PUNTO),
        (POLIGONO, POLIGONO),
        (LINEA, LINEA),
        (TEXTO, TEXTO),
        (ENTERO, ENTERO),
        (FLOTANTE, FLOTANTE),
        (POLIGONO_MULTIPLE, POLIGONO_MULTIPLE),
        (LINEA_MULTIPLE, LINEA_MULTIPLE)
    )

    capa = models.ForeignKey(Capas, on_delete=models.CASCADE,
                             related_name='atributos')
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=80, null=True)

def crear_modelo(nombre):
    opciones = {
        "__module__": "capas"
    }
    campos = buscar_capa_y_atributos(nombre)
    opciones.update(campos)
    modelo = type(nombre, (models.Model,), opciones)
    return modelo

def buscar_capa_y_atributos(nombre):
    try:
        capa = Capas.objects.filter(nombre=nombre).first()
        campos = {}
        for attr in capa.atributos.all():
            if attr.tipo == Atributos.TEXTO:
                attr.tipo = models.CharField(max_length=255)
            elif attr.tipo == Atributos.ENTERO:
                attr.tipo = models.IntegerField()
            elif attr.tipo == Atributos.FLOTANTE:
                attr.tipo = models.FloatField()
            campo = {
                attr.nombre: attr.tipo,
            }
            campos.update(campo)
        campos.update({"geom": models.GeometryField()})
        return campos
    except Exception as e:
        print(e)
        error = {
            "capa": "no existe"
        }
        raise ValidationError(error)
