from traceback import print_tb
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import  login_required
from rest_framework.authtoken.models import Token
import re
# Create your views here.



 

#@login_required(login_url='docentes:login')
def index(request):
    return render(request,'docentes/index.html',{})

@login_required(login_url='docentes:login')
def crearPlaneacion(request):
    return render(request,'docentes/crear_planeacion.html',{})

@login_required(login_url='docentes:login')
def favoritos(request):
    return render(request,'docentes/favoritos.html',{})

@login_required(login_url='docentes:login')
def misPlaneaciones(request):
    return render(request,'docentes/tus_planeaciones.html',{})

@login_required(login_url='docentes:login')
def perfil(request):
    return render(request,'docentes/perfil_usuario.html',{})

@login_required(login_url='docentes:login')
def actualizarPassword(request):
    if request.method == 'POST':
        user=User.objects.get(id=request.user.id)
        print(len(request.POST['password']))
        print(request.POST['password2'])
        if request.POST['password'] == request.POST['password2'] and request.POST['password']!='' and request.POST['password2']!='':
            user.set_password(request.POST['password'])
            user.save()
            logout(request)
            return redirect('docentes:login')
        elif request.POST['password']!=request.POST['password2'] or request.POST['password2']!=request.POST['password']:
            return render(request,'docentes/actualizacion_password.html',{'password_distintos':'Contrasena no valida'})
   
        elif request.POST['password']=='' and request.POST['password2']=='' or request.POST['password']=='' or request.POST['password2']=='':
            return render(request,'docentes/actualizacion_password.html',{'password_vacio':'Contrasena no valida'})
    
    return render(request,'docentes/actualizacion_password.html',{})
    
@login_required(login_url='docentes:login')  
def actualizarUsuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        user = User.objects.get(id=request.user.id)
        allUser=User.objects.all()
        for user_ahutenticate in allUser:
            if user_ahutenticate.username==request.POST['name']:
                return render(request,'docentes/actualizacion_informacion.html',{'noUser':'Usuario ya existente'})
        if email=='' and name!='':
            user.username=name
            user.save()
            return render(request,'docentes/index.html',{})
        elif email!='' and name=='':
            user.email=email
            user.save()
            return render(request,'docentes/index.html',{})
        elif  email=='' and name=='':
            return render(request,'docentes/actualizacion_informacion.html',{'noAcualizado':'No se actualiza ningun dato'})
        if len(name)!=0 and len(email)!=0:
            user.username = name
            user.email = email
            user.save()
            return redirect('docentes:index')
    return render(request,'docentes/actualizacion_informacion.html',{'mensajeError' : 'Rellene los campos para hacer el cambio'})
    
#para logiar al usuario
def login_user(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('docentes:index')
        return render(request,'docentes/login.html',{})
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None: # si si se valido el usuario entonces creamos la sesion
            login(request,user)
            token = Token.objects.get_or_create(user=user)#buscamos o creamos el token del usuario
            #regresamos el token del usuario
            return render(request,'docentes/index.html',{'token':'token '+str(token[0])})
        else:# si los datos del usuario no concuerdan mandamos un error
            return render(request,'docentes/login.html',{'datos_invalidos':'Tu usuario o contaseña son invalidos'})

#para cerrar sesion
@login_required(login_url='docentes:login')  
def cerrar_sesion(request):
    u = User.objects.get(id=request.user.id)
    token = Token.objects.get(user=u.id)#buscamos o creamos el token del usuario
    token.delete()#borramos el token de sesion
    logout(request)
    return redirect('docentes:login')

#para registrar un usuario nuevo
def es_correo_valido(correo):
    expresion_regular = r"(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"
    return re.match(expresion_regular, correo) is not None

def registrar_usuario(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('docentes:index')
        return render(request,'docentes/registro_usuario.html',{})     
    elif request.method == 'POST':
        allUser=User.objects.all()
        for user_ahutenticate in allUser:
            if user_ahutenticate.username==request.POST['username']:
                return render(request,'docentes/registro_usuario.html',{'noUser':'Usuario ya existente'})

        if es_correo_valido(request.POST['email'])==False:
            return render(request,'docentes/registro_usuario.html',{'email_no_valido':'email no valida'} )

        if request.POST['password'] == request.POST['password2'] or request.POST['password2']==request.POST['password']:
            user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'],email=request.POST['email'])

                
        elif request.POST['password'] != request.POST['password2'] or request.POST['password2']!=request.POST['password']:
            return render(request,'docentes/registro_usuario.html',{'password_no_valido':'Contraseña no valida'})
       
        return redirect('docentes:login')
