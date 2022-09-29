#urls de la aplicacion de docentes

from django.urls import path
from api import views as v
from docentes import views



#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'
urlpatterns = [

    path('obtenerPlaneacion/<str:titulo>',v.Planeacion_APIView.as_view(),name='obtenerPlaneacion'), #para obtener las planeaciones por un titulo dado por el usuario

     path('obtenerPlaneacionUsuario',v.PlaneacionListViewUser.as_view(),name='obtenerPlaneacionUsuario'), #para obtener las planeaciones de un usuario 


    path('obtenerFavorito',v.FavoritoListView.as_view(),name='obtenerFavoritos'),# para obtener la lista de planeaciones favoritas

    path('obtenerActividades/<str:id>',v.ActividadListView.as_view(),name='obtenerActividades'),# para obtener la lista de actividades de una planeacion
    path('borrarActividad/<str:id>',v.ActividadDeleteView.as_view(),name='borrarActividad'),# para borrar la actividad dada por id
    path('actualizarActividad/<str:id>',v.ActividadUpdateView.as_view(),name='actualizarActividad'),# para borrar la actividad dada por id
    path('agregarActividad/<str:id>',v.ActividadAddView.as_view(),name='agregarActividad'),# para borrar la actividad dada por id

    path('insertarFavorito',v.FavoritoInserView.as_view(),name='insertarFavorito'),

]