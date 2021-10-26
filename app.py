import datetime
from logging import error 
from os import name
from flask import Flask, render_template, request, session, url_for, redirect
import db
from werkzeug.security import check_password_hash

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
        if cedula_init == None:
            if len(encontrado)>0:
                error = f'El número de identificación {cedula} que se desea registrar ya se encuentra en nuestra base de datos'
                href = '/inicio/iniciarSesion'
                link = 'Iniciar Sesion'                
                return render_template('registrar.html', error = error, link = link)
            else:
                especialidad = None
                consultorio = None
                db.sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña)
                error = f'Tú registro ha sido exitoso si deseas iniciar sesión'
                href = '/inicio/iniciarSesion'
                link = 'Iniciar Sesión'
                return render_template('registrar.html', href = href, error = error, link = link)
        else:
            especialidad = None
            consultorio = None
            db.sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña)
            error = f'El registro del paciente con número de identificación {cedula} ha sido exitoso'
            href = '/inicio/iniciarSesion/administrador/paciente'
            link = 'Regresar'
            return render_template('registrar.html', href = href, error = error, link = link)

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
                    session.clear()
                    session['user_id'] = encontrado[0][0]
                    return redirect(url_for('iniciarSesionMedico'))
                elif encontrado[0][1] == 3:
                    session.clear()
                    session['user_id'] = encontrado[0][0]
                    return redirect(url_for('administrador'))
            else:
                error = 'Contraseña incorrecta, intente nuevamente'
                href = '/inicio/iniciarSesion'                
                link = 'Iniciar Sesión'
                return render_template('login.html', href = href, error = error, link = link)
        else:
            href = '/inicio/registro'
            error = f'El usuario con número de identificación {cedula_init} no se encuentra registrado en nuestra base de datos'
            link = 'registrate'            
            return render_template('login.html', href = href, error = error, link = link)

@app.route("/inicio/busqueda", methods = ['POST', 'GET'])
def busqueda():
    return render_template("busqueda.html")

def user(cedula):
    encontrado = db.sql_search_user(cedula)
    today = datetime.datetime.today()
    fechaN = encontrado[0][4]
    fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
    user = {
            'tipo':encontrado[0][1],
            'name' : encontrado[0][2] + ' ' + encontrado[0][3],
            'tipoId': encontrado[0][6],
            'numId': encontrado[0][7],
            'sexo': encontrado[0][5],
            'edad': today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
            'tel': encontrado[0][11],
            'dir': encontrado[0][10]
            }
    return user

@app.route("/inicio/iniciarSesion/Paciente", methods = ['GET', 'POST'])
def iniciarSesionPaciente():
    columnas = []
    busqueda_columnas= db.get_columnas_Cita()
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #if request.method == 'GET':
    encontradas=[]
    historial=[]
    citas= db.sql_search_citaspacientes (cedula_init)
    print(type(citas[0][1]))
    medico=db.get_Medicos1()
    if len(citas)>0:
        for row in citas:
            encontradas.append(row)
        app.logger.info(encontradas)
    else:
        error = "Usuario no Tiene Citas"
        return render_template("principalPaciente.html", user=user, error = error)
    historialcitas=db.sql_search_Historialcitas(cedula_init)
    if len(historialcitas)>0:
        for row in historialcitas:
            historial.append(row)
    
    else:
        error = "Usuario no Tiene Citas"
        return render_template("principalPaciente.html", user = user(cedula_init), error = error)
    return render_template("principalPaciente.html", user=user(cedula_init), cedula=cedula_init, encontradas=encontradas, columnas=columnas, 
    historial=historial)

@app.route("/inicio/iniciarSesion/Paciente/solicitarcita", methods = ['POST', 'GET'])
def SolicitarCita():
    cedula = cedula_init
    medico=[]
    espe=[]
    if request.method=='GET':
        especialidad= db.get_especialidad() 
        if len(especialidad)>0:
            for i in range(len(especialidad)):
                espe.append(especialidad[i][0])
        medicos= db.get_Medicos1() 
        if len(medicos)>0:
            for i in range(len(medicos)):
                medico.append(medicos[i][1]+'  '+medicos[i][0])
                print(medico)
        return render_template("SolicitarCita.html", espe=espe, medico=medico)
    else:
        me=request.form['medico']
        m1=me.split()
        m2=m1[0]
        m3=m1[1]
        pacient=db.Obteneridpaciente(str(cedula))
        medic=db.Obteneridmedico(m2,m3)
        fecha=request.form['fecha']
        hora="7:00 am"
        historiaclinica="null"
        calificacion="null"
        comentarios="null"
        estado="Pendiente"
        paciente=(str(pacient[0][0]))
        medico=(str(medic[0][0]))
        db.sql_CrearCita(paciente, medico, fecha, hora, historiaclinica,calificacion, comentarios, estado)
        Mensaje="Su cita ha Sido Creada Exitosamente"
        return render_template("SolicitarCita.html", cedula=cedula, Mensaje=Mensaje) 
        #return render_template("principalPaciente.html", cedula=cedula, encontradas=encontradas, columnas=columnas, 
        #historial=historial)

    
@app.route("/inicio/iniciarSesion/Paciente/Cancelarcita", methods = ['GET','POST'])
def Cancelarcita():
    cedula = cedula_init
    if request.method=='GET':
        return render_template("CancelarCita.html",cedula=cedula)
    else:
        idcita=request.form['idcita']
        estado='Cancelada'
        db.sql_actualizarestadocita(idcita,estado)
        Mensaje = "Su cita ha Sido Cancelada Exitosamente"
        return render_template("CancelarCita.html",cedula=cedula, Mensaje=Mensaje)

@app.route("/inicio/iniciarSesion/medico", methods=['POST', 'GET'])
def iniciarSesionMedico():
    cedula = cedula_init
    if request.method=='GET':
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
        return render_template("principalMedico.html", user=user(cedula_init),encontradas=encontradas,columnas=columnas)
    else:    
      
        Finicial=request.form['fechainicial']
        Ffinal=request.form['fechafinal']
        global idcita1
        idcita1=request.form['detallecita']
        columnas = []
        busqueda_columnas= db.get_columnas_Cita1()
        for i in busqueda_columnas:
            columnas.append(f'{i}')
        encontradas1=[]
        citas= db.sql_citasmedico_fecha(str(cedula),Finicial,Ffinal)
        if len(citas)>0:
            for row in citas:
                encontradas1.append(row)
            app.logger.info(encontradas1)
            
        return render_template("principalMedico.html", user=user(),encontradas1=encontradas1,columnas=columnas)

@app.route("/inicio/iniciarSesion/actualizarDatos", methods = ['GET', 'POST'])
def actualizarDatos():
    if request.method == 'GET':
        return render_template("actualizarDatosMedico.html")
    else:
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
        if user(cedula_init)['tipo'] == 2:
            if cedula_init == cedula:
                tipo = '2'
                db.sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña, cedula_init)
                error = 'Tú actualización de datos ha sido exitoso si deseas regresar nuevamente a tu sesión'
                href = '/inicio/iniciarSesion/medico'
                link = 'regresar'
                return render_template('actualizarDatosMedico.html', href = href, error = error, link = link)
            else:
                error = 'El número de identificación del usuario no coincide'
                error1 = 'Si deseas volver a tu sesión sin actualizar tus datos da cick en'
                href = '/inicio/iniciarSesion/medico/actualizarDatos'
                href1 = '/inicio/iniciarSesion/medico'
                link = 'Intentar actualizar Datos nuevamente'
                link1 = 'Mi Sesión'
                return render_template('actualizarDatosMedico.html', href = href, href1 = href1, error = error, error1 = error1, link = link, link1 = link1)
        elif user(cedula_init)['tipo'] == 3:
                if cedula_a_buscar_medico == cedula:
                    tipo = '2'
                    db.sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña, cedula_a_buscar_medico)
                    error = f'La actualización de datos del médico con número de identificacion {cedula} ha sido exitosa'
                    return render_template('administradorMedico.html', user = user(cedula_init), error = error)
            
                elif cedula_a_buscar_paciente == cedula:
                    tipo = '1'
                    db.sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña, cedula_a_buscar_paciente)
                    error = f'La actualización de datos del paciente con número de identificacion {cedula} ha sido exitosa'
                    return render_template('administradorPaciente.html', user = user(cedula_init), error = error)          

@app.route("/inicio/iniciarSesion/medico/Verdetallecita", methods=['POST', 'GET'])
def verDetalleMedico():
   
    if request.method == 'GET':
        pa=db.DetallecitaPaciente(str(idcita1))
        if len(pa)>0:
            today = datetime.datetime.today()
            fechaN = pa[0][4]
            fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
            global detallecitap
            detallecitap={
                'nombre':pa[0][0]+' '+pa[0][1],
                'cedula':pa[0][2],
                'sexo':pa[0][3],
                'edad':today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
                'fecha':pa[0][5],
                'hora':'7:00 am'
                }
            return render_template("detallecitamedico.html", idcita1=idcita1, detallecitap=detallecitap)
    else:
        fechao=request.form['FechaC']
        db.ActualizarCitapormedico(fechao,str(idcita1))
        Mensaje="La Cita ha Sido Actualizada Exitosamente"
        pa=db.DetallecitaPaciente(str(idcita1))
        if len(pa)>0:
            today = datetime.datetime.today()
            fechaN = pa[0][4]
            fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
            nombre=pa[0][0]+' '+pa[0][1]
            detallecitap={
                'nombre':pa[0][0]+' '+pa[0][1],
                'cedula':pa[0][2],
                'sexo':pa[0][3],
                'edad':today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
                'fecha':pa[0][5],
                'hora':'7:00 am'
                }
            return render_template("detallecitamedico.html", idcita1=idcita1,detallecitap=detallecitap,Mensaje=Mensaje)

@app.route("/inicio/iniciarSesion/medico/Verdetallecita/aceptarcita", methods=['POST'])  
def medicoaceptacita():
    cedula = cedula_init
    print(idcita1)
     
    estado='Aceptada'
    db.sql_actualizarestadocita(str(idcita1),estado)
    Mensaje='La cita ha Sido Aceptada'
    pa=db.DetallecitaPaciente(str(idcita1))
    if len(pa)>0:
        today = datetime.datetime.today()
        fechaN = pa[0][4]
        fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
        nombre=pa[0][0]+' '+pa[0][1]
        detallecitap={
            'nombre':pa[0][0]+' '+pa[0][1],
            'cedula':pa[0][2],
            'sexo':pa[0][3],
            'edad':today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
            'fecha':pa[0][5],
            'hora':'7:00 am'
            }
        return render_template("detallecitamedico.html", idcita1=idcita1,Mensaje=Mensaje, detallecitap=detallecitap)

@app.route("/inicio/iniciarSesion/medico/Verdetallecita/cancelarcita", methods=['POST'])  
def medicocancelacita():
    cedula = cedula_init
    
   
     
    estado='Cancelada'
    db.sql_actualizarestadocita(str(idcita1),estado)
    Mensaje='La cita ha Sido Cancelada'
    pa=db.DetallecitaPaciente(str(idcita1))
    if len(pa)>0:
        today = datetime.datetime.today()
        fechaN = pa[0][4]
        fechaN = datetime.datetime.strptime(fechaN, "%Y-%m-%d")
        nombre=pa[0][0]+' '+pa[0][1]
        detallecitap={
            'nombre':pa[0][0]+' '+pa[0][1],
            'cedula':pa[0][2],
            'sexo':pa[0][3],
            'edad':today.year - fechaN.year - ((today.month, today.day) < (fechaN.month, fechaN.day)),
            'fecha':pa[0][5],
            'hora':'7:00 am'
            }
        return render_template("detallecitamedico.html", idcita1=idcita1,Mensaje=Mensaje, detallecitap=detallecitap)

    

@app.route("/inicio/iniciarSesion/administrador")
def administrador():
    cedula_a_buscar_medico = None
    cedula_a_buscar_medico = None
    return render_template("administrador.html", user = user(cedula_init))

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
        return render_template("administradorPaciente.html", user = user(cedula_init), columnas=columnas, pacientes=pacientes)
    else:
        coincidencia = []
        global cedula_a_buscar_paciente 
        cedula_a_buscar_paciente = request.form['cedula']
        busqueda_cedula = db.sql_search_user_paciente(cedula_a_buscar_paciente)
        if len(busqueda_cedula)>0:
            cond = True
            for i in range(len(busqueda_columnas)):
                coincidencia.append(f'{busqueda_cedula[0][i]}')
            return render_template("administradorPaciente.html", user=user(cedula_init), coincidencia=coincidencia, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula_a_buscar_paciente} no se encuentra registrado '
            return render_template("administradorPaciente.html", user=user(cedula_init), error = error)

@app.route("/inicio/iniciarSesion/administrador/eliminarPaciente", methods=['POST', 'GET'])
def eliminarPaciente():
    cedula_eliminar = cedula_a_buscar_paciente
    db.sql_delete_user(cedula_eliminar)
    error = f'El paciente con cédula {cedula_eliminar} fue elminado exitosamente'
    return render_template("administradorPaciente.html", user=user(cedula_init), error = error)

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
        return render_template("administradorMedico.html", user=user(cedula_init), columnas=columnas,medicos=medicos)
    else:
        coincidencia = []
        global cedula_a_buscar_medico 
        cedula_a_buscar_medico = request.form['cedula']
        busqueda_cedula = db.sql_search_user_medico(cedula_a_buscar_medico)
        if len(busqueda_cedula)>0:
            cond = True
            for i in range(len(busqueda_columnas)):
                coincidencia.append(f'{busqueda_cedula[0][i]}')
            return render_template("administradorMedico.html", user = user(cedula_init), coincidencia=coincidencia, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula_a_buscar_medico} no se encuentra registrado '
            return render_template("administradorMedico.html", error = error)

@app.route("/inicio/iniciarSesion/administrador/eliminarMedico", methods=["POST", "GET"])
def eliminarMedico():
    cedula_eliminar = cedula_a_buscar_medico
    db.sql_delete_paciente(cedula_eliminar)
    error = f'El médico con cédula {cedula_eliminar} fue elminado exitosamente'
    return render_template("administradorMedico.html", user=user(cedula_init), error = error)
 
@app.route("/inicio/iniciarSesion/administrador/medico/registroMedico", methods = ['GET', 'POST'])
def registroMedico():
    if request.method == 'GET':
        return render_template("registroMedico.html")
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
        encontrado = db.sql_search_user(cedula)
        if len(encontrado)>0:
            error = 'El medico que desea registrar ya se encuentra en nuestra base de datos'
            return render_template("administradorMedico.html", error = error)
        else:
            db.sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoId, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña)
            error = 'El medico ha sido registrado exitosamente'
            return render_template("administradorMedico.html", error = error)  

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
        return render_template("administradorCitas.html", user = user(cedula_init), columnas=columnas,citas=citas)
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
            for row in busqueda_cedula:
                coincidencias.append(row)
            return render_template("administradorCitas.html", coincidencias=coincidencias, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula} no se encuentra registrado '
            return render_template("administradorCitas.html", error = error)

@app.route("/inicio/iniciarSesion/administrador/hclinica",methods=['POST', 'GET'])
def administradordHClinica():
    #montar los nombres de las columnas para la tabla de la vista
    columnas = []
    busqueda_columnas = db.get_columns_hclinica()
    # Agrego a columnas los nombres de las columnas busacado en bd
    for i in busqueda_columnas:
        columnas.append(f'{i}')
    #Organizo la informcion mostrada por defecto, todos los medicos
    hClinicas = []
    dbCitas = db.getHClinica()
    for row in dbCitas:
        hClinicas.append(row)
    
    if request.method == 'GET':
        return render_template("administradorHistoriaClinica.html", user= user(cedula_init),columnas=columnas,hClinicas=hClinicas)
    else:
        coincidencias = []
        cedula = request.form['cedula']
        app.logger.info(cedula)
        # cedula_medico_cita = request.form['medico']
        # fecha_cita = request.form['fecha']
        busqueda_cedula = db.sql_search_Hclinica(cedula)
        app.logger.info(busqueda_cedula)
        if len(busqueda_cedula)>0:
            cond = True
            for row in busqueda_cedula:
                coincidencias.append(row)
            return render_template("administradorHistoriaClinica.html", coincidencias=coincidencias, columnas=columnas,cond=cond)
        else:
            error = f'El usuario con la identificacion {cedula} no se encuentra registrado '
            return render_template("administradorHistoriaClinica.html", error = error)


@app.route("/inicio/iniciarSesion/administrador/agenda")
def administradordAgenda():
    return render_template("administradorAgenda.html", user=user(cedula_init))

@app.route("/inicio/iniciarSesion/administrador/ayuda")
def administradordAyuda():
    return render_template("administradorAyuda.html", user = user(cedula_init))

@app.route("/inicio/iniciarSesion/medico/detalleCita")
def detalleCita():
    return render_template("detallecitamedico.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('iniciarSesion'))


