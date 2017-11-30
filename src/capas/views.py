from rest_framework import viewsets
from .models import Capas, crear_modelo, Atributos
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .serializers import CapaSerializador, PuntoSerializador, CapaListSerializador,\
                         PoligonoSerializador, LineaSerializador
from django.contrib.gis.db.models.functions import Centroid, AsGeoJSON



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

        import pdb
        #pdb.set_trace()

        queryset = modelo.objects.all()


        from django.core.serializers import serialize


        data = serialize('geojson', queryset,
                         geometry_field='geom')
        import json
        data = json.loads(data)
        return Response(data, content_type="application/json")


