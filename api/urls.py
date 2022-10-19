#urls de la aplicacion de docentes

from django.urls import path
from api import views as v
from docentes import views



#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'
urlpatterns = [



    path('planeaciones',v.Planeacion_APIView.as_view(),name='planeaciones'),
    path('planeaciones/<str:pk>',v.Planeacion_APIView.as_view(),name='planeaciones'),
    path('clonarPlaneacion',v.PlaneacionClonarView.as_view(),name='clonarPlaneacion'),

    path('buscarPlaneacion',v.Planeacion_APIViewFree.as_view(),name='buscarPlaneacion'),
    path('buscarPlaneacion/<str:titulo>',v.Planeacion_APIViewFree.as_view(),name='buscarPlaneacion'),

    path('favoritos',v.Favorito_APIView.as_view(),name='favoritos'),#para los favoritos
    path('favoritos/<str:pk>',v.Favorito_APIView.as_view(),name='favoritos'),#para los favoritos

    path('actividades',v.Actividad_APIView.as_view(),name='actividades'),#para los favoritos
    path('actividades/<str:pk>',v.Actividad_APIView.as_view(),name='actividades'),#para los favoritos
    path('actividadesFree',v.Actividad_APIView.as_view(),name='actividadesFree'),#para los favoritos sin logearse
    path('actividadesFree/<str:pk>',v.Actividad_APIView.as_view(),name='actividadesFree'),#para los favoritos sin logearse


]