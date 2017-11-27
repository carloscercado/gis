from django.contrib.gis.db import models
from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos.collections import MultiPolygon
from rest_framework.exceptions import ValidationError

class Manager(models.Manager):

    def get_queryset(self):
        resultado = super(Manager, self).get_queryset().all()
        for i in resultado:
            dato_geografico = i.geom
            if isinstance(dato_geografico, Point):
                return resultado, Atributos.PUNTO
            elif isinstance(dato_geografico, MultiPolygon):
                return resultado, Atributos.POLIGONO_MULTIPLE

class Capas(models.Model):
    nombre = models.CharField(max_length=30)

class Atributos(models.Model):
    PUNTO = 'PUNTO'
    POLIGONO = 'POLIGONO'
    POLIGONO_MULTIPLE = 'POLIGONO_MULTIPLE'
    LINEA = 'LINEA'
    TEXTO = 'TEXTO'
    ENTERO = 'ENTERO'
    FLOTANTE = 'FLOTANTE'

    TIPO_CHOICES = (
        (PUNTO, PUNTO),
        (POLIGONO, POLIGONO),
        (LINEA, LINEA),
        (TEXTO, TEXTO),
        (ENTERO, ENTERO),
        (FLOTANTE, FLOTANTE),
        (POLIGONO_MULTIPLE, POLIGONO_MULTIPLE)
    )

    capa = models.ForeignKey(Capas, on_delete=models.CASCADE,
                             related_name='atributos')
    nombre = models.CharField(max_length=30)
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    descripcion = models.CharField(max_length=80)

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
            elif attr.tipo == Atributos.PUNTO:
                attr.tipo = models.PointField()
            elif attr.tipo == Atributos.POLIGONO_MULTIPLE:
                attr.tipo = models.MultiPolygonField()

            campo = {
                attr.nombre: attr.tipo,
                "datos": Manager()
            }
            campos.update(campo)
        return campos
    except Exception as e:
        print(e)
        error = {
            "capa": "no existe"
        }
        raise ValidationError(error)
