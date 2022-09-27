#urls de la aplicacion de docentes

from django.urls import path
from api.views import Actividad_APIView, Actividad_APIView_Detail, Comentario_APIView, Comentario_APIView_Detail, Customer_APIView, Customer_APIView_Detail, Favorito_APIView, Favorito_APIView_Detail, Planeacion_APIView, Planeacion_APIView_Detail, Rating_APIView, Rating_APIView_Detail
from docentes import views

#ponemos el nombre de la app para cuando mandemos llamar a las url poner docentes.urls
app_name = 'api'
urlpatterns = [
    path('v1/Planeacion', Planeacion_APIView.as_view()), 
    path('v1/Planeacion/<int:pk>/', Planeacion_APIView_Detail.as_view()),

    path('v1/Customer',Customer_APIView.as_view()), 
    path('v1/Customer/<int:pk>/',Customer_APIView_Detail.as_view()), 

    path('obtenerPlaneacion/<str:titulo>/',Planeacion_APIView.as_view(),name='obtenerPlaneacion'), 

]