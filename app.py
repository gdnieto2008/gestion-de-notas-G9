from datetime import datetime
from flask import Flask, jsonify, render_template, url_for,request,redirect, flash,session
import controlador
from werkzeug.security import generate_password_hash, check_password_hash

from envioemail import enviar_email

app=Flask(__name__)

app.secret_key='mi clave de secreta'+str(datetime.now)


#########Recuperar la informacion desde los formularios#####
###Recuperar y Almancenar los Registros de usuario######################
@app.route('/restablecerclave', methods=['POST'])
def restablece_clave():
    datos=request.form
    print(datos)
    usu=datos['recuuser']
    p1=datos['passwd1']
    p2=datos['passwd2']
    p1enc=generate_password_hash(p1)
    if p1!=p2:
        flash('Contraseñas no Coinciden')
    elif len(p1)<8:
        flash('Las contraseñas no cumplen los niveles de seguridad')
    else:
         resultado=controlador.restablecer_clave(p1enc,usu)
         if resultado:
            flash('La contraseña ha sido restablecida con exito')
         else:
            flash("No ha sido posible restablecer la contraseña")   
    
    return render_template('restablecer.html', datauser=usu)  

@app.route('/validaremail', methods=['POST'])
def validar_email():
    datos=request.form
    usu=datos['username']
    resultado=controlador.validar_email(usu)
    if resultado=='SI':
        flash('Usuario Encontrado: Link de recuperacion enviado al correo')
    elif resultado=='NO':
        flash('Usuario no se encuentra registrado')
    else:
        flash('No se pudo realizar la consulta')        
    return redirect(url_for('recuperar'))

@app.route('/listamensindv', methods=['GET','POST'])
def listar_mens_ind():
    if request.method=='POST':
        datos=request.get_json()
        username=datos['username']
        tipo=datos['tipo']
        if tipo==1:
            resultado=controlador.listar_mensajes(1,'')
        else:    
            resultado=controlador.listar_mensajes(2,username)

        return jsonify(resultado)
    else:
         resultado=controlador.listar_mensajes(1,'') 
         return jsonify(resultado)  


@app.route('/listarmensajes')
def listar_mensajes():
    resultado=controlador.listar_mensajes(1,'')
    return jsonify(resultado)

@app.route('/listarusuarios')
def lista_gral_usuarios():
    resultado=controlador.lista_gral_usuarios()
    return jsonify(resultado)


@app.route('/activar',methods=['POST'])
def activar_cuenta():
    datos=request.form
    username=datos['username']
    codver=datos['codverificacion']
    resultado=controlador.activar_usuario(username,codver)
    if resultado == "SI":
        flash('Cuenta Activada Satisfactoriamente')    
    else:
        flash('Error en Activacion') 

    return redirect(url_for('verificar'))           


@app.route('/validarlogin', methods=['POST'])
def val_user():
    datos=request.form
    username=datos['username']
    passwd=datos['password']
    if username=='' or passwd=='':
        flash('Datos Incompletos')
        return redirect(url_for('login'))
    else:
        resultado=controlador.validar_usuarios(username)
        if resultado==False:
            flash('Error al Ingresar')
            return redirect(url_for('login'))
        else:
            print('Resultado: '+ str(resultado[0]['verificado']))
            if(resultado[0]['verificado']==1):
            
                if check_password_hash(resultado[0]['passwd'],passwd):
                    session['username']=username
                    session['nombre']=resultado[0]['nombre'] +" "+resultado[0]['apellido']
                    return redirect(url_for('mensajeria'))
                else:
                    flash('Contraseña Invalida')
                    return redirect(url_for('login'))

            else:
                return redirect(url_for('verificar'))

    
@app.route('/enviarmensajes',methods=['POST'])
def enviar_mesanjes():
    datos=request.form
    remitente=session['username']
    asunto=datos['asunto']
    destinatario=datos['destinatario']
    cuerpo=datos['cuerpo']
    print('destinatario: ' + destinatario)
    if asunto =='' or destinatario=='seleccione' or cuerpo=='':
        flash('Datos incompletos')
        resultado=False
    else:
        resultado=controlador.insertar_mensajes(remitente,destinatario,asunto,cuerpo)
    if resultado:
        flash('Mensaje Enviado Correctamente')
    else:
        flash('Error en el Envio')   
           
    return redirect(url_for('mensajeria'))   


@app.route('/addregistro', methods=['POST'])
def add_registro():
    datos=request.form
    nom=datos['nombre']
    ape=datos['apellido']
    usu=datos['email']
    p1=datos['pass1']
    p2=datos['pass2']
    p1enc=generate_password_hash(p1)
    validacion=controlador.validar_usuarios(usu)
    if validacion == False:
        if nom=='' or ape=='' or usu=='' or p1=='' or p2=='':
            flash("Datos Incompletos")
        elif p1!=p2:
            flash("Las Contraseñas no coinciden")    
        elif len(p1)<8:
            flash('Contraseña no cumple tamaño minimo')
        else:
            resultado=controlador.insertar_usuarios(nom,ape,usu,p1enc)
            flash('Se ha enviado un código de verificación a su correo, intente iniciar sesion para verificar la cuenta con dicho código')
    else:                                      
        flash('Ya se encuentra registrado')

    return redirect(url_for('registro'))   


#####################Rutas de Navegacion#######################################
@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/salir')
def salir():
    session.clear()
    return redirect(url_for('login'))

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/verificacion')
def verificar():
    return render_template('verificacion.html')


@app.route('/mensajeria')
def mensajeria():
    username=session['username']
    listadouser=controlador.listar_usuarios(username)
    return render_template('mensajeria.html',datauser=listadouser)

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')    

@app.route('/restablecer/<usuario>')
@app.route('/restablecer')
def restablecer(usuario=None):
    if usuario==None:  
        return render_template('restablecer.html')  
    else:    
        return render_template('restablecer.html', datauser=usuario)      

@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.before_request
def proteger_rutas():
    ruta=request.path

    if not 'username' in session and (ruta=='/menu' or ruta=='/mensajeria'):
        flash('Por favor debe loguearse en el sistema')
        return redirect('/login')


if  __name__=='__main__':
     app.run(debug=True)  