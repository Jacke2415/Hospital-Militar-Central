import sqlite3
from sqlite3 import Error
from flask import current_app, g
from werkzeug.security import generate_password_hash

def sql_connection():
    try:
        if 'con' not in g:
            g.con = sqlite3.connect("HospitalMilitar.db")
        return g.con
    except Error:
        print(Error)

def close_db():
    con = g.pop( 'con', None )

    if con is not None:
        con.close()
#listo
def sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo, contraseña):
    strsql = 'INSERT INTO Usuarios(TipoUsuario, Nombre, Apellido, FechaNacimiento, Sexo,TipoIdentificacion, NumeroIdentificacion, Especialidad, Consultorio, Direccion, Telefono, Correo, Contraseña) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (tipo, nombre, apellido, fechaN, sexo, tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo, generate_password_hash(contraseña),)
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(*strsql)
    con.commit()
    con.close()

def sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo,contraseña, cedulae):
    strsql = 'update Usuarios set TipoUsuario = ?, Nombre = ?, Apellido = ?, FechaNacimiento =?, Sexo =?, TipoIdentificacion = ?, NumeroIdentificacion = ?, Especialidad = ?, Consultorio = ?, Direccion = ?, Telefono = ?, Correo = ?, Contraseña = ? where NumeroIdentificacion = ?', (tipo, nombre, apellido, fechaN,sexo, tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo, generate_password_hash(contraseña), cedulae,)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(*strsql)
    con.commit()
    con.close()

def sql_delete_user(cedula):
    strsql = 'delete from Usuarios where NumeroIdentificacion = ?',(cedula,) 
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(*strsql)
    con.commit()
    con.close()

def sql_delete_paciente(cedula):
    strsql = 'DELETE FROM Usuarios WHERE NumeroIdentificacion=?', (cedula,)
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(*strsql)
    con.commit()
    print("usuario eliminado")
    con.close()
#listo
def sql_search_user(cedula):
    strsql = 'select * from Usuarios where NumeroIdentificacion = ?',(cedula,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
#listo
def get_columns_usuario():
    strsql = 'select * from Usuarios'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def get_columns_cita():
    strsql = 'select * from CITA'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def get_columns_hclinica():
    strsql = 'select * from HClinica'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def getMedicos():
    strsql = 'select * from Usuarios where TipoUsuario = ?',('2',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def getCitas():
    strsql = "select * from CITA"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def getHClinica():
    strsql = "select * from HClinica"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

# Obtener Historia CLinica del lado del admin
def sql_search_Hclinica(cedula_usuario):
    strsql = 'select HClinica.IdHistoriaC, Usuarios.NumeroIdentificacion, CITA.HistoriaClinica from HClinica, Usuarios, CITA where Usuarios.NumeroIdentificacion=? and',(cedula_usuario)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
    
# Obtener citas del lado del admin
def sql_search_citas_admin(cedula_usuario):
    strsql = "select Idcita,Paciente,Medico,Fecha,Hora,HistoriaClinica,Calificacion,ComentariosCalificacion,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion= '"+cedula_usuario+"' ;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_search_citas_admin_fecha(fecha):
    strsql = "select * from CITA where fecha= '"+fecha+"' ;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

#------------------------------------------------
def sql_search_user_medico(cedula):
    strsql = "select * from Usuarios where NumeroIdentificacion = '"+cedula+"' AND TipoUsuario = 2;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

# Obtener citas del lado del admin
def sql_search_citas_admin(cedula_usuario):
    strsql = 'select Idcita,Paciente,Medico,Fecha,Hora,HistoriaClinica,Calificacion,ComentariosCalificacion,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion= ?',(cedula_usuario,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response


def sql_search_citas_admin_fecha(fecha):
    strsql = 'select * from CITA where fecha= ?',(fecha,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

#------------------------------------------------
def sql_search_user_medico(cedula):
    strsql = 'select * from Usuarios where NumeroIdentificacion = ? AND TipoUsuario = ?',(cedula,'2',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
#listo
def getPacientes():
    strsql = 'select * from Usuarios where TipoUsuario = ?',('1',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
#listo
def sql_search_user_paciente(cedula):
    strsql = 'select * from Usuarios where NumeroIdentificacion = ? AND TipoUsuario = ?',(cedula, '1',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def sql_search_citaspacientes(cedula):
    strsql = 'select Idcita, Medico, Fecha, Hora, Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion= ? and CITA.Estado= ?',(cedula, 'Pendiente',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
#listo
def sql_search_Historialcitas(cedula):
    strsql = 'select Idcita,Medico,Fecha,Hora,Estado from CITA JOIN Usuarios  ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion = ? and CITA.Estado != ?',(cedula,'Pendiente',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def get_columnas_Cita():  
    strsql = 'select Idcita, Medico, Fecha, Hora, Estado from CITA'
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = list(map(lambda x: x[0], cursor.description))
    return response

def get_especialidad():
    strsql = "select Nombre from ESPECIALIDAD ORDER BY Nombre"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response
#listo
def get_Medicos1():
    strsql = 'select Nombre,Apellido from Usuarios where TipoUsuario= ?', ('2',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response

def sql_actualizarestadocita(idcita):
    strsql = 'update CITA set Estado= ? where idcita= ? and Estado = ?',('Cancelada', idcita, 'Pendiente',)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    con.commit()
    con.close()

def get_columnas_Cita1():  
    strsql = "select Idcita,Paciente,Fecha,Hora,Estado from CITA"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = list(map(lambda x: x[0], cursor.description))
    return response
#listo
def sql_citasmedico(cedula):
    strsql = 'select Idcita,Paciente,Fecha,Hora,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Medico where Usuarios.NumeroIdentificacion= ? ORDER BY Fecha desc',(cedula,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
#listo
def sql_citasmedico_fecha(cedula,Finicial,Ffinal):
    strsql = 'select Idcita,Paciente,Fecha,Hora,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Medico where Usuarios.NumeroIdentificacion= ? and Fecha BETWEEN ? and ? ORDER BY Fecha desc',(cedula, Finicial, Ffinal,)
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(*strsql)
    response = cursor.fetchall()
    return response
   
def llenar_cita(cedula_paciente,_cedula_medico,fecha,hora,historia,calificacion,comentarios,estado):
    strsql = 'insert into Usuarios(TipoUsuario, Nombre, Apellido, FechaNacimiento, Sexo,TipoIdentificacion, NumeroIdentificacion, Especialidad, Consultorio, Direccion, Telefono, Correo, Contraseña)' 'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ('"+tipo+"','"+nombre+"', '"+apellido+"','"+fechaN+"', '"+sexo+"', '"+tipoDocumento+"', '"+cedula+"', '"+especialidad+"', '"+consultorio+"', '"+direccion+"', "+telefono+", '"+correo+"', '"+contraseña+"')
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()
def Obteneridpaciente(cedula):
    strsql = "select IdUsuario from Usuarios where NumeroIdentificacion='"+cedula+"';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def Obteneridmedico(m2,m3):
    strsql = "select IdUsuario from Usuarios where Nombre='"+m3+"' and Apellido='"+m2+"';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_CrearCita(paciente, medico, fecha, hora, historiaclinica,calificacion, comentarios, estado):
    strsql = "insert into CITA(Paciente, Medico, Fecha, Hora, HistoriaClinica,Calificacion, ComentariosCalificacion, Estado) values ('"+paciente+"','"+medico+"', '"+fecha+"','"+hora+"', '"+historiaclinica+"', '"+calificacion+"', '"+comentarios+"', '"+estado+"');"
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def DetallecitaPaciente(idcita1):
    strsql = "select Nombre, Apellido, NumeroIdentificacion, Sexo, FechaNacimiento, CITA.Fecha from Usuarios JOIN CITA ON Usuarios.IdUsuario= CITA.Paciente where CITA.IdCita= '"+idcita1+"' ;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def ActualizarCitapormedico(Fecha,idcita1):
    strsql = "update CITA set Fecha='"+Fecha+"' where IdCita='"+idcita1+"'"
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()
    
