from django.contrib.gis.geos import Point, MultiPoint, Polygon, MultiPolygon

class Punto(Point):
    def get(value):
        if len(value) != 1:
            raise Exception("Valor invalido para Punto. "+str(value))
        return Point(value)

class MultiPunto(MultiPoint):
    pass

class Linea(MultiPoint):
    pass

class MultiLinea(MultiPoint):
    pass

class Raster(MultiPoint):
    pass

class Poligono(Polygon):
    def get(value):
        return Polygon(value)

class MultiPoligono(Polygon):
    def get(value):
        poligono = Polygon(value[0][0])
        return MultiPolygon(poligono)