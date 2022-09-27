from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers
from docentes.models import Actividad, Comentario, Favorito, Planeacion,Customer, Rating

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username']

class PlaneacionSerializers(serializers.ModelSerializer):
    id_usuario = UserSerializer()
    class Meta:
        model = Planeacion
        fields = '__all__'
        depth = 1



    

class ActividadSerielizers(serializers.ModelSerializer):
    class Meta:
        model=Actividad
        fields='__all__'

class FavoritoSerielizers(serializers.ModelSerializer):
    class Meta:
        model=Favorito
        fields='__all__'

class RatingSerielizers(serializers.ModelSerializer):
    class Meta:
        model =Rating
        fields = '__all__'

class ComentarioSerielizers(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = '__all__'