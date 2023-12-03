import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from uuid import uuid4
from .usuario import Usuario

class Correo:
    def __init__(self, usuario_correo = str ):
        self.sent_to = usuario_correo
        self.sent_from = "super.trimark@gmail.com"

    def contraseña_temporal(self):
        return str(uuid4().time_low)[0:6]
    
    def send(self):
        gmail_user = "super.trimark@gmail.com"
        gmail_app_password ="lejl augh jffv rshb"
        
        subject = "Olvidé mi Contraseña"
        # Generar contraseña temporal
        contraseña_temporal = self.contraseña_temporal()
        # Iteracion de clase Usuario
        user_forgot = Usuario(email=self.sent_to, password=contraseña_temporal)
        # Actualizar contraseña del registro Usuario por la contraseña temporal generada
        user_forgot.update_password()
        # Enviar Correo con traseña temporal generada
        message = MIMEMultipart()
        message.attach(MIMEText(f"""
                                <h2>Contraseña temporal: <strong>{contraseña_temporal}</strong></h2>
                                <h3>ℹ️ Luego de Iniciar sesión en la plataforma, no olvides cambiar tu contraseña.</h3>
                                """, "html"))
        
        message["From"] = self.sent_from
        message["To"] = self.sent_to
        message["Subject"] = subject
        try:
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(gmail_user, gmail_app_password)
            server.sendmail(self.sent_from, self.sent_to, message.as_bytes())
            server.close()
        except Exception as exception:
            return False
        
# email = Correo(usuario_correo="tomymilla22@gmail.com").send()
# print(email)