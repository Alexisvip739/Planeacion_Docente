#urls de la aplicacion de docentes

from django.urls import path
from api import views as v
from docentes import views



#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'
urlpatterns = [

    path('obtenerPlaneacion',v.Planeacion_APIView.as_view(),name='obtenerPlaneacion11'),
    path('obtenerPlaneacion/<str:titulo>',v.Planeacion_APIView.as_view(),name='obtenerPlaneacion'), #para obtener las planeaciones por un titulo dado por el usuario

     path('obtenerPlaneacionUsuario',v.PlaneacionListViewUser.as_view(),name='obtenerPlaneacionUsuario'), #para obtener las planeaciones de un usuario 


    path('planeaciones',v.Planeacion_APIView.as_view(),name='planeaciones'),# para actualizar la planeacion
    path('planeaciones/<str:pk>',v.Planeacion_APIView.as_view(),name='planeaciones'),# para borrar una planeacion 
    path('clonarPlaneacion',v.PlaneacionClonarView.as_view(),name='clonarPlaneacion'),# para borrar una planeacion



    path('favoritos',v.Favorito_APIView.as_view(),name='favoritos'),#para los favoritos
    path('favoritos/<str:pk>',v.Favorito_APIView.as_view(),name='favoritos'),#para los favoritos

    path('actividades',v.Actividad_APIView.as_view(),name='actividades'),#para los favoritos
    path('actividades/<str:pk>',v.Actividad_APIView.as_view(),name='actividades'),#para los favoritos
    path('actividadesFree',v.Actividad_APIView.as_view(),name='actividadesFree'),#para los favoritos sin logearse
    path('actividadesFree/<str:pk>',v.Actividad_APIView.as_view(),name='actividadesFree'),#para los favoritos sin logearse


]