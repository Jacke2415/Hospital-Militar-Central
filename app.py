import datetime 
from os import name
from flask import Flask, render_template, request, session, url_for, redirect
from werkzeug.security import check_password_hash
import db

app = Flask(__name__)
app.secret_key = 'team5'

@app.route("/")
def inicio():
    return render_template("Principal.html")

@app.route("/inicio")
def principal():
    return render_template("Principal.html")

@app.route("/inicio/registro", methods = ['POST', 'GET'])
def registro():
    if request.method == 'GET':
        return render_template("registrar.html")
    else:
        tipo = '1'
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fechaN = request.form['fechaN']
        sexo = request.form['sexo']
        tipoId = request.form['tipoId']
        cedula = request.form['cedula']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = request.form['password']
        encontrado = db.sql_search_user(cedula)
        if len(encontrado)>0:
            return '<h1>El número de identificación registrado ya se encuentra en nuestra base de datos <a class="link" href="iniciarSesion">Iniciar Sesión</a></h1>'
        else:
            especialidad = 'NoAplica'
            consultorio = 'NoAPlica'
            db.sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña)
            return '<h1>Tú registro ha sido exitoso si deseas iniciar sesión <a class="link" href="iniciarSesion">Iniciar Sesión</a></h1></br><h1>Si deseas volver a nuestra pagina principal <a class="link" href="/inicio">Inicio</a></h1>'

@app.route("/inicio/iniciarSesion", methods = ['POST', 'GET'])
def iniciarSesion():
    if request.method == 'GET':
        return render_template("login.html")
    else:
        global cedula_init
        cedula_init = request.form['cedula']
        contraseña = request.form['password']
        encontrado = db.sql_search_user(cedula_init)
        if len(encontrado)>0: 
            if check_password_hash(encontrado[0][13], contraseña):
                if encontrado[0][1] == 1:
                    session.clear()
                    session['user_id'] = encontrado[0][0]
                    return redirect(url_for('iniciarSesionPaciente'))
                elif encontrado[0][1] == 2:
                    return redirect(url_for('iniciarSesionMedico'))
                elif encontrado[0][1] == 3:
                    return redirect(url_for('administrador'))
            else:
                return '<h1>Contraseña incorrecta, intentar de nuevo <a class="link" href="iniciarSesion">Iniciar Sesión</a></h1>'
        else:
            return '<h1>El usuario no se encuentra registrado <a class="link" href="registro">Regitrate</a></br><h1>Si fue un error inicia sesión nuevamente <a class="link" href="iniciarSesion">Iniciar Sesión</a></h1>'

@app.route("/inicio/busqueda", methods = ['POST', 'GET'])
def busqueda():
    return render_template("busqueda.html")

@app.route("/inicio/iniciarSesion/Paciente", methods = ['GET', 'POST'])
def iniciarSesionPaciente():
    cedula = cedula_init
    encontrado = db.sql_search_user(cedula)
    today = datetime.datetime.today()
    fechaN = encontrado[0][4]
    fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
    user = {
            'name' : encontrado[0][2] + ' ' + encontrado[0][3],
            'tipoId': encontrado[0][6],
            'numId': encontrado[0][7],
            'sexo': encontrado[0][5],
            'edad': today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
            'tel': encontrado[0][11],
            'dir': encontrado[0][10]
            }
    columnas = []
    
    busqueda_columnas= db.get_columnas_Cita()
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #if request.method == 'GET':
    encontradas=[]
    historial=[]
    citas= db.sql_search_citaspacientes (str(cedula))
    medico=db.get_Medicos1()
    if len(citas)>0:
        for row in citas:
            encontradas.append(row)
        app.logger.info(encontradas)
    historialcitas=db.sql_search_Historialcitas(str(cedula))
    if len(historialcitas)>0:
        for row in historialcitas:
            historial.append(row)
    else:
        error = "Usuario no Tiene Citas"
        return render_template("principalPaciente.html",user=user, error = error)
    return render_template("principalPaciente.html", user=user, cedula=cedula, encontradas=encontradas, columnas=columnas, 
    historial=historial)
    
@app.route("/inicio/iniciarSesion/Paciente/solicitarcita", methods = ['POST', 'GET'])
def SolicitarCita():
    cedula=request.args.get('cedula')
    medico=[]
    espe=[]
    if request.method=='GET':
        especialidad= db.get_especialidad() 
        if len(especialidad)>0:
            for i in range(len(especialidad)):
                espe.append(f'{especialidad[i]}')
    
        #opcion=request.form['especialidad']
        #print(opcion)
        medicos= db.get_Medicos1() 
        if len(especialidad)>0:
            for i in range(len(medicos)):
                medico.append(f'{medicos[i]}')
    return render_template("SolicitarCita.html", espe=espe, medico=medico)
    
@app.route("/inicio/iniciarSesion/Paciente/Cancelarcita", methods = ['GET','POST'])
def Cancelarcita():
    cedula=request.args.get('cedula')
    
    if request.method=='GET':
        return render_template("CancelarCita.html",cedula=cedula)
    else:
        idcita=request.form['idcita']
        db.sql_actualizarestadocita(idcita)
        Mensaje = "Su cita ha Sido Cancelada Exitosamente"
        return render_template("CancelarCita.html",cedula=cedula, Mensaje=Mensaje)

@app.route("/inicio/iniciarSesion/medico", methods=['POST', 'GET'])
def iniciarSesionMedico():
    cedula = cedula_init
    encontrado = db.sql_search_user(cedula)
    today = datetime.datetime.today()
    fechaN = encontrado[0][4]
    fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
    user = {
            'name' : encontrado[0][2] + ' ' + encontrado[0][3],
            'tipoId': encontrado[0][6],
            'numId': encontrado[0][7],
            'especialidad': encontrado[0][8],
            'consultorio': encontrado[0][9],
            'sexo': encontrado[0][5],
            'edad': today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
            'tel': encontrado[0][11],
            'dir': encontrado[0][10]
            }
    
    columnas = []
    
    busqueda_columnas= db.get_columnas_Cita1()
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    
    encontradas=[]
    citas= db.sql_citasmedico(str(cedula))
    if len(citas)>0:
        for row in citas:
            encontradas.append(row)
        app.logger.info(encontradas)
    return render_template("principalMedico.html", user=user,encontradas=encontradas,columnas=columnas)
        
    if request.method=='POST':
        Finicial=request.form['fechainicial']
        Ffinal=request.form['fechafinal']
        columnas = []
        print(Finicial)
        print(Ffinal)
        busqueda_columnas= db.get_columnas_Cita1()
        for i in busqueda_columnas:
            columnas.append(f'{i}')
        encontradas1=[]
        citas= sql_citasmedico_fecha(str(cedula),Finicial,Ffinal)
        if len(citas)>0:
            for row in citas:
                encontradas1.append(row)
            app.logger.info(encontradas1)
        return render_template("principalMedico.html", user=user,encontradas1=encontradas1,columnas=columnas)

@app.route("/inicio/iniciarSesion/medico/actualizarDatos", methods = ['GET', 'POST'])
def actualizarDatos():
    if request.method == 'GET':
        return render_template("actualizarDatosMedico.html")
    else:
        tipo = '2'
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fechaN = request.form['fechaN']
        sexo = request.form['sexo']
        tipoId = request.form['tipoId']
        cedula = request.form['cedula']
        especialidad = request.form['especialidad']
        consultorio = request.form['nconsultorio']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        correo = request.form['correo']
        contraseña = request.form['password']
        cedulae = cedula_init
        if cedulae == cedula:                
            print(type(cedulae), type(cedula))
            db.sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña, cedulae)
            return '<h1>Tú actualización de datos ha sido exitoso si deseas regresar nuevamente a tu sesión <a class="link" href="/inicio/iniciarSesion/medico">Mi Sesión</a></h1></br><h1>Si deseas volver a nuestra pagina principal <a class="link" href="/inicio">Inicio</a></h1>'
        else:
            return '<h1>El número de identificación del usuario no coincide, <a class="link" href="/inicio/iniciarSesion/medico/actualizarDatos">Intentar actualizar Datos nuevamente</a></h1></br><h1>Si deseas volver a tu sesión sin actualizar tus datos da cick en <a class="link" href="/inicio/iniciarSesion/medico">Mi Sesión</a></h1>'

@app.route("/inicio/iniciarSesion/administrador")
def administrador():
    return render_template("administrador.html")

@app.route("/inicio/iniciarSesion/administrador/paciente",methods=['POST', 'GET'])
def administradorPaciente():
    #comentario de prueba frank
    columnas = []
    busqueda_columnas = db.get_columns_usuario()
    # Agrego a columnas los nombres de las columnas buscado en bd
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #Organizo la información mostrada por defecto, todos los médicos
    pacientes = []
    dbpacientes = db.getPacientes()
    for row in dbpacientes:
        pacientes.append(row)
    if request.method == 'GET':
        return render_template("administradorPaciente.html",columnas=columnas,pacientes=pacientes)
    else:
        coincidencia = []
        global cedula_a_buscar_paciente 
        cedula_a_buscar_paciente = request.form['cedula']
        busqueda_cedula = db.sql_search_user_paciente(cedula_a_buscar_paciente)
        if len(busqueda_cedula)>0:
            cond = True
            for i in range(len(busqueda_columnas)):
                coincidencia.append(f'{busqueda_cedula[0][i]}')
            return render_template("administradorPaciente.html", coincidencia=coincidencia, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula_a_buscar_paciente} no se encuentra registrado '
            return render_template("administradorPaciente.html", error = error)

@app.route("/eliminarPaciente", methods=['POST'])
def eliminarPaciente():
    cedula_eliminar = cedula_a_buscar_paciente
    db.sql_delete_paciente(cedula_eliminar)
    return '<h1>El paciente con cedula ' + cedula_eliminar + 'fue eliminado' + '<a class="link" href="/inicio/iniciarSesion/administrador/paciente">Regresar</a></br><h1>'
#--------------------------------------------

@app.route("/inicio/iniciarSesion/administrador/medico",methods=['POST', 'GET'])
def administradorMedico():
    #montar los nombres de las columnas para la tabla de la vista
    columnas = []
    busqueda_columnas = db.get_columns_usuario()
    # Agrego a columnas los nombres de las columnas busacado en bd
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #Organizo la informcion mostrada por defecto, todos los medicos
    medicos = []
    dbmedicos = db.getMedicos()
    for row in dbmedicos:
        medicos.append(row)
    app.logger.info(medicos[1][3])
    if request.method == 'GET':
        return render_template("administradorMedico.html",columnas=columnas,medicos=medicos)
    else:
        coincidencia = []
        global cedula_a_buscar_medico 
        cedula_a_buscar_medico = request.form['cedula']
        busqueda_cedula = db.sql_search_user_medico(cedula_a_buscar_medico)
        if len(busqueda_cedula)>0:
            cond = True
            for i in range(len(busqueda_columnas)):
                coincidencia.append(f'{busqueda_cedula[0][i]}')
            return render_template("administradorMedico.html", coincidencia=coincidencia, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula_a_buscar_medico} no se encuentra registrado '
            return render_template("administradorMedico.html", error = error)

@app.route("/eliminarMedico", methods=['POST'])
def eliminarMedico():
    cedula_eliminar = cedula_a_buscar_medico
    db.sql_delete_paciente(cedula_eliminar)
    return '<h1>El medico con cedula ' + cedula_eliminar + 'fue eliminado' + '<a class="link" href="/inicio/iniciarSesion/administrador/paciente">Regresar</a></br><h1>'
 
@app.route("/inicio/iniciarSesion/administrador/medico/registroMedico")
def registroMedico():
    return render_template("registroMedico.html")

@app.route("/inicio/iniciarSesion/administrador/citas",methods=['POST', 'GET'])
def administradorCitas():
    #montar los nombres de las columnas para la tabla de la vista
    columnas = []
    busqueda_columnas = db.get_columns_cita()
    # Agrego a columnas los nombres de las columnas busacado en bd
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #Organizo la informcion mostrada por defecto, todos los medicos
    citas = []
    dbCitas = db.getCitas()
    for row in dbCitas:
        citas.append(row)
    
    if request.method == 'GET':
        return render_template("administradorCitas.html",columnas=columnas,citas=citas)
    else:
        coincidencias = []
        cedula = request.form['cedula']
        app.logger.info(cedula)
        # cedula_medico_cita = request.form['medico']
        # fecha_cita = request.form['fecha']
        busqueda_cedula = db.sql_search_citas_admin(cedula)
        app.logger.info(busqueda_cedula)
        if len(busqueda_cedula)>0:
            cond = True
            app.logger.info("prueba")
            for row in busqueda_cedula:
                coincidencias.append(row)
            return render_template("administradorCitas.html", coincidencias=coincidencias, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula} no se encuentra registrado '
            return render_template("administradorCitas.html", error = error)

@app.route("/inicio/iniciarSesion/administrador/hclinica")
def administradordHClinica():
    return render_template("administradorHistoriaClinica.html")

@app.route("/inicio/iniciarSesion/administrador/agenda")
def administradordAgenda():
    return render_template("administradorAgenda.html")

@app.route("/inicio/iniciarSesion/administrador/ayuda")
def administradordAyuda():
    return render_template("administradorAyuda.html")

@app.route("/inicio/iniciarSesion/medico/detalleCita")
def detalleCita():
    return render_template("detallecitamedico.html")

@app.route( '/logout' )
def logout():
    session.clear()
    return redirect(url_for('iniciarSesion'))


