from rest_framework import viewsets
from .models import Capas, crear_modelo, Categoria
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.contrib.gis.db import models
from .serializadores import CategoriaSerializador, CapaSerializador, \
                            CapaListSerializador, CategoriaListSerializador
import pygeoj
from rest_framework.exceptions import ValidationError
from django.core.serializers import serialize
from rest_framework.parsers import FormParser, MultiPartParser
from .capa import CapaImporter
from django.db import connection
from django.db.backends.base.schema import BaseDatabaseSchemaEditor


class CapasRecursos(viewsets.ModelViewSet):

    queryset = Capas.objects.all()
    serializer_class = CapaSerializador

    def get_serializer_class(self):
        if self.action == 'list':
            return CapaListSerializador
        return CapaSerializador

    @list_route(methods=['get'], url_path=r'tipo=(?P<nombre>[^/]+)')
    def get_capa(self, request, nombre):
        modelo =  None
        try:
            from capas.models import nombre
        except:
            modelo = crear_modelo(nombre)

        queryset = modelo.objects.all()
        data = serialize('geojson', queryset,
                         geometry_field='geom')
        data = json.loads(data)
        return Response(data, content_type="application/json")

class ImportarRecurso(viewsets.ViewSet):
    queryset = Capas.objects.all()
    serializer_class = CapaSerializador
    parser_classes = (MultiPartParser, FormParser,)

    def create(self, request, *args, **kwargs):
        _file = self.request.data.get('file')
        nombre = self.request.data.get("nombre")
        categoria = self.request.data.get("categoria")
        geo = pygeoj.load(_file.fileno())
        importer = CapaImporter(geo, nombre, categoria)
        importer.importar_tabla()
        connection.commit()
        return Response()

class CategoriaRecursos(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializador


    def get_serializer_class(self):
        if self.action in ['list', "retrieve"]:
            return CategoriaListSerializador
        return CategoriaSerializador

    def destroy(self, request, *args, **kwargs):
        objecto = self.get_object()

        if not objecto.eliminable:
            respuesta = {
                "mensaje": "Categoria no se puede eliminar, tiene capas asociadas"
            }
            return Response(respuesta,status=400)
        self.perform_destroy(objecto)
        return Response(status=204)

    def perform_destroy(self, instance):
        instance.delete()

