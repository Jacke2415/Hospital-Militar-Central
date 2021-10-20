from re import template
import db 
from jinja2 import Environment, FileSystemLoader 

env = Environment(loader = FileSystemLoader("templates"))
template = env.get_template('principalPaciente.html')

cedula = '67028405'
encontrado = db.sql_search_user(cedula)

user = {
        'name' : encontrado[0][2] + ' ' + encontrado[0][3],
        'tipoId': encontrado[0][5],
        'numId': encontrado[0][6],
        'sexo': encontrado[0][4],
        'edad': 15,
        'tel': encontrado[0][10],
        'dir': encontrado[0][9]
        }

print(user['sexo'])