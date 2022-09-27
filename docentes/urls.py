


#urls de la aplicacion de docentes

from django.contrib import admin
from django.urls import path
from docentes import views

#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'docentes'

urlpatterns = [
    path('',views.index,name='index'),
    path('login',views.login_user,name='login'),
    path('registrarse',views.registrar_usuario,name='registrar_usuario'),
    path('cerrarsesion',views.cerrar_sesion,name='cerrar_sesion'),
]
