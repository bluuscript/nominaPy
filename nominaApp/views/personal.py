from django.shortcuts import render, redirect
from nominaApp.model.personal import Personal
from nominaApp.model.solicitud import Solicitud
# Utils
from uuid import uuid4
from datetime import datetime
import pytz
import math

# Interfaces del Personal Empresa
def inicio(request): 
    # Solicitud del tipo GET
    if "user_uuid" in request.session:
        # Recuperar datos del sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        context = {
            "rut_usuario": rut_usuario,
            "username": username,
            "tipo_personal": tipo_personal
        }
        return render(request, "personal/index.html", context)
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")

def mi_registro(request):
    # Solicitud del tipo GET
    if "user_uuid" in request.session:
        # Recuperar datos del sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        # Obtener el registro del ususario en base al rut desde base de datos
        mi_registro = Personal().get_one(personal_rut=rut_usuario)
        context = {
            "rut_usuario": rut_usuario,
            "username": username,
            "tipo_personal": tipo_personal,
            "mi_registro": mi_registro if mi_registro is not None else None,
        }
        return render(request, "personal/mi-registro.html", context)
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")

def  modificar_registro(request):
    # Solicitudes del tipo GET y POST
    if "user_uuid" in request.session:
        # Recuperar datos del la sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"] 
        if request.method == "GET":
            # Obtener el registro del ususario en base al rut desde base de datos
            mi_registro = Personal().get_one(personal_rut=rut_usuario)
            context = {
                "rut_usuario": rut_usuario,
                "username": username,
                "tipo_personal": tipo_personal,
                "mi_registro": mi_registro if mi_registro is not None else None,
            }
            return render(request, "personal/modificar-registro.html", context)
        else:
            # Metodo POST | Logica para modificar el registro en la base de datos
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
            modificar_registro = nuevo_registro.update(personal_rut = rut_personal)
            if modificar_registro.acknowledged == True:
                if tipo_personal == "PE":
                    return redirect(f"/personal/mi-registro/?actualizar=success")
                else:
                    return redirect(f"/rrhh/mi-registro/?actualizar=success")
            else:
                if tipo_personal == "PE":
                    return redirect(f"/personal/mi-registro/?actualizar=fail")
                else:
                    return redirect(f"/rrhh/mi-registro/?actualizar=success")
    else:
        # Usuario no esta autenticado devolver a index login page
         return redirect("/")

def enviar_solicitud(request):
    # Solicitudes del tipo GET y POST
    if "user_uuid" in request.session:
        # recuperar datos del sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        if request.method == "GET":
            context = {
                "rut_usuario": rut_usuario,
                "username": username,
                "tipo_personal": tipo_personal,
            }
            return render(request, "personal/enviar-solicitud.html", context)
        else:
            # Metodo POST
            # Logica para enviar la solicitud a la base  de datos
            uuid_solicitud = str(uuid4())
            asunto_solicitud = request.POST["asunto"]
            descripcion_solicitud = request.POST["descripcion"]
            estado = "EN PROCESO"
            nueva_solicitud = Solicitud(solicitud_uuid = uuid_solicitud, rut_solicitante=rut_usuario, nombre_solicitante=username, asunto=asunto_solicitud, 
                                         descripcion=descripcion_solicitud, estado_solicitud= estado, fecha_ultima_modificacion= datetime.now(tz=pytz.timezone("Chile/Continental")) )
            # Enviar nueva solicitud
            enviar_solicitud = nueva_solicitud.save()
            # Respuesta según tipo de personal si la solicitud fue enviada exitosamente
            if  enviar_solicitud:
                if tipo_personal == "RRHH":
                    return redirect(f"/rrhh/mis-solicitudes/?solicitud=enviada&asunto={asunto_solicitud}")
                else:
                    return redirect(f"/personal/mis-solicitudes/?solicitud=enviada&asunto={asunto_solicitud}")
            # Respuesta seun tipo personal, si la solicitud por algun motivo no se  puedo guardar en la base de datos
            else:
                if tipo_personal == "RRHH":
                    return redirect(f"/rrhh/mis-solicitudes/?solicitud=error&asunto={asunto_solicitud}")
                else:
                    return redirect(f"/personal/mis-solicitudes/?solicitud=error&asunto={asunto_solicitud}")
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")

def mis_solicitudes(request):
    # Solicitud del tipo GET
    if "user_uuid" in request.session:
        # recuperar datos del sesion del Usuario
        rut_usuario = request.session["rut_usuario"]
        username = request.session["username"]
        tipo_personal = request.session["tipo_personal"]
        # Recuperar numero de la pagina 
        num_pagina_actual = int(request.GET["page"])  if "page" in request.GET else 1
        solicitudes_por_pagina = 9
        num_solicitudes_pagina = (num_pagina_actual - 1) * solicitudes_por_pagina
        # Recuperar las solicitudes del personal de la base de datos
        mis_solicitudes = Solicitud().get_all_personal(
                                                rut_solicitante=rut_usuario,
                                                numero_pagina=num_pagina_actual - 1, 
                                                solicitudes_por_pagina=solicitudes_por_pagina,
                                            )
        cant_mis_solicitudes = Solicitud().count_personal(rut_solicitante=rut_usuario)
        # Data para Paginación de Solicitudes del Personal
        cantidad_paginas = math.ceil( cant_mis_solicitudes / solicitudes_por_pagina )
        lista_num_paginas = []
        for num in range(0, cantidad_paginas, 1):
            lista_num_paginas.append(num + 1)
        context = {
            # Enviar datos de la session del Usuario
            "rut_usuario": rut_usuario,
            "username": username,
            "tipo_personal": tipo_personal,
            # Validar que existan mis solicitudes
            "mis_solicitudes": mis_solicitudes if cant_mis_solicitudes > 0  and not None else None,
            "cant_mis_solicitudes": cant_mis_solicitudes,
            # Enviar Datos para Paginacion
            "cantidad_paginas": cantidad_paginas,
            "lista_num_paginas": lista_num_paginas,
            "num_pagina_actual": num_pagina_actual,
            "num_solicitudes_pagina": num_solicitudes_pagina,
        }
        return render(request, "personal/mis-solicitudes.html", context)
    else:
        # Usuario no esta autenticado devolver a index login page
        return redirect("/")