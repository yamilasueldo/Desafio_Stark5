import json
from data_stark import lista_personajes

def leer_archivo(nombre_archivo:str):
    '''
    Lee el contenido de un archivo.
    Parámetros:
        nombre_archivo (str): El nombre del archivo a leer.

    Retorna:
        str: El contenido del archivo leído.
        False: Si el archivo no fue encontrado.
    '''
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            retorno = archivo.read()
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        retorno = False
    return retorno

#1.2
def guardar_archivo(nombre_archivo:str,nuevo_contenido:str):
    '''
    Guarda contenido en un archivo.
    Parámetros:
        nombre_archivo (str): El nombre del archivo a guardar.
        nuevo_contenido (str): El nuevo contenido a escribir en el archivo.
    Retorna:
        bool: True si la operación fue exitosa, False si hubo un error.
    '''
    try:
        with open(nombre_archivo, 'w+', encoding='utf-8') as archivo:
            archivo.write(nuevo_contenido)
            mensaje = f"Se creó el archivo: {nombre_archivo}"
            retorno = True
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        mensaje =f"Eror al crear el archivo: {nombre_archivo}"
        retorno = False
    print(mensaje)
    return retorno

#1.3
def generar_csv(nombre_archivo:str,lista_supeheroes:list):
    '''
    Genera un archivo CSV a partir de una lista de superhéroes.
    Parámetros:
        nombre_archivo (str): El nombre del archivo CSV a generar.
        lista_superheroes (list): La lista de superhéroes a convertir en CSV.
    Retorna:
        bool: True si la operación fue exitosa, False si hubo un error.
    '''
    retorno = False
    if len(lista_supeheroes) > 0:
        cabeceras = lista_supeheroes[0].keys()
        csv_string = ",".join(cabeceras) + '\n'
        for heroe in lista_supeheroes:
            csv_string += ",".join(str(heroe[clave]) for clave in cabeceras) + "\n"
        retorno = guardar_archivo(nombre_archivo,csv_string)
    return retorno

#1.4
def leer_csv(nombre_archivo:str):
    '''
    Lee un archivo CSV y retorna una lista de superhéroes.
    Parámetros:
        nombre_archivo (str): El nombre del archivo CSV a leer.
    Retorna:
        list: La lista de superhéroes leída desde el archivo.
        False: Si el archivo no fue encontrado.
    '''
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()
        claves = lineas[0].strip().split(',')
        lista_superheroes = []
        for linea in lineas[1:]:
            datos_heroe = linea.strip().split(',')
            heroe = {}
            for i in range(len(claves)):
                heroe[claves[i]] = datos_heroe[i]
            lista_superheroes.append(heroe)
        return lista_superheroes
    
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        retorno = False

def sanitizar_entero(numero_str)->int:
    '''
    Analiza el string recibido y determina si es un número
    entero positivo.
    Parametros: numero_str:str -> un string que representa un posible número entero
    Retorno: un entero 
            -1 -> si numero_str contienen caracteres no númericos
            -2 -> si numero_str es un numero negativo
            -3 -> si ocurre algun error al intertar convertir numero_str en entero
            el string recibido casteado a entero -> si el string es un numero entero positivo 
    '''
    numero_str = numero_str.strip()
    if(not numero_str.isdigit()):
        retorno = -1
    else:
        if(int(numero_str) < 0):
            retorno = -2
        else:
            try:
                numero = int(numero_str) 
                retorno = numero 
            except ValueError: 
                retorno = -3
    return retorno

def sanitizar_flotante(numero_str:str)->int:
    '''
    Analiza el string recibido y determina si es un número
    flotante positivo.
    Parametros: numero_str:str -> un string que representa un posible número decimal
    Retorno: un entero negativo
            -1 -> si numero_str contienen caracteres no númericos
            -2 -> si numero_str es un numero negativo
            -3 -> si ocurre algun error al intertar convertir numero_str en flotante
            el string recibido casteado a float -> si el string es un numero flotante positivo 
    '''
    numero_str = numero_str.strip()
    if(not (numero_str.replace('.','')).isdigit()):
        retorno = -1
    else:
        if(float(numero_str) < 0):
            retorno = -2
        else:
            try:
                numero = float(numero_str) 
                retorno = numero 
            except ValueError: 
                retorno = -3
    return retorno

def sanitizar_string(valor_str, valor_por_defecto='-'):
    '''
    Analiza el string recibido y determina si es solo texto, sin numeros
    Parametros: numero_str:str -> un string que representa el texto a validar
                valor_por_defecto:str -> un string que representa un valor por defecto, inicializado con '-'
    Retorno: un string:
                'N/A' -> si el string contiene numeros
                valor_str convertido a minusculas -> si se verifica que es solo texto
                valor_por_defecto convertido a minusculas -> si el texto a validar es vacio               
    '''
    valor_str = valor_str.strip()
    valor_por_defecto = valor_por_defecto.strip()
    valor_str = valor_str.replace('/', ' ')
    if valor_str.isalpha():
        resultado =  valor_str.lower()
    else:
        if valor_str == '':
            resultado = valor_por_defecto.lower()
        else:
            resultado = 'N/A'
    return resultado

def sanitizar_dato(heroe:dict,clave:str,tipo_dato:str)->bool:
    '''
    Sanitiza el valor del diccionario heroe correspondiente a la clave y al tipo de dato recibido.
    Parámetros:
        heroe (dict): El diccionario del héroe que contiene los datos a sanitizar.
        clave (str): La clave de los datos a sanitizar.
        tipo_dato (str): El tipo de dato a aplicar ('entero' para números enteros, 'flotante' para números con decimales, 'string' para texto).

    Retorna:
        bool: True si los datos se sanitizaron con éxito, False en caso contrario.
    '''
    se_sanitizo_dato = False
    clave = clave.lower()
    tipo_dato = tipo_dato.lower()
    if clave in heroe:
        if tipo_dato == 'entero':
            heroe[clave] = sanitizar_entero(heroe[clave])
            se_sanitizo_dato = True
        elif tipo_dato == 'flotante':
            heroe[clave] = sanitizar_flotante(heroe[clave])
            se_sanitizo_dato = True
        elif tipo_dato == 'string':
            heroe[clave] = sanitizar_string(heroe[clave])
            se_sanitizo_dato = True
        else:
            print("Tipo de dato no reconocido")
    else:
        print("La clave especificada no existe en el héroe.")
    return se_sanitizo_dato

def stark_normalizar_datos(lista_heroes:list):
    '''
    Normaliza los datos en una lista de héroes según ciertos criterios.
    Parámetros:
        lista_heroes (list): La lista de héroes cuyos datos se normalizarán.

    Esta función normaliza los datos de altura, peso, color de ojos, color de pelo, fuerza e inteligencia en la lista de héroes.
    '''
    if len(lista_heroes) > 0:
        for heroe in lista_heroes:
            sanitizar_dato(heroe,'altura','flotante')
            sanitizar_dato(heroe,'peso','flotante')
            sanitizar_dato(heroe,'color_ojos','string')
            sanitizar_dato(heroe,'color_pelo','string')
            sanitizar_dato(heroe,'fuerza','entero')
            sanitizar_dato(heroe,'inteligencia','string')

#1.5
def generar_json(nombre_archivo:str,lista_superheroes:list,nombre_lista:str)->None:
    '''
    Genera un archivo JSON a partir de una lista de superhéroes.
    Parámetros:
        nombre_archivo (str): El nombre del archivo JSON a generar.
        lista_superheroes (list): La lista de superhéroes a convertir en JSON.
        nombre_lista (str): El nombre de la clave que contendrá la lista de superhéroes en el archivo JSON.
    '''
    if len(lista_personajes) > 0:
        datos_json = {nombre_lista : lista_superheroes}
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            json.dump(datos_json, archivo, indent=4)
        print(f"Se ha generado el archivo JSON: {nombre_archivo}")
    else:
        print("La lista de superhéroes está vacía. No se generará el archivo JSON.")

#1.6
def leer_json(nombre_archivo:str, nombre_lista:str):
    '''
    Lee un archivo JSON y retorna una lista de superhéroes.
    Parámetros:
        nombre_archivo (str): El nombre del archivo JSON a leer.
        nombre_lista (str): El nombre de la clave que contiene la lista de superhéroes en el archivo JSON.
    Retorna:
        list: La lista de superhéroes leída desde el archivo.
        False: Si el archivo no fue encontrado o la lista especificada no se encuentra en el archivo JSON.
    '''
    try:
        with open(nombre_archivo, 'r', encoding='utf-8') as archivo:
            datos_json = json.load(archivo)
            if nombre_lista in datos_json:
                retorno = datos_json[nombre_lista]
            else:
                print(f"Error: La lista '{nombre_lista}' no se encuentra en el archivo JSON.")
                retorno = False
    except FileNotFoundError:
        print(f"Error: El archivo '{nombre_archivo}' no fue encontrado.")
        retorno = False
    return retorno

#SEGUNDA PARTE

#2.1
def ordenar_ascendente(lista_personajes:list,clave:str)->None:
    '''
    Ordena una lista de personajes de manera ascendente según la clave especificada.
    Parámetros:
        lista_personajes (list): La lista de personajes a ordenar.
        clave (str): La clave por la cual se ordenará la lista.
    '''
    for i in range(len(lista_personajes)-1):
        for j in range(i+1,len(lista_personajes)):
            if lista_personajes[i][clave] > lista_personajes[j][clave]:
                aux = lista_personajes[i]
                lista_personajes[i] = lista_personajes[j]
                lista_personajes[j]= aux

def ordenar_descendente(lista_personajes:list,clave:str)->None:
    '''
    Ordena una lista de personajes de manera descendente según la clave especificada.
    Parámetros:
        lista_personajes (list): La lista de personajes a ordenar.
        clave (str): La clave por la cual se ordenará la lista.
    '''
    for i in range(len(lista_personajes)-1):
        for j in range(i+1,len(lista_personajes)):
            if lista_personajes[i][clave] < lista_personajes[j][clave]:
                aux = lista_personajes[i]
                lista_personajes[i] = lista_personajes[j]
                lista_personajes[j]= aux  

def ordenar_asc_desc(lista_personajes:list,clave:str)->None:
    '''
    Ordena una lista de personajes de manera ascendente o descendente según la elección del usuario.
    Parámetros:
        lista_personajes (list): La lista de personajes a ordenar.
        clave (str): La clave por la cual se ordenará la lista.
    '''
    orden = input("¿De que manera desea ordenar? ( asc - desc): ").lower()
    while orden not in ['asc','desc']:
        orden = input("Error. ¿De que manera desea ordenar? ( asc - desc): ").lower()
    if orden == 'asc':
        ordenar_ascendente(lista_personajes,clave)
    else:
        ordenar_descendente(lista_personajes,clave)

def pedir_ingreso(opciones_validas:list):
    '''
    Pide al usuario que elija una opción de una lista de opciones válidas.
    Parámetros: opciones_validas (list): Una lista de opciones válidas.
    Retorna: un string -> La opción elegida por el usuario.
    '''
    ingreso = input("Elija una opcion: ")
    while ingreso not in opciones_validas:
        ingreso = input("Error. Elija una opcion valida: ")
    return ingreso

def mostrar_menu(menu:list)->None:
    '''
    Muestra un menú en la consola.
    Parámetros:  menu(list) Una lista de opciones que se mostrarán en el menú.
    '''
    for opcion in menu:
        print(opcion)

def listar_personajes(lista_personajes,clave):
    for personaje in lista_personajes:
        print(f"Nombre: {personaje['nombre']} - {clave}: {personaje[clave]}")

#3
def menu_principal(lista_personajes:list):
    '''
    Menú principal que permite al usuario interactuar con una lista de personajes.
    Esta función muestra un menú interactivo con varias opciones y permite al usuario realizar diferentes acciones en la lista de personajes.
    Parámetros:
        lista_personajes(list): Una lista que contiene información de personajes.
    '''
    seguir = True
    datos_normalizados = False
    mensaje_error = 'ERROR. Primero se deben normalizar los datos.'
    menu = ['1) Normalizar datos','2) Generar CSV','3) Listar heroes del archivo csv por altura ASC','4) Generar JSON','5) Listar heroes del json ordenados por peso DESC','6) Ordenar lista por fuerza.','7) Salir']
    while seguir:
        mostrar_menu(menu)
        opcion = pedir_ingreso(['1','2','3','4','5','6','7'])
        if(not datos_normalizados and opcion != '1' and opcion != '7'):
            print(mensaje_error)
        else:  
            match opcion:
                case '1':
                    if datos_normalizados:
                        print("Hubo un error al normalizar los datos. Verifique que la lista no esté vacía o que los datos ya no se hayan normalizado anteriormente") 
                    else:
                        stark_normalizar_datos(lista_personajes)
                        datos_normalizados= True
                        print('Datos normalizados.')
                    pass
                case '2':
                    nuevo_csv = generar_csv('heroes.csv',lista_personajes)
                    pass
                case '3':
                    lista_heroes_csv = leer_csv('heroes.csv')
                    if lista_heroes_csv:
                        stark_normalizar_datos(lista_heroes_csv)
                        ordenar_ascendente(lista_heroes_csv,'altura')
                        listar_personajes(lista_heroes_csv,'altura')
                    else:
                        print("El archivo CSV no existe.")
                    pass
                case '4':
                    nuevo_json = generar_json('heroes.json',lista_personajes,'heroes')
                    pass
                case '5':
                    lista_heroes_json = leer_json('heroes.json','heroes')
                    if lista_heroes_json:
                        ordenar_descendente(lista_heroes_json, 'peso')
                        listar_personajes(lista_heroes_json, 'peso')
                    else:
                        print("El archivo JSON no existe.")
                    pass
                case '6':
                    ordenar_asc_desc(lista_personajes,'fuerza')
                    listar_personajes(lista_personajes,'fuerza')

                    pass
                case '7':
                    seguir = False

menu_principal(lista_personajes)