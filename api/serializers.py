from dataclasses import fields
from pyexpat import model
from rest_framework import serializers
from docentes.models import Actividad, Planeacion,Customer

class CustomerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class PlaneacionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Planeacion
        fields = '__all__'

    

class ActividadSerielizers(serializers.ModelSerializer):
    class Meta:
        model=Actividad
        fields='__all__'