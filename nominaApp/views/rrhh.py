from django.shortcuts import render, redirect
from datetime import datetime
import math
# Clases de models para iterar y asi crear objetos y poder manipularlos con sus respectivos metodos
from nominaApp.model.rrhh import RRHH
from nominaApp.model.personal import Personal
from nominaApp.model.solicitud import Solicitud

# Interfaces del Personal de RRHH
def inicio(request): 
    # Solicitud del tipo GET
    if "user_uuid" in request.session:
        # Recuperar datos de la sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        context = {
            "rut_usuario": rut_usuario,
            "username": username,
            "tipo_personal": tipo_personal
        }
        return render(request, "rrhh/index.html", context)
    else:
        # Usuario no esta autenticado devovler a index login page
        return redirect("/")

def nomina_personal(request):
     # Verificar que usuario este autentificado para peticion de de nomina | Metodo POST y el GET 
    if "user_uuid" in request.session:        
        # Recuperar datos de la sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        # Mostrar Nomina en caso de peticion  de tipo GET
        if request.method == "GET":
            # Recuperar numero de la pagina 
            num_pagina_actual = int(request.GET["page"])  if "page" in request.GET else 1
            registros_por_pagina = 10
            num_registros_pagina = (num_pagina_actual - 1) * registros_por_pagina
            # Obtener los registros del personal 
            registros_nomina = Personal().get_all(
                                    rut_usuario_rrhh = rut_usuario,
                                    numero_pagina = num_pagina_actual - 1,
                                    registros_por_pagina = registros_por_pagina
                                )
            cantidad_registros = Personal().count(rut_usuario_rrhh = rut_usuario)
            # Data para Paginación de Solicitudes del Personal
            cantidad_paginas = math.ceil( cantidad_registros / registros_por_pagina )
            lista_num_paginas = []
            for num in range(0, cantidad_paginas, 1):
                lista_num_paginas.append(num + 1)
            context = {
                "rut_usuario": rut_usuario,
                "username": username,
                "tipo_personal": tipo_personal,
                # Validar que existan registro del personal
                "registros_nomina": registros_nomina if registros_nomina is not None else None,
                "cantidad_registros": cantidad_registros,
                # Enviar Datos para Paginacion
                "cantidad_paginas": cantidad_paginas,
                "lista_num_paginas": lista_num_paginas,
                "num_pagina_actual": num_pagina_actual,
                "num_registros_pagina": num_registros_pagina,
            }
            return render(request, "rrhh/nomina-personal.html", context)
        else:
            # Metodo POST => Redireccionar a nomina TODO: ACEPTAR POST DE MODIFICAR REGISTRO
            return redirect("/rrhh/nomina/")
    else:
        # Usuario no esta autenticado devovler a index login page
        return redirect("/")

def eliminar_registro_personal(request):
    # Verificar que usuario este autentificado para peticion de Eliminar | Metodo POST y GET es redirect
    if "user_uuid" in request.session:
        if request.method == "POST":
            # id_registro = request.POST["idRegistro"]
            rut_personal = request.POST["rutPersonal"]
            registro_exist = Personal().get_one(personal_rut=str(rut_personal))
            if registro_exist is not None:
                eliminar_registro = Personal().delete(personal_rut=str(rut_personal))
                # Se valida eliminar_registro para revisar si se elimino registro o no
                if eliminar_registro.acknowledged == True:
                    return redirect(f"/rrhh/nomina/?registro_rut={rut_personal}&eliminar_registro=ok")
                else:
                    return redirect(f"/rrhh/nomina/?registro_rut={rut_personal}&eliminar_registro=falló")
            else:
                return redirect(f"/rrhh/nomina/?registro_rut={rut_personal}&eliminar_registro=no%encontrado")
    else:
        # Usuario no esta autenticado devovler a index login page
        return redirect("/")
        
def nuevo_registro_personal(request):
    # Solicitudes del tipo GET y POST
    if "user_uuid" in request.session:
        # Recuperar datos de la sesion Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        if request.method == "GET":
            context = {
                "rut_usuario": rut_usuario,
                "username": username,
                "tipo_personal": tipo_personal
            }
            return render(request, "rrhh/nuevo-registro-personal.html", context)
        # Metodo POST | Logica para insertar el registro en la base de datos
        else:
            # Verificar que Usuario de RRHH no Ingrese su propio Registro
            rut_personal = request.POST["rutPersonal"]
            if rut_usuario == rut_personal:
                return redirect(f"/rrhh/nuevo-registro/?nuevo_registro=no%puedes%ingresar%tu%propio%registro")
            # Verificar que el reistro no exista e insertarlo si no existe
            if Personal(personalRut=rut_personal).exist() == True:
                return redirect(f"/rrhh/nuevo-registro/?nuevo_registro=existe&rut_personal={rut_personal}")
            else:
                # Datos Personal
                nombre_personal = request.POST["nombrePersonal"]
                genero_personal = request.POST["generoPersonal"]
                direccion_personal = request.POST["direccionPersonal"]
                # Agregar posibilidad de más telefonos 
                telefonos_personal = []
                telefono_personal = request.POST["telefonoPersonal"]
                telefonos_personal.append(int(telefono_personal)) if telefono_personal else None
                # Datos Cargo
                cargo_personal = request.POST["cargoPersonal"]
                cargo_sueldo = request.POST["cargoSueldo"]
                
                fecha_ingreso = request.POST["fechaIngresoPersonal"]
                año, mes, dia = map(int, fecha_ingreso.split("-"))
                
                area_personal = request.POST["areaPersonal"]
                departamento_personal = request.POST["departamentoPersonal"] 
                # Datos Contactos de Emergencia ( SOLO 1 DE MOMENTO)
                rut_contacto = request.POST["rutContacto"]
                nombre_contacto = request.POST["nombreContacto"]
                relacion_contacto_personal = request.POST["relacionContactoPersonal"]
                # Agregar posibilidad de más telefonos de Contacto
                telefonos_contacto = []
                telefono_contacto = request.POST["telefonoContacto"]
                telefonos_contacto.append(int(telefono_contacto)) if telefono_contacto else None
                # Datos Cargas Familiares ( SOLO 1 DE MOMENTO )
                rut_carga = request.POST["rutCarga"]
                nombre_carga = request.POST["nombreCarga"]
                parentesco_carga =  request.POST["parentescoCarga"]
                genero_carga = request.POST["generoCarga"]
                # Iterar un nuevo objeto Personal para insertar registro en la base de datos
                registro_personal = Personal(
                    # Datos Personales
                    personalRut=str(rut_personal), personalNombre=str(nombre_personal), personalGenero=str(genero_personal), personalDireccion=str(direccion_personal), telefonosPersonal=list(telefonos_personal),
                    # Datos Laborales
                    cargoNombre=str(cargo_personal), cargoSueldo = float(cargo_sueldo), cargoFechaIngreso=datetime(year=año, month=mes, day=dia), departamentoNombre=str(departamento_personal), areaNombre=str(area_personal),
                    # Datos Contactos de Emergencia
                    contactoRut=str(rut_contacto), contactoNombre=str(nombre_contacto), contactoRelacionPersonal=str(relacion_contacto_personal), telefonosContacto=list(telefonos_contacto),
                    # Datos Cargas Familiares 
                    cargaRut=str(rut_carga), cargaNombre=str(nombre_carga), cargaGenero=str(genero_carga), cargaParentesco=str(parentesco_carga)
                )
                # Insertar registro personal en la base de datos
                nuevo_registro = registro_personal.save()
                if  nuevo_registro.acknowledged == True:
                    return redirect(f"/rrhh/nomina/?nuevo_registro=ok&nombre_personal={nombre_personal}")
                else:
                    return redirect(f"/rrhh/nomina/?nuevo_registro=falló&nombre_personal={nombre_personal}")
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")

def solicitudes_personal(request):
        # Solicitudes del tipo GET y POST
    if "user_uuid" in request.session:
        # Recuperar datos de la sesion Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        # Mostrar las Solicitudes del personal en solocitud de tipo GET
        if request.method == "GET":
            # Recuperar numero de la pagina 
            num_pagina_actual = int(request.GET["page"])  if "page" in request.GET else 1
            solicitudes_por_pagina = 9
            num_solicitudes_pagina = (num_pagina_actual - 1) * solicitudes_por_pagina
            # Recuperar todas las solicitudes del personal
            solicitudes_personal = Solicitud().get_all(
                                                    rut_usuario_rrhh=rut_usuario, 
                                                    numero_pagina=num_pagina_actual - 1, 
                                                    solicitudes_por_pagina=solicitudes_por_pagina
                                                )
            cantidad_solicitudes = Solicitud().count(rut_usuario_rrhh=rut_usuario)
            # Data para Paginación de Solicitudes del Personal
            cantidad_paginas = math.ceil( cantidad_solicitudes / solicitudes_por_pagina )
            lista_num_paginas = []
            for num in range(0, cantidad_paginas, 1):
                lista_num_paginas.append(num + 1)
            context = {
                # Enviar datos de la sesion del Usuario
                "rut_usuario": rut_usuario,
                "username": username,
                "tipo_personal": tipo_personal,
                # Validar que existan solicitudes de personal 
                "solicitudes_personal": solicitudes_personal if cantidad_solicitudes > 0 else None,
                "cantidad_solicitudes": cantidad_solicitudes,
                # Enviar Datos para Paginacion
                "cantidad_paginas": cantidad_paginas,
                "lista_num_paginas": lista_num_paginas,
                "num_pagina_actual": num_pagina_actual,
                "num_solicitudes_pagina": num_solicitudes_pagina,
            }
            return render(request, "rrhh/solicitudes-personal.html", context)
        else:
            # Metodo POST
            # Logica para actualizar estado de solictud de False a True en la base de datos (update)
            uuid_solicitud = request.POST["idSolicitud"]
            nuevo_estado = request.POST["estadoSolicitud"]
            solicitud = Solicitud().get_one(solicitud_uuid=uuid_solicitud)
            if solicitud is not None:
                actualizar_estado = Solicitud().update(solicitud_uuid=uuid_solicitud, estado_solicitud=nuevo_estado)
                if actualizar_estado is not None:
                    return redirect(f"/rrhh/solicitudes/?solicitud={uuid_solicitud}&actualizar=success&nuevoEstado={nuevo_estado}")
                else:
                    return redirect(f"/rrhh/solicitudes/?solicitud={uuid_solicitud}&actualizar=fail")
            else:
                return redirect(f"/rrhh/solicitudes/?solicitud=noEncontrada")
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")
    
def  modificar_registro_personal(request):
    # Solicitudes del tipo GET y POST
    if "user_uuid" in request.session:
        # Recuperar todos los datos del registro, incluso los que se modificaron
        if request.method == "POST":
            # Metodo POST
            # Logica para modificar el registro en la base de datos
            # Datos Personal
            rut_personal = request.POST["rutPersonal"]
            nombre_personal = request.POST["nombrePersonal"]
            genero_personal = request.POST["generoPersonal"]
            direccion_personal = request.POST["direccionPersonal"]
            # Agregar posibilidad de más telefonos 
            telefonos_personal = []
            telefono_personal = request.POST["telefonoPersonal"]
            telefonos_personal.append(int(telefono_personal)) if telefono_personal else None
            # Datos Cargo
            cargo_personal = request.POST["cargoPersonal"]
            cargo_sueldo = request.POST["cargoSueldo"]
            
            fecha_ingreso = request.POST["fechaIngresoPersonal"]
            año, mes, dia = map(int, fecha_ingreso.split("-"))
            
            area_personal = request.POST["areaPersonal"]
            departamento_personal = request.POST["departamentoPersonal"] 
            # Datos Contactos de Emergencia ( SOLO 1 DE MOMENTO)
            rut_contacto = request.POST["rutContacto"]
            nombre_contacto = request.POST["nombreContacto"]
            relacion_contacto_personal = request.POST["relacionContactoPersonal"]
            # Agregar posibilidad de más telefonos de Contacto
            telefonos_contacto = []
            telefono_contacto = request.POST["telefonoContacto"]
            telefonos_contacto.append(int(telefono_contacto)) if telefono_contacto else None
            # Datos Cargas Familiares ( SOLO 1 DE MOMENTO )
            rut_carga = request.POST["rutCarga"]
            nombre_carga = request.POST["nombreCarga"]
            parentesco_carga =  request.POST["parentescoCarga"]
            genero_carga = request.POST["generoCarga"]
            # Iterar un nuevo objeto Personal para insertar registro en la base de datos
            nuevo_registro = Personal(
                # Datos Personales
                personalRut=str(rut_personal), personalNombre=str(nombre_personal), personalGenero=str(genero_personal), personalDireccion=str(direccion_personal), telefonosPersonal=list(telefonos_personal),
                # Datos Laborales
                cargoNombre=str(cargo_personal), cargoSueldo = float(cargo_sueldo), cargoFechaIngreso=datetime(year=año, month=mes, day=dia), departamentoNombre=str(departamento_personal), areaNombre=str(area_personal),
                # Datos Contactos de Emergencia
                contactoRut=str(rut_contacto), contactoNombre=str(nombre_contacto), contactoRelacionPersonal=str(relacion_contacto_personal), telefonosContacto=list(telefonos_contacto),
                # Datos Cargas Familiares 
                cargaRut=str(rut_carga), cargaNombre=str(nombre_carga), cargaGenero=str(genero_carga), cargaParentesco=str(parentesco_carga)
            )
            # Modificar el registro en la base de datos
            modificar_registro = nuevo_registro.update()
            if modificar_registro.acknowledged == True:
                return redirect(f"/rrhh/nomina/?registro_modificado=ok&rut_personal={rut_personal}")
            else:
                return redirect(f"/rrhh/nomina/?registro_modificado=falló&rut_personal={rut_personal}")
        else:
            # Metodo GET
            return redirect("/rrhh/nomina/")
    else:
        # Usuario no esta autenticado devolver a index login page
         return redirect("/")