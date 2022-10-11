from email.message import EmailMessage
import smtplib

def enviar_email(email_destino,codigo):
    remitente = "stevenforero@uninorte.edu.co"
    destinatario = email_destino
    mensaje = "Codigo de Confirmacion: " + codigo
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Codigo de Activacion Cuenta en Plataforma Instamensajes"
    email.set_content(mensaje)
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "Electronico-97")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()

def recuperar_email(email_destino):
    remitente = "stevenforero@uninorte.edu.co"
    destinatario = email_destino
    mensaje="<hr>"
    mensaje = "<h2>Recuperacion de Cuenta</h2>"
    mensaje =mensaje+ "<a href='https://proyectogrupo9mintic.herokuapp.com/restablecer/"+ email_destino +"'>Ingrese Aqui para restablecer su contraseña</a>"
    #mensaje =mensaje+ "<a href='http://localhost:5000/restablecer/"+ email_destino +"'>Ingrese Aqui para restablecer su contraseña</a>" 
    mensaje=mensaje+"<hr>"
    email = EmailMessage()
    email["From"] = remitente
    email["To"] = destinatario
    email["Subject"] = "Recuperar Contraseña" 
    email.set_content(mensaje, subtype="html")
    smtp = smtplib.SMTP("smtp-mail.outlook.com", port=587)
    smtp.starttls()
    smtp.login(remitente, "Electronico-97")
    smtp.sendmail(remitente, destinatario, email.as_string())
    smtp.quit()