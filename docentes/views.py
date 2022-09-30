from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import  login_required
# Create your views here.



 

@login_required(login_url='docentes:login')
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
        password1=request.POST['password1']
        password2=request.POST['password2']
        user=User.objects.get(id=request.user.id)
        print(user.password)
        if password1 == password2:
            user.set_password(password1)
            user.save()
            logout(request)
            return redirect('docentes:login')
        elif password1!=password2 or password2!=password1:
            return render(request,'docentes/actualizacion_password.html',{'mensajeError':'Una de las contrasenas no es valida'})
        
           

    return render(request,'docentes/actualizacion_password.html',{})
    
@login_required(login_url='docentes:login')  
def actualizarUsuario(request):
    if request.method == 'POST':
        email = request.POST['email']
        name = request.POST['name']
        user = User.objects.get(id=request.user.id)

        if len(name)!=0 and len(email)!=0:
            user.username = name
            user.email = email
            user.save()
            return render(request,'docentes/index.html',{})

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
            return redirect('docentes:index')
        else:# si los datos del usuario no concuerdan mandamos un error
            return render(request,'docentes/login.html',{'mensajeError':'Tu usuario o contaseña son invalidos'})

#para cerrar sesion
def cerrar_sesion(request):
    logout(request)
    return redirect('docentes:login')

#para registrar un usuario nuevo
def registrar_usuario(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('docentes:index')
        return render(request,'docentes/registro_usuario.html',{})
    elif request.method == 'POST':
        if request.POST['password'] == request.POST['password2']:
            user = User.objects.create_user(username=request.POST['username'],password=request.POST['password'])
        return redirect('docentes:login')
