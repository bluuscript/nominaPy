from .db import ConnectDB
from pymongo import ASCENDING, DESCENDING
from datetime import date, datetime
import pytz
from uuid import uuid4

class Solicitud:
    def __init__( self, solicitud_uuid = str, rut_solicitante = str, nombre_solicitante = str, asunto = str, descripcion = str, estado_solicitud = str, fecha_ultima_modificacion = date ):
        self.solicitud_uuid = solicitud_uuid if solicitud_uuid is not None else str(uuid4())
        self.rut_solicitante = rut_solicitante
        self.nombre_solicitante = nombre_solicitante
        self.asunto = asunto
        self.descripcion = descripcion
        self.estado_solicitud = estado_solicitud
        self.fecha_emision = datetime.now(tz=pytz.timezone('Chile/Continental'))
        self.fecha_ultima_modificacion = fecha_ultima_modificacion
        # Set dict type for mongodb
        self.solicitud = {
            "solicitud_uuid": self.solicitud_uuid,
            "rut_solicitante": self.rut_solicitante,
            "nombre_solicitante": self.nombre_solicitante,
            "asunto": self.asunto,
            "descripcion": self.descripcion,
            "estado": self.estado_solicitud,
            "fecha_emision": self.fecha_emision,
            "fecha_ultima_modificacion": self.fecha_ultima_modificacion
        }
        # Connect to MongoDB Solicitudes Collection
        self.solicitudCollection = ConnectDB().get_conn().solicitudes

    def get_one(self, solicitud_uuid = str):
        try:
            result = self.solicitudCollection.find_one({"solicitud_uuid": solicitud_uuid})
        except Exception as e:
            print("get one solicitud: ", e)
        return result if result is not None else None
    
    # Obtener todas las solicitudes de todo el personal excepto el personal con rut_usuario_rrhh = rut_solicitante
    def get_all(self, rut_usuario_rrhh = str, numero_pagina = int, solicitudes_por_pagina = int):
        try:
            # Solicitudes del personal  ordenadas por fecha de emison => de las más antiguas a las más recientes
            result = self.solicitudCollection.find(
                {"rut_solicitante":  {"$ne": rut_usuario_rrhh}, "estado": "EN PROCESO" }
                ).sort([("fecha_emision", ASCENDING)]).skip(numero_pagina*solicitudes_por_pagina).limit(solicitudes_por_pagina)
        except Exception as e:
            print("get all solicitudes: ", e)
        return result if result is not None else None
    
    # Guardar un documento solicitud en la base de datos
    def save(self):
        try:
            result = self.solicitudCollection.insert_one(self.solicitud)
        except Exception as e:
            print("save solicitud: ", e)
        # Revisar result para retornar respuesta True o False
        return result.acknowledged if result is not None else None
    
    # Obtener todas las solicitudes de un personal
    def get_all_personal(self, rut_solicitante = str, numero_pagina = int, solicitudes_por_pagina = int):
        try:
            result = self.solicitudCollection.find(
                {"rut_solicitante": rut_solicitante}
                ).sort([("fecha_emision", DESCENDING)]).skip(numero_pagina * solicitudes_por_pagina).limit(solicitudes_por_pagina)
        except Exception as e:
            print("get all solicitudes: ", e)
        return result if result is not None else None
    
    # Actualizar el estado de una solicutd de un personal
    def update(self, solicitud_uuid, estado_solicitud):
        try:
            result = self.solicitudCollection.update_one({"solicitud_uuid": solicitud_uuid}, {"$set": {"estado": estado_solicitud} })
        except Exception as e:
            print("update one solicitud: ", e)
        return result if result is not None else None
    
    def count(self, rut_usuario_rrhh = str):
        try:
            result = self.solicitudCollection.count_documents({"rut_solicitante":  {"$ne": rut_usuario_rrhh}, "estado": "EN PROCESO" })
        except Exception as e:
            print("count solicitudes: ", e)
        return result if result is not None else None
    
    def count_personal(self, rut_solicitante):
        try:
            result = self.solicitudCollection.count_documents({"rut_solicitante": rut_solicitante})
        except Exception as e:
            print("count solicitudes: ", e)
        return result if result is not None else None
    
    def __str__(self) -> str:
        return f"Solicitante: {self.nombre_solicitante} - Asunto: {self.asunto} - Fecha Emision: {self.fecha_emision} - Descripción: {self.descripcion}"
    
# sol = Solicitud(nombre_solicitante="Tomás", asunto="Vacaciones",  descripcion="descripcion")
# print(sol.fecha_emision)