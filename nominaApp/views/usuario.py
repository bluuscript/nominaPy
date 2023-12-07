from django.shortcuts import render, redirect
from nominaApp.model.usuario import Usuario
from nominaApp.model.correo import Correo
from uuid import uuid4

# Página punto de entrada de la plataforma como Inicio de Sesión
def index(request):
    return render(request, "login.html")

# Interfaces del Usuario
def login(request):
    if request.method == "POST":
        # Recuperar correo y contraseña ingresada del formulario
        user_email = request.POST["email"]
        user_password = request.POST["password"]
        # Nuevo Usuario de la clase Usuario
        user = Usuario(email=user_email, password=user_password)
        # user login managment
        if user.exist() == True:
            if user.check_password():
                # Obtener registro Usuario
                user_db = user.get()
                rut_usuario, username, tipo_personal  = user_db["rut"], user_db["username"], user_db["tipo_personal"]
                # Set session data from user data base 
                request.session["user_uuid"] = str(uuid4())
                request.session["rut_usuario"] = rut_usuario
                request.session["username"] = username
                request.session["tipo_personal"] = tipo_personal

                if tipo_personal == "RRHH":
                    return redirect(f"/rrhh/inicio/?auth=ok&username={username}&tipo_personal={tipo_personal}")
                else:
                    return redirect(f"/personal/inicio/?auth=ok&username={username}&tipo_personal={tipo_personal}")
            else:
                # Contraseña invalida
                return redirect('/?auth=invalid')
        else:
            # Usuario no existe
            return redirect('/?auth=invalid')
    else:
        # En caso de haber solicitudes de tipo GET, devolver a index formulario login
        return redirect("/")

def forgot(request):
    if request.method == "GET":
        return render(request, "forgot.html")
    else:
        # Metodo POST
        # Recuperar correo de usuario que quiere recuperar su cuenta
        correo_usuario = request.POST["usuarioCorreo"]
        user_forgot = Usuario(email=correo_usuario, password=None)
        # Verificar que existencia de registro de Usuario para posterior enviar el correo
        if user_forgot.exist() == True:
            send_email = Correo(usuario_correo=correo_usuario).send()
            if send_email != False:
                return redirect(f"/?correo={correo_usuario}&correo_recuperacion=enviado")
            else:
                return redirect(f"/?correo={correo_usuario}&correo_recuperacion=error")
        else:
            return redirect(f"/forgot/?correo={correo_usuario}%no%registrado")
    
def register(request):
    if request.method == "GET":
        return render(request, "register.html")
    else:
        # Metodo POST
        user_rut = request.POST["rut"]
        user_name = request.POST["username"]
        user_email = request.POST["email"]
        user_tipo_personal = request.POST["tipoPersonal"]
        user_password = request.POST["password"]
        # Iteración de Clase para nuevo Usuario
        user = Usuario(rut=user_rut, username=user_name, email=user_email, tipo_personal=user_tipo_personal, password=user_password)
        # user register managment
        if user.exist() == True:
            return redirect(f"/register/?correo={user_email}&usuario=existe")
        elif user.exist() == False:
            # Ingresar Usuario al no existir registro de  Usuario en la base de datos
            if user.save() == True:
                return redirect(f"/?usuario_correo={user_email}&agregar_usuario=exitoso")
            else:
                return redirect(f"/?usuario_correo={user_email}&agregar_usuario=error")
        
def logout(request):
    try:
        del request.session["user_uuid"]
    except KeyError:
        pass
    return redirect("/")