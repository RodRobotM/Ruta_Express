import unicodedata

# ---------------------------------------------------------------------
# FUNCIONES AUXILIARES Y DE NORMALIZACIÓN
# ---------------------------------------------------------------------

def limpiar_texto(texto):
    """
    Normaliza el texto quitando acentos, espacios extras 
    y convirtiéndolo a minúsculas para comparaciones seguras.
    """
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
    Valida la opción ingresada por el menú utilizando excepciones.
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


def buscar_codigo(codigo, recorridos):
    """
    Retorna True si el código existe (insensible a mayúsculas/minúsculas).
    """
    return codigo.strip().upper() in recorridos


def asientos_origen(origen, recorridos, venta):
    """
    Acumula y muestra el total de asientos disponibles para un origen dado.
    """
    origen_buscado = limpiar_texto(origen)
    total_asientos = 0
    for codigo, datos_recorrido in recorridos.items():
        if limpiar_texto(datos_recorrido[0]) == origen_buscado and codigo in venta:
            total_asientos += venta[codigo][1]
    print(f"El total de asientos disponibles es: {total_asientos}")


def busqueda_precio(p_min, p_max, recorridos, venta):
    """
    Busca y ordena alfabéticamente los recorridos según rango de precios.
    """
    resultados = []
    for codigo, datos_venta in venta.items():
        precio, asientos = datos_venta
        if p_min <= precio <= p_max and asientos != 0 and codigo in recorridos:
            origen = recorridos[codigo][0]
            destino = recorridos[codigo][1]
            resultados.append(f"{origen}-{destino}--{codigo}")

    if resultados:
        resultados.sort(key=limpiar_texto)
        print(f"Los recorridos encontrados son: {resultados}")
    else:
        print("No hay recorridos en ese rango de precios.")


def actualizar_precio(codigo, nuevo_precio, recorridos, venta):
    """
    Actualiza el precio de un recorrido si existe en el sistema.
    """
    codigo_normalizado = codigo.strip().upper()
    if not buscar_codigo(codigo_normalizado, recorridos):
        return False
    venta[codigo_normalizado][0] = nuevo_precio
    return True


def agregar_recorrido(codigo, origen, destino, distancia, tipo_bus, servicio, tiene_wifi, precio, asientos, recorridos, venta):
    """
    Registra el nuevo recorrido en los diccionarios.
    """
    codigo_normalizado = codigo.strip().upper()
    if buscar_codigo(codigo_normalizado, recorridos):
        return False

    recorridos[codigo_normalizado] = [
        origen.strip(),
        destino.strip(),
        distancia,
        tipo_bus.strip(),
        servicio.strip(),
        tiene_wifi,
    ]
    venta[codigo_normalizado] = [precio, asientos]
    return True


def eliminar_recorrido(codigo, recorridos, venta):
    """
    Elimina un recorrido de ambos diccionarios de forma segura si existe.
    """
    codigo_normalizado = codigo.strip().upper()
    if not buscar_codigo(codigo_normalizado, recorridos):
        return False
    del recorridos[codigo_normalizado]
    del venta[codigo_normalizado]
    return True


def solicitar_rango_precios():
    """
    Pide y valida el rango de precios gestionando excepciones.
    """
    while True:
        try:
            p_min = int(input("Ingrese precio mínimo: ").strip())
            p_max = int(input("Ingrese precio máximo: ").strip())
        except (ValueError, EOFError):
            print("Debe ingresar valores enteros")
            continue

        if p_min < 0 or p_max < 0 or p_min > p_max:
            print("Debe ingresar un rango válido")
            continue

        return p_min, p_max


# ---------------------------------------------------------------------
# FUNCIONES DE VALIDACIÓN INDEPENDIENTES (Opción 4)
# ---------------------------------------------------------------------

def validar_no_vacio(valor):
    """Retorna True si el valor no está vacío ni contiene solo espacios."""
    return isinstance(valor, str) and valor.strip() != ""


def validar_distancia(valor):
    """Retorna True si la distancia es un entero mayor que cero."""
    return isinstance(valor, int) and valor > 0


def validar_tipo_bus(valor):
    """Retorna True si el bus es exactamente 'normal', 'semi-cama' o 'cama'."""
    return limpiar_texto(valor) in {"normal", "semi-cama", "cama"}


def validar_servicio(valor):
    """Retorna True si el servicio es exactamente 'dia' o 'noche'."""
    return limpiar_texto(valor) in {"dia", "noche"}


def validar_wifi(valor):
    """Retorna True si la opción de wifi ingresada es 's' o 'n'."""
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
    # Inicialización de las estructuras de datos vacías (Persistentes)
    recorridos = {}
    venta = {}

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
            origen = input("Ingrese origen: ")
            destino = input("Ingrese destino: ")

            # Validación de entrada para distancia
            try:
                distancia = int(input("Ingrese distancia (km): ").strip())
            except (ValueError, EOFError):
                distancia = -1  # Forzará el fallo en la validación de distancia de abajo

            tipo_bus = input("Ingrese tipo de bus (normal/semi-cama/cama): ")
            servicio = input("Ingrese servicio (dia/noche): ")
            tiene_wifi = input("¿Tiene WiFi? (s/n): ")

            # Validación de entrada para precio
            try:
                precio = int(input("Ingrese precio: ").strip())
            except (ValueError, EOFError):
                precio = -1

            # Validación de entrada para asientos
            try:
                asientos = int(input("Ingrese asientos: ").strip())
            except (ValueError, EOFError):
                asientos = -1

            # Despliegue de validaciones independientes usando las funciones
            if not validar_no_vacio(codigo):
                print("El código no puede estar vacío")
            elif buscar_codigo(codigo, recorridos):
                print("El código ya existe")
            elif not validar_no_vacio(origen):
                print("El origen no puede estar vacío")
            elif not validar_no_vacio(destino):
                print("El destino no puede estar vacío")
            elif not validar_distancia(distancia):
                print("La distancia debe ser un entero mayor que cero")
            elif not validar_tipo_bus(tipo_bus):
                print("El tipo de bus no es válido")
            elif not validar_servicio(servicio):
                print("El servicio no es válido")
            elif not validar_wifi(tiene_wifi):
                print("Debe ingresar s o n")
            elif not validar_precio(precio):
                print("El precio debe ser un entero mayor que cero")
            elif not validar_asientos(asientos):
                print("Los asientos deben ser un entero mayor o igual a cero")
            else:
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