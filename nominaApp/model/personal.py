from .db import ConnectDB
from datetime import datetime
from pymongo import DESCENDING

class Personal:
    def __init__(self, 
                 # Datos Personales
                 personalRut = str, personalNombre = str, personalGenero = str, personalDireccion = str,  telefonosPersonal = list,
                 # Datos Laborales
                 cargoNombre = str, cargoFechaIngreso = datetime, cargoSueldo = float, departamentoNombre = str, areaNombre = str,
                 # Datos Contactos de Emergencia
                 contactoRut = str, contactoNombre = str, contactoRelacionPersonal = str, telefonosContacto = list, 
                 # Datos Cargas
                 cargaRut = str, cargaNombre = str, cargaGenero = str, cargaParentesco = str): 
        #Tabla Personal
        self.personalRut = personalRut
        self.personalNombre = personalNombre
        self.personalGenero = personalGenero
        self.personalDireccion = personalDireccion
        # Tabla Cargo
        self.cargoNombre = cargoNombre
        self.cargoFechaIngreso = cargoFechaIngreso
        self.cargoSueldo = cargoSueldo
        # Tabla Departamento
        self.departamentoNombre = departamentoNombre
        self.areaNombre = areaNombre
        # Tabla TelefonosPersonal
        self.telefonosPersonal= telefonosPersonal
        # Tabla CargasFamiliares
        self.cargaRut = cargaRut
        self.cargaNombre = cargaNombre
        self.cargaGenero = cargaGenero
        self.cargaParentesco = cargaParentesco
        # Tabla ContactosEmergencia
        self.contactoRut = contactoRut
        self.contactoNombre = contactoNombre
        self.contactoRelacionPersonal = contactoRelacionPersonal 
        self.telefonosContacto = telefonosContacto
            # Set dict type for mongodb
        self.personal = {
            "personalRut": self.personalRut,
            "personalNombre":  self.personalNombre,
            "personalGenero":  self.personalGenero,
            "personalDireccion":  self.personalDireccion,
            "telefonosPersonal": telefonosPersonal, 
            "cargo": {
                "cargoNombre":  self.cargoNombre,
                "cargoFechaIngreso": self.cargoFechaIngreso,
                "cargoSueldo":  self.cargoSueldo,
                "departamentoNombre":  self.departamentoNombre,
                "areaNombre":  self.areaNombre,
            },
            "cargaFamiliar": [{
                "cargaRut": self.cargaRut,
                "cargaNombre": self.cargaNombre
                ,"cargaGenero": self.cargaGenero
                ,"cargaParentesco": self.cargaParentesco
            }],
            "contactosEmergencia": [{
                "contactoRut":  self.contactoRut,
                "contactoNombre":  self.contactoNombre,
                "contactoRelacionPersonal":  self.contactoRelacionPersonal
                ,"telefonosContacto": self.telefonosContacto, 
            }]
            }
        # Connect to MongoDB Personal Collection
        self.personalCollection = ConnectDB().get_conn().get_collection('personal')
    
    # Método para verificar existencia de personal o bien de su registro
    def exist(self):
        try:
            result = self.personalCollection.find_one({"personalRut": self.personalRut})
        except Exception as e:
            print("exist personal, error: ", e)
        return True if result is not None else False
    
    def get_one(self, personal_rut = str):
        try:
            result = self.personalCollection.find_one({"personalRut": personal_rut})
        except Exception as e:
            print("get registro personal, error: ", e)
        return result if result is not None else None
    
    # Recuperar todos los registros del personal
    def get_all(self, rut_usuario_rrhh = str, numero_pagina = int, registros_por_pagina = int):
        try:
            result = self.personalCollection.find(
                {"personalRut": {"$ne": rut_usuario_rrhh}}
                ).sort([("cargo.cargoFechaIngreso", DESCENDING)]).skip(numero_pagina * registros_por_pagina).limit(registros_por_pagina)
        except Exception as e:
            print("get registro personal: ",e)
        return result if result is not None else None
    
    def update(self):
        try:
            result = self.personalCollection.update_one({"personalRut": self.personalRut}, {"$set": self.personal})
        except Exception as e:
            print("update registro personal: ",e)
        # Revisar que devuelve result
        return result if result is not None else None
    
    def save(self):
        try:
            result = self.personalCollection.insert_one(self.personal)
        except Exception as e:
            print("insert registro personal: ",e)
        return result if result is not None else None
    
    def delete(self, personal_rut = str):
        try:
            result = self.personalCollection.delete_one({"personalRut": personal_rut})
        except Exception as e:
            print("delete registro personal: ",e)
        # Revisar que devuelve result
        return result if result is not None else None
    
    def count(self, rut_usuario_rrhh = str):
        try:
            result = self.personalCollection.count_documents({"personalRut": {"$ne": rut_usuario_rrhh}})
        except Exception as e:
            print("count registro personal: ",e)
        return result if result is not None else None