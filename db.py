import sqlite3
from sqlite3 import Error

def sql_connection():
    try:
        con = sqlite3.connect("HospitalMilitar.db")
        return con
    except Error:
        print(Error)

def sql_insert_user(tipo, nombre, apellido, fechaN, sexo,tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo,contraseña):
    strsql = 'insert into Usuarios(TipoUsuario, Nombre, Apellido, FechaNacimiento, Sexo,TipoIdentificacion, NumeroIdentificacion, Especialidad, Consultorio, Direccion, Telefono, Correo, Contraseña)' 'values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', ('"+tipo+"','"+nombre+"', '"+apellido+"','"+fechaN+"', '"+sexo+"', '"+tipoDocumento+"', '"+cedula+"', '"+especialidad+"', '"+consultorio+"', '"+direccion+"', "+telefono+", '"+correo+"', '"+contraseña+"')
    con = sql_connection()    
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_edit_user(tipo, nombre, apellido, fechaN, sexo, tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo,contraseña, cedulae):
    strsql = "update Usuarios set TipoUsuario = '"+tipo+"', Nombre = '"+nombre+"', Apellido = '"+apellido+"', FechaNacimiento = '"+fechaN+"', Sexo ='"+sexo+"', TipoIdentificacion = '"+tipoDocumento+"', NumeroIdentificacion = '"+cedula+"', Especialidad = '"+especialidad+"', Consultorio = '"+consultorio+"', Direccion = '"+direccion+"', Telefono = "+telefono+", Correo = '"+correo+"', Contraseña = '"+contraseña+"' where NumeroIdentificacion = '"+cedulae+"';"
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    con.close()

def sql_delete_user(cedula):
    strsql = "delete from Usuarios where cedula = '"+cedula+"';" 
    con = sql_connection()
    cursorObj = con.cursor()
    con.commit()
    con.close()

def sql_delete_paciente(cedula):
    strsql = 'DELETE FROM Usuarios WHERE NumeroIdentificacion=' + cedula+';'
    con = sql_connection()
    cursorObj = con.cursor()
    cursorObj.execute(strsql)
    con.commit()
    print("usuario eliminado")

def sql_search_user(cedula):
    strsql = "select * from Usuarios where NumeroIdentificacion = '"+cedula+"';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def get_columns_usuario():
    strsql = "select * from Usuarios"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def get_columns_cita():
    strsql = "select * from CITA"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    names = list(map(lambda x: x[0], cursor.description))
    return names

def getMedicos():
    strsql = "select * from Usuarios where TipoUsuario = 2"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def getCitas():
    strsql = "select * from CITA"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
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

def getPacientes():
    strsql = "select * from Usuarios where TipoUsuario = 1"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_search_user_paciente(cedula):
    strsql = "select * from Usuarios where NumeroIdentificacion = '"+cedula+"' AND TipoUsuario = 1;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_search_citaspacientes(cedula):
    strsql = "select Idcita,Medico,Fecha,Hora,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion= '"+cedula+"' and CITA.Estado='Pendiente';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_search_Historialcitas(cedula):
    strsql = "select Idcita,Medico,Fecha,Hora,Estado from CITA JOIN Usuarios  ON Usuarios.IdUsuario= CITA.Paciente where Usuarios.NumeroIdentificacion= '"+cedula+"' and CITA.Estado NOT IN ('Pendiente');"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def get_columnas_Cita():  
    strsql = "select Idcita,Medico,Fecha,Hora,Estado from CITA"
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

def get_Medicos1():
    strsql = "select Nombre,Apellido from Usuarios where TipoUsuario='2';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_actualizarestadocita(idcita):
    strsql = "update CITA set Estado='Cancelada' where idcita='"+idcita+"' and Estado='Pendiente';"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    con.commit()
    con.close()

def get_columnas_Cita1():  
    strsql = "select Idcita,Paciente,Fecha,Hora,Estado from CITA"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = list(map(lambda x: x[0], cursor.description))
    return response

def sql_citasmedico(cedula):
    strsql = "select Idcita,Paciente,Fecha,Hora,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Medico where Usuarios.NumeroIdentificacion= '"+cedula+"' ORDER BY Fecha desc;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response

def sql_citasmedico_fecha(cedula,Finicial,Ffinal):
    strsql = "select Idcita,Paciente,Fecha,Hora,Estado from CITA JOIN Usuarios ON Usuarios.IdUsuario= CITA.Medico where Usuarios.NumeroIdentificacion= '"+cedula+"' and Fecha BETWEEN '"+Finicial+"' and '"+Ffinal+"' ORDER BY Fecha desc;"
    con =sql_connection()
    cursor = con.cursor()
    cursor.execute(strsql)
    response = cursor.fetchall()
    return response
   


