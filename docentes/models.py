from email.policy import default
from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Customer(User):
    class meta:
        proxy=True
    
    
class Planeacion(models.Model):
    grado = models.IntegerField(null=False)
    fecha_de_finalizacion = models.DateField(null=False)
    titulo = models.CharField(max_length=60,null=False)
    tema = models.CharField(max_length=60,null=False)
    fecha_de_inicio=models.DateField(null=False)
    id_usuario = models.ForeignKey(User,on_delete=models.CASCADE,blank=False)
    anonima = models.BooleanField(default=False)
    finalizada = models.BooleanField(default=False)
    observaciones = models.TextField(null=True,blank=True)
    #blank true indica que si se puede dejar vacio
    def __str__(self) -> str:
        return self.titulo
    def nombreUsuario(self):
        return User.objects.get(id=self.id_usuario).username


class Actividad(models.Model):
    titulo=models.CharField(max_length=50,null=False)
    fecha_de_inicio=models.DateField(null=False)
    descripcion=models.TextField(null=True,blank=True)
    id_planeacion=models.ForeignKey(Planeacion,on_delete=models.CASCADE)
    finalizada = models.BooleanField(default=False)
    def __str__(self) -> str:
        return self.titulo

##class Rating(models.Model):


class Comentario(models.Model):
    id_usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    id_planeacion=models.ForeignKey(Planeacion,on_delete=models.CASCADE)
    comentario=models.TextField(null=True,blank=True)
    def __str__(self)->str:
        return self.comentario

   
    


class Favorito(models.Model):
    id_usuario=models.ForeignKey(User,on_delete=models.CASCADE)
    id_planeacion=models.ForeignKey(Planeacion,on_delete=models.CASCADE)
    fecha_agregad=models.DateField(auto_now_add=True)
    def __str__(self) -> str:
        return str(self.pk)+' '+str(self.id_usuario)+' '+str(self.id_planeacion)
