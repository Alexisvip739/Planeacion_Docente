from dataclasses import fields
from pyexpat import model
from django.contrib.auth.models import User
from rest_framework import serializers
from docentes.models import Actividad, Comentario, Favorito, Planeacion,Customer, Rating
from docentes.models import Favorito

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username']
class FavoritoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorito
        fields ='__all__'

class PlaneacionFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planeacion
        fields ='__all__'

#para cuando se agrega una planeacion
class PlaneacionPostInicial(serializers.ModelSerializer):
    class Meta:
        model = Planeacion
        exclude = ('finalizada','observaciones', )

        
class ActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actividad
        fields ='__all__'


class PlaneacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planeacion
        fields ='__all__'

# para mostrar todas las planeaciones buscadas por titulo -------------------------------------------------
class PlaneacionSearchListSerializers(serializers.ModelSerializer):
    id_usuario = UserSerializer()
    class Meta:
        model = Planeacion
        fields = '__all__'
        depth = 1
        




class PlaneacionFavoritoSerializers(serializers.ModelSerializer):
    id_usuario = UserSerializer()
    id_planeacion = PlaneacionSerializer()
    class Meta:
        model = Favorito
        fields = '__all__'
        depth = 1
    

class ActividadSerielizers(serializers.ModelSerializer):
    class Meta:
        model=Actividad
        fields='__all__'


#lista de planeacionnes favoritas de un usuario
class FavoritoListSerielizers(serializers.ModelSerializer):
    id_planeacion = PlaneacionFullSerializer()
    id_usuario = UserSerializer()
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