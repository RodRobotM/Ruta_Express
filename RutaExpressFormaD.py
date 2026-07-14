import unicodedata

# ---------------------------------------------------------------------
# FUNCIONES AUXILIARES Y DE NORMALIZACIÓN
# ---------------------------------------------------------------------

def limpiar_texto(texto):
    """
    Normaliza el texto quitando acentos, espacios extras 
    y convirtiéndolo a minúsculas para comparaciones seguras.
    """
    if not isinstance(texto, str):
        return ""
    texto_normalizado = texto.strip().casefold()
    texto_sin_acentos = unicodedata.normalize("NFD", texto_normalizado)
    return "".join(caracter for caracter in texto_sin_acentos if unicodedata.category(caracter) != "Mn")


def mostrar_menu():
    print("\n========== MENÚ PRINCIPAL ==========")
    print("1. Asientos por ciudad de origen")
    print("2. Búsqueda de recorridos por rango de precio")
    print("3. Actualizar precio de recorrido")
    print("4. Agregar recorrido")
    print("5. Eliminar recorrido")
    print("6. Salir")
    print("=====================================")


def leer_opcion():
    """
    Valida la opción ingresada por el menú utilizando excepciones (IE 2.5.1).
    """
    try:
        opcion = int(input("Ingrese opción: ").strip())
        if 1 <= opcion <= 6:
            return opcion
        print("Debe seleccionar una opción válida")
        return None
    except (ValueError, EOFError):
        print("Debe seleccionar una opción válida")
        return None


# ---------------------------------------------------------------------
# LÓGICA DE NEGOCIO (PASO DE PARAMETROS STRICTO - VARIABLE GLOBAL PROHIBIDA)
# ---------------------------------------------------------------------

def buscar_codigo(codigo, recorridos):
    """
    Retorna True si el código existe en el diccionario (IE 4.1.1).
    La validación del código no distingue mayúsculas y minúsculas.
    """
    if not isinstance(recorridos, dict):
        return False
    return codigo.strip().upper() in recorridos


def asientos_origen(origen, recorridos, venta):
    """
    Acumula y muestra el total de asientos disponibles para un origen dado (Opción 1).
    Evita totalmente el uso de variables globales accediendo solo por parámetros (IE 3.2.2).
    """
    origen_buscado = limpiar_texto(origen)
    total_asientos = 0
    for codigo, datos_recorrido in recorridos.items():
        if limpiar_texto(datos_recorrido[0]) == origen_buscado and codigo in venta:
            total_asientos += venta[codigo][1]
    print(f"El total de asientos disponibles es: {total_asientos}")


def busqueda_precio(p_min, p_max, recorridos, venta):
    """
    Busca y ordena alfabéticamente los recorridos según el rango de precios (Opción 2).
    """
    resultados = []
    for codigo, datos_venta in venta.items():
        precio, asientos = datos_venta
        if p_min <= precio <= p_max and asientos != 0 and codigo in recorridos:
            origen = recorridos[codigo][0]
            destino = recorridos[codigo][1]
            resultados.append(f"{origen}-{destino}--{codigo}")

    if resultados:
        # Ordenar alfabéticamente ignorando tildes y mayúsculas
        resultados.sort(key=limpiar_texto)
        print(f"Los recorridos encontrados son: {resultados}")
    else:
        print("No hay recorridos en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, recorridos, venta):
    """
    Actualiza el precio de un recorrido si existe en el sistema (Opción 3).
    Usa buscar_codigo internamente de forma limpia.
    """
    codigo_normalizado = codigo.strip().upper()
    if not buscar_codigo(codigo_normalizado, recorridos):
        return False
    venta[codigo_normalizado][0] = nuevo_precio
    return True


def agregar_recorrido(codigo, origen, destino, distancia, tipo_bus, servicio, tiene_wifi, precio, asientos, recorridos, venta):
    """
    Registra el nuevo recorrido en los diccionarios de forma estandarizada (Opción 4).
    """
    codigo_normalizado = codigo.strip().upper()
    if buscar_codigo(codigo_normalizado, recorridos):
        return False

    recorridos[codigo_normalizado] = [
        origen.strip(),
        destino.strip(),
        distancia,
        tipo_bus.strip().lower(),
        servicio.strip().lower(),
        tiene_wifi,
    ]
    venta[codigo_normalizado] = [precio, asientos]
    return True


def eliminar_recorrido(codigo, recorridos, venta):
    """
    Elimina un recorrido de ambos diccionarios de forma segura si existe (Opción 5).
    """
    codigo_normalizado = codigo.strip().upper()
    if not buscar_codigo(codigo_normalizado, recorridos):
        return False
    del recorridos[codigo_normalizado]
    del venta[codigo_normalizado]
    return True


def solicitar_rango_precios():
    """
    Pide y valida el rango de precios gestionando excepciones en el programa principal (IE 2.5.1).
    Garantiza que p_min >= 0, p_max >= 0 y p_min <= p_max.
    """
    while True:
        try:
            p_min = int(input("Ingrese precio mínimo: ").strip())
            p_max = int(input("Ingrese precio máximo: ").strip())
        except (ValueError, EOFError):
            print("Debe ingresar valores enteros")
            continue

        if p_min < 0 or p_max < 0 or p_min > p_max:
            continue

        return p_min, p_max


# ---------------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN INDEPENDIENTES (Opción 4 - Una por campo)
# ---------------------------------------------------------------------

def validar_codigo(valor, recorridos):
    """Retorna True si el código no está vacío, no son solo espacios y es único."""
    if not isinstance(valor, str) or valor.strip() == "":
        return False
    return not buscar_codigo(valor, recorridos)


def validar_origen(valor):
    """Retorna True si el origen no está vacío ni contiene solo espacios."""
    return isinstance(valor, str) and valor.strip() != ""


def validar_destino(valor):
    """Retorna True si el destino no está vacío ni contiene solo espacios."""
    return isinstance(valor, str) and valor.strip() != ""


def validar_distancia(valor):
    """Retorna True si la distancia es un entero mayor que cero."""
    return isinstance(valor, int) and valor > 0


def validar_tipo_bus(valor):
    """Retorna True si el tipo de bus es exactamente 'normal', 'semi-cama' o 'cama'."""
    if not isinstance(valor, str):
        return False
    return limpiar_texto(valor) in {"normal", "semi-cama", "cama"}


def validar_servicio(valor):
    """Retorna True si el servicio es exactamente 'dia' o 'noche'."""
    if not isinstance(valor, str):
        return False
    return limpiar_texto(valor) in {"dia", "noche"}


def validar_wifi(valor):
    """Retorna True si la opción de wifi ingresada es 's' o 'n'."""
    if not isinstance(valor, str):
        return False
    return limpiar_texto(valor) in {"s", "n"}


def validar_precio(valor):
    """Retorna True si el precio es un entero mayor que cero."""
    return isinstance(valor, int) and valor > 0


def validar_asientos(valor):
    """Retorna True si los asientos son un entero mayor o igual a cero."""
    return isinstance(valor, int) and valor >= 0


# ---------------------------------------------------------------------
# PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------
def main():
    # Inicialización local de diccionarios (IE 2.1.1)
    recorridos = {
        'R001': ['Santiago', 'Valparaíso', 120, 'normal', 'dia', True],
        'R002': ['Santiago', 'Concepción', 500, 'cama', 'noche', True],
        'R003': ['La Serena', 'Coquimbo', 15, 'normal', 'dia', False],
        'R004': ['Temuco', 'Valdivia', 165, 'semi-cama', 'dia', True],
        'R005': ['Iquique', 'Arica', 310, 'cama', 'noche', False],
        'R006': ['Santiago', 'Rancagua', 90, 'normal', 'dia', True]
    }
    
    venta = {
        'R001': [7990, 20],
        'R002': [25990, 0],
        'R003': [1990, 35],
        'R004': [12990, 8],
        'R005': [18990, 3],
        'R006': [4990, 12]
    }

    while True:
        mostrar_menu()
        opcion = leer_opcion()

        if opcion is None:
            continue

        elif opcion == 1:
            origen = input("Ingrese ciudad de origen a consultar: ")
            asientos_origen(origen, recorridos, venta)

        elif opcion == 2:
            p_min, p_max = solicitar_rango_precios()
            busqueda_precio(p_min, p_max, recorridos, venta)

        elif opcion == 3:
            while True:
                codigo = input("Ingrese código del recorrido: ")

                while True:
                    try:
                        nuevo_precio = int(input("Ingrese nuevo precio: ").strip())
                        if nuevo_precio > 0:
                            break
                        print("El precio debe ser mayor que cero")
                    except (ValueError, EOFError):
                        print("Debe ingresar valores enteros")

                if actualizar_precio(codigo, nuevo_precio, recorridos, venta):
                    print("Precio actualizado")
                else:
                    print("El código no existe")

                respuesta = input("¿Desea actualizar otro precio (s/n)?: ")
                if limpiar_texto(respuesta) != "s":
                    break

        elif opcion == 4:
            codigo = input("Ingrese código del recorrido: ")
            if not validar_codigo(codigo, recorridos):
                if buscar_codigo(codigo, recorridos):
                    print("El código ya existe")
                else:
                    print("El código no puede estar vacío")
                continue

            origen = input("Ingrese origen: ")
            if not validar_origen(origen):
                print("El origen no puede estar vacío")
                continue

            destino = input("Ingrese destino: ")
            if not validar_destino(destino):
                print("El destino no puede estar vacío")
                continue

            # Validación de entrada para distancia con try-except
            try:
                distancia = int(input("Ingrese distancia (km): ").strip())
                if not validar_distancia(distancia):
                    print("La distancia debe ser un entero mayor que cero")
                    continue
            except (ValueError, EOFError):
                print("La distancia debe ser un entero mayor que cero")
                continue

            tipo_bus = input("Ingrese tipo de bus (normal/semi-cama/cama): ")
            if not validar_tipo_bus(tipo_bus):
                print("El tipo de bus no es válido")
                continue

            servicio = input("Ingrese servicio (dia/noche): ")
            if not validar_servicio(servicio):
                print("El servicio no es válido")
                continue

            tiene_wifi = input("¿Tiene WiFi? (s/n): ")
            if not validar_wifi(tiene_wifi):
                print("Debe ingresar s o n")
                continue

            # Validación de entrada para precio con try-except
            try:
                precio = int(input("Ingrese precio: ").strip())
                if not validar_precio(precio):
                    print("El precio debe ser un entero mayor que cero")
                    continue
            except (ValueError, EOFError):
                print("El precio debe ser un entero mayor que cero")
                continue

            # Validación de entrada para asientos con try-except
            try:
                asientos = int(input("Ingrese asientos: ").strip())
                if not validar_asientos(asientos):
                    print("Los asientos deben ser un entero mayor o igual a cero")
                    continue
            except (ValueError, EOFError):
                print("Los asientos deben ser un entero mayor o igual a cero")
                continue

            # Registro definitivo en los diccionarios con valores limpios
            wifi_bool = limpiar_texto(tiene_wifi) == "s"
            if agregar_recorrido(
                codigo,
                origen,
                destino,
                distancia,
                tipo_bus,
                servicio,
                wifi_bool,
                precio,
                asientos,
                recorridos,
                venta
            ):
                print("Recorrido agregado")
            else:
                print("El código ya existe")

        elif opcion == 5:
            codigo = input("Ingrese código del recorrido: ")
            if eliminar_recorrido(codigo, recorridos, venta):
                print("Recorrido eliminado")
            else:
                print("El código no existe")

        elif opcion == 6:
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()