#urls de la aplicacion de docentes

from django.urls import path
from api.views import Customer_APIView, Customer_APIView_Detail, Planeacion_APIView, Planeacion_APIView_Detail
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