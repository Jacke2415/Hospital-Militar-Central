import db
import names
import  random
import string

def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))

tipo_usuario = []
primer_nombre = []
segundo_nombre = []
sexo = []
tipo_id = []
numero_id = []
especialidad = []
consultorio = []
direction = []
telefono = []
correo = []
contrasena = []

num_input = 0
for i in range(num_input):
    tipo_usuario.append(random.randint(1,3))
    #----------------------------
    primer_nombre.append(names.get_first_name(gender='female'))
    #----------------------------
    segundo_nombre.append(names.get_last_name())
    #----------------------------
    sex_choice = random.randint(0,1)
    #----------------------------
    if sex_choice == 1:
        sexo.append("Femenino")
    else:
        sexo.append("Masculino")
    #----------------------------
    tipo_id_choice = random.randint(0,3)
    if tipo_id_choice == 0:
        tipo_id.append("RC")
    elif tipo_id_choice == 1:
        tipo_id.append("TI")
    elif tipo_id_choice == 1:
        tipo_id.append("CC")
    elif tipo_id_choice == 1:
        tipo_id.append("Pasaporte")
    #----------------------------
    numero_id.append(random.randint(10000000,20000000))
    #----------------------------
    if tipo_usuario[i] == 2:
        especialidad_choice = random.randint(0,4)
        if especialidad_choice == 0:
            especialidad.append("General")
        elif especialidad_choice == 1:
            especialidad.append("Pediatria")
        elif especialidad_choice == 2:
            especialidad.append("Dermatologia")
        elif especialidad_choice == 3:
            especialidad.append("Ginecologia")
        elif especialidad_choice == 4:
            especialidad.append("Cardiologia")
    else:
        especialidad.append("NoAplica")
    #----------------------------
    if tipo_usuario[i] == 2:
        consultorio_generator = random.randrange(100,400,5)
        consultorio.append(consultorio_generator)
    else:
        consultorio.append("NoAplica")
    #----------------------------
    direction.append("Direccion de Prueba")
    #----------------------------
    telefono.append(random.randint(500000,599999))
    #----------------------------
    correo.append(random_char(7)+"@gmail.com")
    #----------------------------
    contrasena.append(random_char(10))


# print(tipo_usuario)
# print(primer_nombre)
# print(segundo_nombre)
# print(sexo)
# print(tipo_id)
# print(numero_id)
# print(especialidad)
# print(consultorio)
# print(direction)
# print(telefono)
# print(correo)
# print(contrasena)

#tipo, nombre, apellido, sexo,tipoDocumento, cedula, especialidad, consultorio, direccion, telefono, correo,contraseña
for i in range(num_input):
    db.sql_insert_user(str(tipo_usuario[i]),primer_nombre[i],segundo_nombre[i],sexo[i],tipo_id[i],str(numero_id[i]),especialidad[i],str(consultorio[i]),direction[i],str(telefono[i]),correo[i],contrasena[i])


db.sql_delete_paciente('17648240')