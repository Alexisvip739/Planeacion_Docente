from curses.ascii import NUL
from itertools import count
from nis import cat
from sys import *
from urllib import request
from xmlrpc.client import Boolean
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import *
#importamos todos los serializadores
from docentes.models import Actividad, Comentario, Favorito, Planeacion,Customer, Rating
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404
from rest_framework import permissions
from datetime import datetime


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.authtoken.models import Token
import copy


# Create your views here.
class Customer_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = User.objects.all()
        serializer = CustomerSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = CustomerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Customer_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = CustomerSerializers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = CustomerSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#para obtener las planeaciones buscadas por titulo sin logearse (y en caso se estar logeado manda la info que no este en favoritos)
class Planeacion_APIViewFree(APIView):
    permission_classes = [permissions.AllowAny]#para que cualquiera pueda encontrar una planeacion sin logearse
    def get(self, request, format=None, *args, **kwargs):
        post = Planeacion.objects.all()
        serializer = PlaneacionSearchListSerializers(post, many=True)

    def get(self, request, titulo):# para obtener las planeaciones por su titulo-------------------------------------------------------------------
        if request.auth is not None:# si el usuario esta autenticado entonces
            token = Token.objects.get(key=request.auth)#obtenemos el objeto token para de ahi obtener el usuario

            listaFavoritos = Favorito.objects.values('id_planeacion').all().filter(id_usuario=token.user.id)#buscamos las planeaciones favoritas del usuario
            #buscamos las planeaciones favoritas del usuario excluyendo las que aya agreado a favoritos
            post = Planeacion.objects.all().filter(titulo__contains=titulo).order_by('fecha_de_inicio').exclude(id__in=listaFavoritos)
            #exluimos las planeaciones que tengamos en favoritos
            if len(post) == 0:
                #mandamos el error 404 ya que no hay planeaciones con ese titulo
                raise Http404
            serializer = PlaneacionSearchListSerializers(post, many=True)
            return Response(serializer.data)
        #si el usuario No esta autenticado entonces devolvemos todas las planeaciones 
        post = Planeacion.objects.all().filter(titulo__contains=titulo).order_by('fecha_de_inicio')#ordenamos por la fecha de inicio
        if len(post) == 0:
            #mandamos el error 404 ya que no hay planeaciones con ese titulo
            raise Http404
        #post = Planeacion.objects.prefetch_related('favorito_set').all()
        #.filter(titulo__contains=titulo).
        serializer = PlaneacionSearchListSerializers(post, many=True)
        
        return Response(serializer.data)



#para las Planeaciones ------------------------------------------------------------ REAL
class Planeacion_APIView(APIView):
    permission_clases = [permissions.IsAuthenticated] 
    def get_object(self, pk):
        try:
            return Planeacion.objects.get(pk=pk)
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, format=None):#obtenemos las planeaciones del usuario
        token = Token.objects.get(key = request.auth)
        post = Planeacion.objects.all().filter(id_usuario=token.user.id).order_by('fecha_de_inicio')#ordenamos por la fecha de inicio
        serializer = PlaneacionSearchListSerializers(post, many=True)
        return Response(serializer.data)
    def post(self, request, format=None):#crear una planeacion
        token = Token.objects.get(key=request.auth)
        if token.user.id == request.data['id_usuario']:
            serializer = PlaneacionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):#actualizar una planeacion
        token = Token.objects.get(key=request.auth)
        if token.user.id == request.data['id_usuario']:
            post = self.get_object(pk)
            serializer = PlaneacionSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):#borrar una planeacion
        token = Token.objects.get(key=request.auth)
        post = self.get_object(pk)
        if post.id_usuario.id ==  token.user.id:#para solo si el usuario es el creador de dicha planeacion se pueda borrar
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)







#Para clonar una planeacion--------------------------------------------------------------------------------------
class PlaneacionClonarView(APIView):
    permission_clases = [permissions.IsAuthenticated]        
    
    def post(self, request, format=None):
        try:
            post = Planeacion.objects.get(id=request.data['id'])
        except Planeacion.DoesNotExist:
            raise Http404
        #obtenemos el token para de ahi obtener el usuario
        token = Token.objects.get(key=request.auth)
        
        #clonamos la planeacion
        plan = Planeacion()
        plan.grado = post.grado
        plan.fecha_de_finalizacion = post.fecha_de_finalizacion
        plan.titulo = 'Copia-'+post.titulo
        plan.tema = post.tema
        plan.fecha_de_inicio = post.fecha_de_inicio
        plan.anonima = post.anonima
        plan.finalizada = post.finalizada
        plan.observaciones = post.observaciones
        plan.id_usuario = token.user
        plan.save()#guardamos la nueva planeacion
        listaActividades = Actividad.objects.all().filter(id_planeacion=post.id)#obtenemos la lista de actividades para luego copiarlas
        for a in listaActividades:
            nuevaActividad = Actividad()
            nuevaActividad.id_planeacion = plan
            nuevaActividad.titulo = a.titulo
            nuevaActividad.fecha_de_inicio = a.fecha_de_inicio
            nuevaActividad.descripcion = a.descripcion
            nuevaActividad.finalizada = a.finalizada
            nuevaActividad.save()#guardamos la actividad
        serializer = FavoritoSerializerAdd(post)  
        return Response(status=status.HTTP_201_CREATED)



#para las Actividades (obtener actividades de un plan) sin logearse
class Actividad_APIViewFree(APIView):
    permission_clases = [permissions.AllowAny]
    def get_object(self, pk):
        try:
            return Actividad.objects.get(pk=pk)
        except Actividad.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):#obtener las actividades de una planeacion
        post = Actividad.objects.all().filter(id_planeacion=pk).order_by('fecha_de_inicio')#ordenamos por fecha de inicio
        serializer = ActividadSerielizers(post, many=True)  
        return Response(serializer.data)

#para las Actividades
class Actividad_APIView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, pk):
        try:
            return Actividad.objects.get(pk=pk)
        except Actividad.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):#obtener las actividades de una planeacion
        post = Actividad.objects.all().filter(id_planeacion=pk).order_by('fecha_de_inicio')#ordenamos por fecha de inicio
        serializer = ActividadSerielizers(post, many=True)  
        return Response(serializer.data)

    def post(self, request, format=None):
        token = Token.objects.get(key=request.auth)
        try:#validamos que la planeacion exista
            plan = Planeacion.objects.get(id=request.data['id_planeacion'])
            if plan.id_usuario.id == token.user.id:#si el usuario creo la planeacion entonces ponemos agregar una actividad
                serializer = ActividadSerielizers(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                raise Http404
        except Planeacion.DoesNotExist:
            raise Http404
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put(self, request, pk, format=None):
        token = Token.objects.get(key=request.auth)
        try:#validamos que la planeacion exista
            plan = Planeacion.objects.get(id=request.data['id_planeacion'])
            if plan.id_usuario.id == token.user.id:#si el usuario creo la planeacion entonces ponemos modificar una actividad
                post = self.get_object(pk)
                serializer = ActividadSerielizers(post, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
            else:
                raise Http404
        except Planeacion.DoesNotExist:
            raise Http404
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


        
        
#para los favoritos (insertar y borrar) --------------------------------------------------------------------------------------
class Favorito_APIView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    #nota se esta pasando por parametro el id de la planeacion
    def get_object(self, pk):
        try:
            return Favorito.objects.get(id_planeacion=pk,id_usuario=token.user)
        except Favorito.DoesNotExist:
            raise Http404
    def get(self, request, format=None):
        token = Token.objects.get(key=request.auth)
        post =  Favorito.objects.all().filter(id_usuario=token.user.id)
        #print(Favorito.objects.annotate(suma = sum('id_usuario')).query )
        serializer = FavoritoListSerielizers(post, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):# aqui vamos a agregar un elemento a favoritos
        serializer = FavoritoSerializerAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        token = Token.objects.get(key=request.auth)
        try:
            post = Favorito.objects.get(id_planeacion=pk,id_usuario=token.user)
        except Favorito.DoesNotExist:
            raise Http404
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class Rating_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Rating.objects.all()
        serializer = RatingSerielizers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = RatingSerielizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Rating_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Rating.objects.get(pk=pk)
        except Rating.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = RatingSerielizers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = RatingSerielizers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Comentario_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Comentario.objects.all()
        serializer = ComentarioSerielizers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ComentarioSerielizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Comentario_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Comentario.objects.get(pk=pk)
        except Comentario.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ComentarioSerielizers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ComentarioSerielizers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)