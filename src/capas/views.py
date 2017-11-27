from rest_framework import viewsets
from .models import Capas, crear_modelo, Atributos
from rest_framework.decorators import list_route
from rest_framework.response import Response
from .serializers import CapaSerializador, PuntoSerializador, CapaListSerializador, PoligonoSerializador



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

        queryset, tipo = modelo.datos.get_queryset()

        for i in queryset:
            i.tipo = tipo

        if tipo == Atributos.PUNTO:
            serializer_class = PuntoSerializador
            serializer_class.Meta.model = modelo
            serializer = PuntoSerializador(queryset, many=True,
                                              context={'request': request})
        elif tipo == Atributos.POLIGONO_MULTIPLE:
            serializer_class = PoligonoSerializador
            serializer_class.Meta.model = modelo
            serializer = PoligonoSerializador(queryset, many=True,
                                              context={'request': request})


        return Response(serializer.data)


