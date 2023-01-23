#importaciones
import mysql.connector
import json
import requests
import pprint as pp

#conexion con el servidor
conexion = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database="pokemon"
)

#creación del cursor
cursor = conexion.cursor()


#apartado de funciones
#creación de nueva base de datos

def creardatabase (nombredatabase):
    try:
        cursor.execute(f'CREATE DATABASE IF NOT EXISTS {nombredatabase};')
        resultado = "Se creó correctamente la base de datos."
        return resultado
    except:
        resultado = "Base de datos ya creada."
        return resultado

#eliminación de la base de datos

def eliminardatabase (nombredatabase):
    try:
        cursor.execute(f'DROP DATABASE {nombredatabase};')
        resultado = "Se eliminó correctamente la base de datos."
        return resultado
    except:
        resultado = "Ocurrió un error al intentar eliminar la base de datos. Inténtelo de nuevo."
        return resultado
    
#eliminar tabla ingresando su nombre
def eliminartabla (nombretabla):
    try:
        cursor.execute(f'DROP TABLE {nombretabla};')
        resultado = "Se eliminó correctamente la tabla."
        return resultado
    except:
        resultado = "Ocurrió un error al intentar eliminar la tabla. Inténtelo de nuevo."
        return resultado
#crea la tabla principal info, donde se almacenan los datos de entrada
def creartablainfo():
    try:
        cursor.execute(f'CREATE TABLE IF NOT EXISTS informacion' 
        "(id INT NOT NULL AUTO_INCREMENT,"
        "Nombre VARCHAR (32) NOT NULL," 
        "Habilidad VARCHAR (32) NOT NULL,"
        "Limite VARCHAR (3) NOT NULL, "
        "PRIMARY KEY (id));")
        resultado = "Se creó correctamente la tabla."
        return resultado
    except:
        resultado = "Tabla ya creada."
        return resultado 
       
#Guarda en la base de datos los elementos de entrada para iniciar la busqueda en la pokeapi.
#En caso de que la informacion ya exista en la de datos solo la imprimira sin realizar la busqueda en la pokeapi.
def rellenartabla(name,ability,limit):
    try:
        cursor.execute("SELECT Nombre FROM informacion")
        dispositivos= cursor.fetchall()
        contador=0
        for fila in dispositivos:
            for columna in fila:
                if columna == name: 
                    cursor.execute("SELECT * FROM informacion")
                    row = cursor.fetchall()
                    print ("Tomando variables para iniciar busqueda:")
                    print ((row[contador]))
                    try:
                        cursor.execute("SELECT Informacion FROM ditto")
                    except:
                        (busqueda(name,ability,limit))    
                    result = cursor.fetchall()
                    print("Informacion buscada con anterioridad,imprimiendo desde la base de datos:")
                    resultado = "Fin de busqueda"   
                    for row in result:
                        print(row)   
                    return resultado 
                else:
                    contador=contador+1         
        sql = "INSERT INTO informacion (Nombre, Habilidad, Limite) VALUES (%s, %s, %s)"
        val = (name,ability,limit)
        cursor.execute(sql, val)
        conexion.commit()
        (busqueda(name,ability,limit))
        resultado = "Se relleno la tabla correctamente."
        return resultado
    except:
        resultado = "Ocurrió un error al intentar rellenar la tabla. Inténtelo de nuevo."
        return resultado 

#Busca en la pokeapi la informacion requerida y crea la tabla para guardar esa informacion.
def busqueda(name,ability,limit): 

    cursor.execute('CREATE TABLE IF NOT EXISTS ditto' 
    "(id INT NOT NULL AUTO_INCREMENT,"
    "Informacion VARCHAR (256), "
    "PRIMARY KEY (id));")

    
    urlpkmn = f'https://pokeapi.co/api/v2/pokemon/{name}/'
    params = {'limit': limit}
    print("Comenzando busqueda de informacion desde la pokeapi:")
    for offset in range(0, 1):
        params['offset'] = offset  # limite
        response = requests.get(urlpkmn, params=params)

        if response.status_code != 200: 
            print(response.text)
        else:
            data = response.json()
            #pp.pprint(data)
            for item in data['abilities']:
                efecto = item['ability']
                json_object = json.dumps(efecto, indent = 4)
                datos_diccionario = json.loads(json_object)
                names = datos_diccionario["name"]
                namehaAbility = "Ability: "+names
                sql = "INSERT INTO ditto (Informacion) VALUES (%s)"
                val = (namehaAbility)
                cursor.execute(sql, (val,))
                conexion.commit()
                print(namehaAbility)
    
    urlability = f'https://pokeapi.co/api/v2/ability/{ability}/'
    params = {'limit': limit}

    for offset in range(0, 1):
        params['offset'] = offset  # limite
        response = requests.get(urlability, params=params)

        if response.status_code != 200: 
            print(response.text)
        else:
            data = response.json()
            
            for item in data['effect_entries']:
                efecto = item['short_effect']
                effect = "Effect: "+efecto
                sql = "INSERT INTO ditto (Informacion) VALUES (%s)"
                val = (effect)
                cursor.execute(sql, (val,))
                conexion.commit()
                print(effect)

def obtenerentrada():
    cursor.execute("SELECT Nombre FROM informacion")
    dispositivos= cursor.fetchall()
    contador = 0
    for fila in dispositivos:
            if contador >0:
                break
            else:
                contador = contador+1
                for columna in fila:
                    name = columna
    cursor.execute("SELECT Habilidad FROM informacion")
    dispositivos= cursor.fetchall()
    contador = 0
    for fila in dispositivos:
            if contador >0:
                break
            else:
                contador = contador+1
                for columna in fila:
                    ability = columna                    
    cursor.execute("SELECT Limite FROM informacion")
    dispositivos= cursor.fetchall()
    contador = 0
    for fila in dispositivos:
            if contador >0:
                break
            else:
                contador = contador+1
                for columna in fila:
                    limit = columna
    rellenartabla(name,ability,limit)



nombredatabase = "pokemon"
nombretabla = "Información"

#pasos:
#1.ejecutar estas 2 partes primero si no hay base de datos ni tablas
print(creardatabase(nombredatabase))
print(creartablainfo())

#2.ingresar estos datos de entrada en formato json en postman usando el comando post
#la url usada fue http://localhost:3000/api/informacion/
#en caso de ser una url distinta solo se debe tener en cuenta la parte /api/informacion/ para ingresar el json
'''
{
"name": "ditto",
"ability": "imposter",
"limit": 20
}
'''
#3.ejecutar la siguiente funcion, permite realizar la busqueda con la informacion de entrada
obtenerentrada()



#funciones para eliminar database y tablas, no son necesarias para el funcionamiento

#print(eliminartabla(nombretabla))
#print(eliminardatabase(nombredatabase))