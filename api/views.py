from curses.ascii import NUL
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

#para obtener las planeaciones de un usuario
class PlaneacionListViewUser(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Planeacion.objects.all()
        serializer = PlaneacionSearchListSerializers(post, many=True)

    def get(self, request):# para las planeaciones de un usuario
        post = Planeacion.objects.all().filter(id_usuario=request.user.id).order_by('fecha_de_inicio')#ordenamos por la fecha de inicio
        serializer = PlaneacionSearchListSerializers(post, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = PlaneacionSearchListSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#para obtener las planeaciones buscadas por titulo
class Planeacion_APIView(APIView):
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
    
    '''def post(self, request, format=None):#para agregar planeaciones ---------------------------------------------------POST
        serializer = PlaneacionPostInicial(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)'''



#para las Planeaciones
class Planeacion_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Planeacion.objects.get(pk=pk)
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PlaneacionSerializers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PlaneacionSerializers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#para actualizar la Planeacion------------------------------------------------ Actualizar la planeacion
class PlaneacionUpdateView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            list = str(id).split(',')
            return Planeacion.objects.get(pk=int(list[0]))
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        list = str(id).split(',')
        post = self.get_object(int(list[0]))
        if post.id_usuario.id == request.user.id:
            post.tema=list[1]
            post.grado = list[2]
            post.fecha_de_inicio = list[3]
            post.fecha_de_finalizacion = list[4]
            if list[5] == 'true':
                post.anonima = True
            else:
                post.anonima = False
            post.observaciones = list[6]
            if list[7] == 'true':
                post.finalizada = True
            else:
                post.finalizada = False
            post.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

#---------------------------------------------------------------------------- Para borrar una planeacion
class PlaneacionDeleteView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            return Planeacion.objects.get(pk=id)
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        post = self.get_object(id)
        print('----------------------------- Borrando')
        if post.id_usuario.id == request.user.id:
            post.delete()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


#----------------------------------------------------------------------------- Para agregar una planeacion
#para guardar las actividades
class PlaneacionAddView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            list = str(id).split(',')
            return Planeacion.objects.get(pk=int(list[0]))#verificamos que la planeacion exista
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        list = str(id).split(',')#lista con los elementos
        u = User.objects.get(id=request.user.id)
        plan = Planeacion()
        plan.id_usuario = u
        plan.titulo = list[0]
        plan.tema = list[1]
        plan.grado = list[2]
        plan.fecha_de_inicio = list[3]
        plan.fecha_de_finalizacion = list[4]
        if list[5] == 'true':
            plan.anonima = True
        else:
            plan.anonima = False
        plan.save()
        lista = Planeacion.objects.all().filter(id=plan.id)
        serializer = PlaneacionFullSerializer(lista, many=True) 
        return Response(serializer.data)


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

#para obtener la lista de actividades de una planeacion---------------------------------------------------------------------------------
class ActividadListView(APIView):
    def get(self, request,id):
        post = Actividad.objects.all().filter(id_planeacion=id).order_by('fecha_de_inicio')#ordenamos por fecha de inicio
        serializer = ActividadSerielizers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ActividadSerielizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, id, format=None):
        print('borrando ---------------------------------------------')
        post = self.get_object(id)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#para las Actividades
class Actividad_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Actividad.objects.get(pk=pk)
        except Actividad.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ActividadSerielizers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = ActividadSerielizers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#para borrar las actividades
class ActividadDeleteView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            return Actividad.objects.get(pk=id)
        except Actividad.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        post = self.get_object(id)
        print('----------------------------- Borrando')
        if post.id_planeacion.id_usuario.id == request.user.id:
            post.delete()
            print('')
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)


#para actualizar las actividades
class ActividadUpdateView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            list = str(id).split(',')
            return Actividad.objects.get(pk=int(list[0]))
        except Actividad.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        list = str(id).split(',')
        post = self.get_object(int(list[0]))
        if post.id_planeacion.id_usuario.id == request.user.id:
            post.fecha_de_inicio=list[1]
            post.titulo = list[2]
            post.descripcion = list[3]
            if list[4] == 'true':
                post.finalizada = True
            else:
                post.finalizada = False
            post.save()
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

#para guardar las actividades
class ActividadAddView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    def get_object(self, id):
        try:
            list = str(id).split(',')
            return Planeacion.objects.get(pk=int(list[0]))#verificamos que la planeacion exista
        except Planeacion.DoesNotExist:
            raise Http404
    def get(self, request, id, format=None):
        list = str(id).split(',')#lista con los datos pasados por el path
        post = self.get_object(int(list[0]))
        if post.id_usuario.id == request.user.id: #revisamos que la planeacion aya sido echa por ese usuario    
            act = Actividad()
            act.id_planeacion = post
            act.fecha_de_inicio=list[1]
            act.titulo = list[2]
            act.descripcion = list[3]
            act.save()
            p = Actividad.objects.all().filter(id=act.id)# mandamos la lista con elementos en este caso solo es 1
            serializer = ActividadSerializer(p, many=True) 
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)

#para obtener la lista de planeaciones favoritas de cada usuario---------------------------------------------
class FavoritoListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None, *args, **kwargs):
        post = Favorito.objects.all()
        serializer = FavoritoListSerielizers(post, many=True)
    def get(self,request):
        #print('hola:',request.user)
        post =  Favorito.objects.select_related('id_planeacion').all().filter(id_usuario=request.user.id)
        serializer = FavoritoListSerielizers(post, many=True)
        return Response(serializer.data)


class FavoritoInserView(APIView):
    def get(self, request,id_plan):
        try:
            
            fav = Favorito.objects.get(id_planeacion=id_plan,id_usuario=request.user.id)
            print(fav)
            
        except ObjectDoesNotExist:
            print('insertando')
            fav = Favorito(id_planeacion=id_plan,id_usuario=request.user.id)
            
            return Response(status= status.HTTP_200_OK)
        return Response(status= status.HTTP_200_OK)
        
        
#para los favoritos--------------------------------------------------------------------------------------
class Favorito_APIView(APIView):
    permission_clases = [permissions.IsAuthenticated]
    #nota se esta pasando por parametro el id de la planeacion
    def get_object(self, pk):
        try:
            return Favorito.objects.get(id_planeacion=pk)
        except Favorito.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = FavoritoSerializerAdd(post)  
        return Response(serializer.data)

    def post(self, request, format=None):# aqui vamos a agregar un elemento a favoritos
        serializer = FavoritoSerializerAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class Favorito_APIView_Detail(APIView):
    def get_object(self, pk):
        try:
            return Favorito.objects.get(id_planeacion=pk)
        except Favorito.DoesNotExist:
            raise Http404
    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = FavoritoSerielizers(post)  
        return Response(serializer.data)
    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = FavoritoSerielizers(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
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