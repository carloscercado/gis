from django.db import connection
from .models import Capas
from rest_framework.exceptions import ValidationError
import json

class CapaImporter():

    def __init__(self, capa, nombre):
        self.cursor = connection.cursor()
        self.nombre = nombre.replace('.', '_')
        self.capa = capa

    def get_geometria(self, obj):
        """
        Obtener el tipo de dato geometrico
        """
        return obj.geometry.type

    def validar_capa(self):
        """
        Validar que toda la capa tiene un solo dato geometrico y
        que no exista otro en base de datos
        """
        tipo = self.capa[0].geometry.type
        for item in self.capa:
            if item.geometry.type != tipo:
                raise ValidationError("la capa tiene multiples tipos de geometria")
            tipo = item.geometry.type
        if Capas.objects.filter(nombre=self.nombre.lower()).count() > 0:
            raise ValidationError({"mensaje": "ya existe la capa registrada"})

    def add(self, obj):
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
        insert = "INSERT INTO capas_"+self.nombre+"("+keys+") VALUES ("+valores+" ST_SetSRID(ST_GeomFromGeoJSON(%s), 4326));"
        self.cursor.execute(insert, (data,) )

    def importar_tabla(self):
        """
        crea la tabla con su estructura en la base de datos
        """
        self.validar_capa()
        attrs = self.capa.common_attributes

        table_query = "CREATE TABLE if not exists capas_"+self.nombre+"  (\
                     id SERIAL,\
                     PRIMARY KEY (id),\
                     geom GEOMETRY("+self.get_geometria(self.capa[0])+", 4326)\
                     "
        for i in attrs:
            if i.lower() == "id":
                continue
            table_query += ", "+i+" varchar(255)"
        table_query += ");"
        self.cursor.execute(table_query)
        for obj in self.capa:
            self.add(obj)
        self.registrar_estructura(attrs)
        connection.commit()

    def registrar_estructura(self, attrs):
        """
        registrar la estructura de la capa a nivel de datos
        """
        self.cursor.execute("INSERT INTO capas_capas (nombre) values(%s) RETURNING id;", (self.nombre,))
        _id = self.cursor.fetchone()[0]
        self.cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, 'geom', %s);", (_id, self.get_geometria(self.capa[0]),))
        for i in attrs:
            if i.lower() == "id":
                continue
            self.cursor.execute("INSERT INTO capas_atributos (capa_id, nombre, tipo) values(%s, %s, 'Text');", (_id, i.lower(),))

    def desde_tabla(self, instancia):
        geom = instancia.atributos.filter(nombre="geom").first()
        if geom is None:
            raise ValidationError({"capa": "falta atributo geom"})

        table_query = "CREATE TABLE if not exists capas_"+self.nombre+"  (\
                        id SERIAL,\
                        PRIMARY KEY (id),\
                        geom GEOMETRY("+geom.tipo+", 4326)\
                        "
        for i in instancia.atributos.all():
            if i.nombre.lower() in ["id", "geom"]:
                continue
            table_query += ", "+i.nombre+" "+i.tipo.lower()
        table_query += ");"
        self.cursor.execute(table_query)