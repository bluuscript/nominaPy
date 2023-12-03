from .db import ConnectDB
import bcrypt

class Usuario:
    def __init__(self, rut = "", username = "", email = "", tipo_personal = "", password = ""):
        self.rut = rut
        self.username = username
        self.email = email
        self.tipo_personal = tipo_personal
        self.password = password
        # Set dict type for mongodb
        self.user= {
            "rut": self.rut,
            "username": self.username,
            "email": self.email,
            "tipo_personal": self.tipo_personal,
            "password": self.get_hashed_password() if self.password is not None else None
        }
        # Connect to MongoDB Usuarios Collection
        self.userCollection = ConnectDB().get_conn().get_collection("usuarios")
    
    # Verificar que existencia de registro de Usuario   
    def exist(self):
        try:
            result =  self.userCollection.find_one({ "$or": [{"email": self.email}, {"rut": self.rut }] })
        except Exception as e:
            print("Error al verificar exitencia usuario:  ", e)
            result = e
        return True if result is not None else False
    
    # Obtener un registro Usuario a partir de Correo
    def get(self):
        try:
            result = self.userCollection.find_one({"email": self.email})
        except Exception as e:
            print("Error al buscar usuario:  ", e)
            result = e
        return result if result is not None else None
    
    # Insertar un registro Usuario en la base de datos
    def save(self):
        try:
            result = self.userCollection.insert_one(self.user)
        except Exception as e:
            print("Error al insertar usuario:  ", e)
        return result.acknowledged
    
    # Actualizar la contraseña del registro Usuario en la base de datos
    def update_password(self):
        try:
            result = self.userCollection.update_one({"email": self.email}, {"$set": {"password": self.get_hashed_password()}})
        except Exception as e:
            print("Error al actualizar usuario:  ", e)
        return result.acknowledged
    
    # Encriptar la contraseña  del objeto iterado a partir de la clase Usuario
    def get_hashed_password(self):
        return bcrypt.hashpw(self.password, bcrypt.gensalt())

    # Validar que la contraseña encriptada del objeto iterado sea igual a la del registro Usuario en la base de datos
    def check_password(self):
        get_password = self.get()['password']
        return bcrypt.checkpw(self.password, get_password)

    # Metodo de Clase para imprimir los valores del objeto iterado
    def __str__(self):
        return f"rut: {self.rut} - username: {self.username} - email: {self.email} - Tipo Personal: {self.tipo_personal} - password: {self.password}"

# user= Usuario("20-9", "test", "anpch@example.com", "rrhh", "123")
# print(user)
