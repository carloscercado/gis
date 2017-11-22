from django.db import models


class Estado(models.Model):
    nombre = models.CharField(max_length=20)

class Municipio(models.Model):
    estado = models.ForeignKey(Estado, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=20)
