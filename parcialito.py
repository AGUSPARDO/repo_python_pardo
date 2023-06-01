
import json
import csv
#ABRIR ARCHIVO JSON:
def leer_archivo(nombre_archivo:str)->list:
    '''
    Esta función lee un archivo JSON y devuelve una lista de jugadores.
    Parámetros:
    nombre_archivo: Una cadena que representa el nombre del archivo JSON a leer
    Retorna: 
    Una lista de jugadores en formato JSON.
    '''
    with open(nombre_archivo, "r") as archivo:
        contenido = archivo.read()
        lista_jugadores = json.loads(contenido)
    return lista_jugadores

data_dream = leer_archivo("dt.json")
data_dream_lista = data_dream["jugadores"]

# 1.MUESTRA LA LISTA DE TODOS LOS JUGADORES POR NOMBRE Y POSICION
def print_jug(data_dream_lista:list)->None:
    '''
    Esta función muestra la lista de todos los jugadores del Dream Team, incluyendo su nombre y posición.
    Parámetros:
    data_dream_lista: Una lista de jugadores en formato JSON.
    Retorna:
    No tiene valor de retorno.
    '''
    for indice in range(len(data_dream_lista)):
        jugador = data_dream_lista[indice]
        nombre = jugador["nombre"]
        posicion = jugador["posicion"]
        print("{0} - {1} - {2}".format(indice, nombre, posicion))

#2.SELECCIONAR UN JUGADOR POR SU ÍNDICE Y MOSTRAR SUS ESTADÍSTICAS
def get_player_data(data_dream_lista:list)->dict:
    '''
    Recibe la LISTA de jugadores
    Se requiere al usuario que ingrese un índice 
    Devuelve el diccionario del jugador seleccionado y muestra el nombre y las estadísticas del jugador

    :param data_dream_lista: La lista de jugadores con sus estadísticas
    :type data_dream_lista: list
    :return: El diccionario del jugador seleccionado
    :rtype: dict
    '''
    opcion = int(input("Ingrese el índice del jugador deseado para mostrar las estadísticas: "))
    
    if opcion < 0 or opcion >= len(data_dream_lista):
        print("Índice inválido")
        return None
    
    jugador_seleccionado = data_dream_lista[opcion]
    nombre = jugador_seleccionado["nombre"]
    estadisticas = jugador_seleccionado["estadisticas"]
    
    print("El jugador seleccionado es: {0}".format(nombre))
    print("Estadísticas:")
    for estadistica, valor in estadisticas.items():
        print("{0}: {1}".format(estadistica, valor))
    
    return jugador_seleccionado
#FUNCION GENERAR TEXTO PARA PODER PASAR DICT A STR
def generar_cadena(jugador_seleccionado: dict) -> str:
    '''
    Esta función genera una cadena de texto que representa los datos del jugador seleccionado en formato CSV.

    Parámetros:

    jugador_seleccionado: Un diccionario que contiene los datos del jugador seleccionado.
    Retorna:

    Una cadena de texto en formato CSV con los datos del jugador.
    '''
    selected_player = jugador_seleccionado
    jugador_stats = selected_player["estadisticas"]
    j_posicion = "{0}, {1}".format(selected_player["nombre"], \
                                        selected_player["posicion"])
    
    lista_key = ["nombre", "posicion"]
    lista_valores = []

    for key, value in jugador_stats.items():
        lista_key.append(key)
        lista_valores.append(str(value))

    keystr = ",".join(lista_key)
    valuestr = ",".join(lista_valores)

    datos_str = "{0}\n{1},{2}".format(keystr, j_posicion, valuestr)
    return datos_str


# Función para exportar los datos del jugador seleccionado a un archivo CSV
def exportar_a_csv(jugador_seleccionado:dict)->None:
    '''Esta función exporta los datos del jugador seleccionado a un archivo CSV.
    Parámetros:
    jugador_seleccionado: Un diccionario que contiene los datos del jugador seleccionado
    Retorna:
    No tiene valor de retorno.
    '''
    if jugador_seleccionado is None:
        return

    nombre = jugador_seleccionado.get("nombre", "jugador")
    nombre_archivo = nombre.lower().replace(" ", "_") + "_estadisticas.csv"

    # Generar la cadena de datos del jugador seleccionado
    datos_jugador = generar_cadena(jugador_seleccionado)

    with open(nombre_archivo, "w", newline="") as archivo_csv:
        archivo_csv.write(datos_jugador)

    print("Los datos se han exportado correctamente a {0}".format(nombre_archivo))
jugador_seleccionado = None

#BUSCAR JUGADOR POR SU NOMBRE Y MOSTRAR SUS LOGROS:
def buscar_jugador_por_nombre(data_dream_lista: list) -> None:
    '''
    Esta función busca un jugador por su nombre en la lista y muestra sus logros.

    Parámetros:

    data_dream_lista: Una lista de jugadores en formato JSON.
    Retorna:

    No tiene valor de retorno.
    '''
    nombre = input("Ingrese el nombre del jugador a buscar: ")

    jugadores_encontrados = []
    for jugador in data_dream_lista:
        if jugador["nombre"].lower() == nombre.lower():
            jugadores_encontrados.append(jugador)

    if len(jugadores_encontrados) == 0:
        print("No se encontró ningún jugador con ese nombre.")
        return

    for jugador in jugadores_encontrados:
        nombre_jugador = jugador["nombre"]
        logros_jugador = jugador.get("logros", [])
        
        print("Jugador: {0}".format(nombre_jugador))
        print("Logros:")
        for logro in logros_jugador:
            print("- {0}".format(logro))
#CALCULAR PROMEDIO
def calcular_promedio(lista: list, clave: str) -> float:
    '''
    Esta función calcula el promedio de una estadística específica de todos los jugadores en la lista.

    Parámetros:

    lista: Una lista de jugadores en formato JSON.
    clave: Una cadena que representa la clave de la estadística a promediar.
    Retorna:

    El promedio de la estadística especificada, o None si no hay suficientes datos.
    '''
    total = 0
    count = 0

    for jugador in lista:
        if clave in jugador["estadisticas"]:
            total += float(jugador["estadisticas"][clave])
            count += 1

    if count > 0:
        promedio = total / count
        return promedio
    else:
        return None
#QUICKSORT ORDENAMIENTO:
def quick_sort(lista: list, clave: str, flag_orden: bool) -> list:
    '''
    Esta función realiza el algoritmo de ordenamiento QuickSort en la lista de jugadores según una clave de estadística.
    Parámetros:
    lista: Una lista de jugadores en formato JSON.
    clave: Una cadena que representa la clave de la estadística para ordenar.
    flag_orden: Un valor booleano que indica si el ordenamiento es ascendente (True) o descendente (False).
    Retorna:
    Una lista de jugadores ordenada según la clave de estadística especificada y el orden indicado.
    '''
    jugadores_izq = []
    jugadores_der = []
    if len(lista) <= 1:
        return lista
    else:
        pivot = lista[0]['estadisticas'][clave]
        for elemento in lista[1:]:
            if elemento['estadisticas'][clave] > pivot:
                jugadores_der.append(elemento)
            else:
                jugadores_izq.append(elemento)
        jugadores_izq = quick_sort(jugadores_izq, clave, flag_orden)
        jugadores_der = quick_sort(jugadores_der, clave, flag_orden)
        if flag_orden:
            return jugadores_der + [lista[0]] + jugadores_izq
        else:
            return jugadores_izq + [lista[0]] + jugadores_der

#MIEMBRO DEL SALON DE LA FAMA
def es_miembro_salon_fama(data_dream_lista:list) -> bool:
    '''
    Verifica si un jugador es miembro del Salón de la Fama del Baloncesto.

    Parámetros:
        data_dream_lista: Lista de jugadores con sus estadísticas.

    Retorna:
        bool: True si el jugador es miembro del Salón de la Fama del Baloncesto, False en caso contrario.
    '''
    nombre_jugador = input("Ingrese el nombre del jugador: ")
    nombre_jugador = nombre_jugador.title()

    for jugador in data_dream_lista:
        if nombre_jugador == jugador["nombre"]:
            logros = jugador.get("logros", [])
            if "Miembro del Salon de la Fama del Baloncesto" in logros:
                return True

    return False

#CALCULOS 7,8, 9, 13, 14 MAXS y MINS

def calcular_jugadores_valor(jugadores, sub_clave, calcular_maximo=True):
    '''
    Calcula y muestra el jugador con la mayor o menor cantidad de una estadística específica.

    Parámetros:
        jugadores (list): Lista de jugadores.
        sub_clave (str): Clave que se encuentra dentro de los diccionarios de los jugadores y a su vez dentro de la clave "estadisticas".
        calcular_maximo (bool): Indica si se desea calcular el máximo valor. Por defecto es True.

    Retorna:
        str: Una cadena que indica el nombre del jugador con la mayor o menor cantidad según el dato de la "sub_clave" ingresada.
    '''
    if jugadores:
        primer_jugador = jugadores[0]
        valor_extremo = int(primer_jugador["estadisticas"][sub_clave])
        jugadores_extremo = [primer_jugador]

        for jugador in jugadores[1:]:
            valor = int(jugador["estadisticas"][sub_clave])
            if (calcular_maximo and valor > valor_extremo) or (not calcular_maximo and valor < valor_extremo):
                valor_extremo = valor
                jugadores_extremo = [jugador]
            elif valor == valor_extremo:
                jugadores_extremo.append(jugador)

        if jugadores_extremo:
            resultado = "Jugador(es) con la mayor cantidad de {0}:\n".format(sub_clave) if calcular_maximo else "Jugador(es) con la menor cantidad de {0}:\n".format(sub_clave)
            for jugador in jugadores_extremo:
                resultado += "- {0}\n".format(jugador["nombre"])
            return resultado
    
    if calcular_maximo:
        return "No se encontraron jugadores con estadísticas de {0}.".format(sub_clave)
    else:
        return "No se encontraron jugadores con estadísticas de {0}.".format(sub_clave)
# 10, 11, 12, 15 
def mostrar_jugadores_valor(jugadores, sub_clave):
    '''
    Calcula y muestra los nombres de los jugadores con una estadística específica que supera un valor ingresado por el usuario.

    Parámetros:
        jugadores (list): Lista de jugadores.
        sub_clave (str): Clave que se encuentra dentro de los diccionarios de los jugadores y a su vez dentro de la clave "estadisticas".

    Retorna:
        list: Una lista de nombres de los jugadores que superan el valor ingresado en la estadística especificada.
    '''
    if jugadores:
        valor = float(input("Ingrese un valor: "))
        jugadores_superiores = []

        for jugador in jugadores:
            if sub_clave in jugador["estadisticas"]:
                if jugador["estadisticas"][sub_clave] > valor:
                    jugadores_superiores.append(jugador["nombre"])

        if jugadores_superiores:
            return jugadores_superiores

    return []
def calcular_promedio_excluyendo_menor(lista: list, clave: str) -> float:
    '''
    Calcula y muestra el promedio de una estadística específica de los jugadores del equipo,
    excluyendo al jugador con la menor cantidad de dicha estadística.

    Parámetros:
        lista (list): Lista de jugadores en formato JSON.
        clave (str): Clave que representa la estadística a promediar.

    Retorna:
        float: El promedio de la estadística especificada, excluyendo al jugador con la menor cantidad.
    '''
    lista_ordenada = quick_sort(lista, clave, flag_orden= True)

    lista_vacia = []
    
    for jugador in range (1,len(lista_ordenada)):
        lista_vacia.append(lista_ordenada[jugador])
        
    print(lista_vacia)
    #promedio = calcular_promedio(lista_ordenada, clave)

    return None
while True:
        print("Seleccione una opción:")
        print("1. Mostrar la lista de todos los jugadores del Dream Team")
        print("2. Seleccionar un jugador por su índice y mostrar sus estadísticas")
        print("3. Guardar las estadísticas de jugador en CSV")
        print("4. Buscar un jugador por nombre y mostrar sus logros")
        print("5. Calcula y muestra el promedio de puntos por partido del Dream Team, ordenado por nombre de manera ascendente")
        print("6. Ingrese el nombre de un jugador para saber si es miembro del Salón de la Fama del Baloncesto")
        print("7. Calcula y muestra el jugador con la mayor cantidad de rebotes totales")
        print("8. Calcula y muestra el jugador con el mayor porcentaje de tiros de campo")
        print("9. Calcula y muestra el jugador con la mayor cantidad de asistencias totales")
        print("10. Ingrese un valor para mostrar los jugadores que han promediado más puntos por partido que ese valor")
        print("11. Ingrese un valor para mostrar los jugadores que han promediado más rebotes por partido que ese valor")
        print("12. Ingrese un valor para mostrar los jugadores que han promediado más asistencias por partido que ese valor")
        print("13. Calcula y muestra el jugador con la mayor cantidad de robos totales")
        print("14. Calcula y muestra el jugador con la mayor cantidad de bloqueos totales")
        print("15. Ingrese un valor para mostrar los jugadores que hayan tenido un porcentaje de tiros libres superior a ese valor")
        print("16. Calcula y muestra el promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad de puntos por partido")
        print("17. Calcula y muestra el jugador con la mayor cantidad de logros obtenidos")
        print("18. Ingrese un valor para mostrar los jugadores que hayan tenido un porcentaje de tiros triples superior a ese valor")
        print("19. Calcula y muestra el jugador con la mayor cantidad de temporadas jugadas")
        print("20. Ingrese un valor para mostrar los jugadores, ordenados por posición en la cancha, que hayan tenido un porcentaje de tiros de campo superior a ese valor")
        print("21. Calcula de cada jugador cuál es su posición en los siguientes rankings: - Puntos - Rebotes - Asistencias - Robos y los exporta a CSV")
        print("22. Salir")

        option = input()
    
        match option:
            case "1":
                print_jug(data_dream_lista) 
            case "2":
                jugador_seleccionado = get_player_data(data_dream_lista)
            case "3":
                if jugador_seleccionado is not None:
                    exportar_a_csv(jugador_seleccionado)
                else:
                    print("Debe seleccionar un jugador antes de exportar las estadísticas.")
            case "4":
                buscar_jugador_por_nombre(data_dream_lista)
            case "5":
                promedio_puntos_por_partido = calcular_promedio(data_dream_lista, "promedio_puntos_por_partido")
                jugadores_ordenados = quick_sort(data_dream_lista, "promedio_puntos_por_partido", False)
                if promedio_puntos_por_partido is not None:
                    print("El promedio de puntos por partido del Dream Team es: {0}".format(promedio_puntos_por_partido))
                else:
                    print("No hay suficientes datos para calcular el promedio de puntos por partido.")
                print("Jugadores ordenados:")
                for jugador in jugadores_ordenados:
                    nombre = jugador["nombre"]
                    promedio_puntos = jugador["estadisticas"]["promedio_puntos_por_partido"]
                    print("Nombre: {0} - Promedio de puntos: {1}".format(nombre, promedio_puntos))
            case "6":
                resultado = es_miembro_salon_fama(data_dream_lista)
                if resultado:
                    print("El jugador es miembro del Salón de la Fama del Baloncesto.")
            case "7":
                print(calcular_jugadores_valor(data_dream_lista, "rebotes_totales", calcular_maximo=True))
            case "8":
                print(calcular_jugadores_valor(data_dream_lista, "porcentaje_tiros_de_campo", calcular_maximo=True))
            case "9":
                print(calcular_jugadores_valor(data_dream_lista, "asistencias_totales", calcular_maximo=True))
            case "10":
                jugadores_superiores = mostrar_jugadores_valor(data_dream_lista, "promedio_puntos_por_partido")
                print(jugadores_superiores)
            case "11":
                print(mostrar_jugadores_valor(data_dream_lista, "promedio_rebotes_por_partido"))
            case "12":
                print(mostrar_jugadores_valor(data_dream_lista, "promedio_asistencias_por_partido"))
            case "13":
                resultado = calcular_jugadores_valor(data_dream_lista, "robos_totales", calcular_maximo=True)
                print(resultado)
            case "14":
                resultado = calcular_jugadores_valor(data_dream_lista, "bloqueos_totales", calcular_maximo=True)
                print(resultado)
            case "15":
                print(mostrar_jugadores_valor(data_dream_lista, "porcentaje_tiros_libres"))
                pass
            case "16":
                promedio_excluyendo_menor = calcular_promedio_excluyendo_menor(data_dream_lista, "promedio_puntos_por_partido")
                print("Promedio de puntos por partido del equipo excluyendo al jugador con la menor cantidad:")
                print(promedio_excluyendo_menor)
            case "17":
                pass
            case "18":
                pass
            case "19":
                pass
            case "20":
                pass
            case "21":
                pass
            case "22":
                print("Saliendo del programa...")
                pass
            case _:
                print("Opción no válida. Intente de nuevo.")





