#urls de la aplicacion de docentes

from django.urls import path
from api import views as v
from docentes import views



#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'
urlpatterns = [

    path('obtenerPlaneacion/<str:titulo>/',v.Planeacion_APIView.as_view(),name='obtenerPlaneacion'), 

    path('obtenerFavoritos1/<str:pk>',v.Favorito_APIView_Detail.as_view(),name='obtenerFavorito1'),

    path('obtenerFavorito/<str:id>',v.Favorito_APIView_Detail2.as_view(),name='obtenerFavorito'),

    path('insertarFavorito',v.FavoritoInserView.as_view(),name='insertarFavorito'),

]