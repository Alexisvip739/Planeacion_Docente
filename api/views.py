from nis import cat
from urllib import request
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework.response import Response
from .serializers import ActividadSerielizers, ComentarioSerielizers, CustomerSerializers, FavoritoSerielizers, PlaneacionSerializers, RatingSerielizers
from docentes.models import Actividad, Comentario, Favorito, Planeacion,Customer, Rating
from rest_framework import status
from django.contrib.auth.models import User
from django.http import Http404


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from django.core.exceptions import ObjectDoesNotExist
    

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




#para obtener las planeaciones
class Planeacion_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Planeacion.objects.all()
        serializer = PlaneacionSerializers(post, many=True)

    def get(self, request, titulo):# para obtener las planeaciones por su titulo
        post = Planeacion.objects.prefetch_related('favorito_set').all()
        #.filter(titulo__contains=titulo).
        print('lista----------')
        print(post)#imprimimos la lista
        for a in post:
            print(a.favorito_set)
        

        serializer = PlaneacionSerializers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = PlaneacionSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Favorito_APIView_Detail2(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Favorito.objects.all()
        serializer = FavoritoSerielizers(post, many=True)
    def get(self,request,id):
        post = Favorito.objects.filter(id_planeacion=id).filter(id_usuario=request.user.id)
        serializer = FavoritoSerielizers(post, many=True)
        return Response(serializer.data)




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


#para las actividades
class Actividad_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Actividad.objects.all()
        serializer = ActividadSerielizers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):
        serializer = ActividadSerielizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        
        
#para los favoritos
class Favorito_APIView(APIView):
    def get(self, request, format=None, *args, **kwargs):
        post = Favorito.objects.all()
        serializer = FavoritoSerielizers(post, many=True)
        
        return Response(serializer.data)
    def post(self, request, format=None):# aqui recibiremos los like
        print('holaaaaaaa--------------')
        serializer = FavoritoSerielizers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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