from rest_framework import viewsets
from .models import Capas, crear_modelo, Atributos
from rest_framework.decorators import list_route
from rest_framework.response import Response
from django.contrib.gis.db import models
from .serializers import CapaSerializador, PuntoSerializador, CapaListSerializador,\
                         PoligonoSerializador, LineaSerializador
import pygeoj
from rest_framework.exceptions import ValidationError
from django.db import connection
import json
from django.core.serializers import serialize
from rest_framework.parsers import FormParser, MultiPartParser


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

        def get_geometria(obj):
            """
            Obtener el tipo de dato geometrico
            """
            return obj.geometry.type

        def validar_capa(capa, nombre):
            """
            Validar que toda la capa tiene un solo dato geometrico y
            que no exista otro en base de datos
            """
            tipo = capa[0].geometry.type
            for item in capa:
                if item.geometry.type != tipo:
                    raise ValidationError("la capa tiene multiples tipos de geometria")
                tipo = item.geometry.type
            if Capas.objects.filter(nombre=nombre.lower()).count() > 0:
                raise ValidationError({"mensaje": "ya existe la capa registrada"})


        def registrar_estructura(cursor, capa, nombre):
            """
            registrar la estructura de la capa a nivel de datos
            """
            attrs = capa.common_attributes
            cursor.execute("INSERT INTO capas_capas (nombre) values(%s) RETURNING id;", (nombre,))
            _id = cursor.fetchone()[0]
            cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, 'geom', %s);", (_id, get_geometria(capa[0]),))
            for i in attrs:
                if i.lower() == "id":
                    continue
                cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, %s, 'Text');", (_id, i.lower(),))

        def add(cursor, nombre, obj):
            """
            crea los registro de la capa
            """
            keys = []
            valores = ""
            for i in obj.properties.items():
                if i[0].lower() == "id":
                    continue
                keys.append(i[0].lower())
                valores += "'"+str(i[1])+"',"
            keys.append("geom")

            keys = keys = ','.join(map(str, keys))
            geom = {
                "type": obj.geometry.type,
                "coordinates": obj.geometry.coordinates
            }
            data = (json.dumps(geom))
            insert = "INSERT INTO capas_"+nombre+"("+keys+") VALUES ("+valores+" ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326));"
            cursor.execute(insert, (data,) )

        def importar_tabla(cursor, capa, nombre):
            """
            crea la tabla con su estructura en la base de datos
            """
            attrs = geo.common_attributes

            table_query = "CREATE TABLE if not exists capas_"+nombre+"  (\
                         id SERIAL,\
                         PRIMARY KEY (id),\
                         geom GEOMETRY("+get_geometria(capa[0])+", 4326)\
                         "
            for i in attrs:
                if i.lower() == "id":
                    continue
                table_query += ", "+i+" varchar(255)"
            table_query += ");"
            cursor.execute(table_query)
            for obj in capa:
                add(cursor, nombre, obj)
            registrar_estructura(cursor, capa, nombre)

        try:
            _file = self.request.data.get('file')
            geo = pygeoj.load(_file.fileno())
            nombre = _file.name.replace('.geojson', '')
            validar_capa(geo, nombre)
            cursor = connection.cursor()
            importar_tabla(cursor, geo, nombre)
            connection.commit()
            return Response()
        except Exception as e:
            connection.rollback()
            print(e)
            raise ValidationError(str(e))
