from django.conf.urls import url, include
from django.contrib import admin
from rest_framework.documentation import include_docs_urls
from territorios.views import EstadoRecurso
from .enrrutador import RaizRouter

router = RaizRouter(trailing_slash=False)

router.register(r'estados', EstadoRecurso)

urlpatterns = [
    url(r'^', include(router.urls)),
    #url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #url(r'^docs/', include_docs_urls(title='Documentacion'))
]