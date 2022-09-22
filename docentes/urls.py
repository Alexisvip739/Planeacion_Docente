


#urls de la aplicacion de docentes

from django.contrib import admin
from django.urls import path
from docentes import views

#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'docentes'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index',views.index,name='index'),
]
