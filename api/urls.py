#urls de la aplicacion de docentes

from django.urls import path
from docentes import views

#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'

urlpatterns = [
    path('',views.index,name='index'),
]
