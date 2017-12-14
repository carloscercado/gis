from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from .enrrutador import RaizRouter
from capas.views import CapasRecursos, ImportarRecurso, CategoriaRecursos

router = RaizRouter(trailing_slash=False)
router.register("capas", CapasRecursos)
router.register("categorias", CategoriaRecursos)
router.register("importar", ImportarRecurso)

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^docs/', include_docs_urls(title='Documentacion'))
]