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