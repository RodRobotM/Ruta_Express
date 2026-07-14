# Ruta Express

Este repositorio contiene `RutaExpress.py`, un script para gestionar recorridos de buses.

Contenido:
- `RutaExpress.py`: programa principal con funciones para crear, buscar, actualizar y eliminar recorridos.

Uso rápido

1. Ejecutar el script:

```bash
python3 RutaExpress.py
```

Descripción de las estructuras

- `recorridos` (dict): mapea `codigo` -> [origen, destino, distancia, tipo_bus, servicio, tiene_wifi]
- `venta` (dict): mapea `codigo` -> [precio, asientos]

Funciones (resumen)

Las siguientes funciones están definidas en `RutaExpress.py`. Abre el archivo para ver implementaciones completas.

- `limpiar_texto(texto)`
	- Normaliza una cadena: trim, minúsculas y elimina tildes.
	- Parámetros: `texto` (str)
	- Retorna: `str` normalizado.

- `mostrar_menu()`
	- Imprime el menú principal en consola.
	- Parámetros: ninguno. Retorna: `None`.

- `leer_opcion()`
	- Lee y valida la opción del menú (1-6).
	- Parámetros: ninguno. Retorna: `int` opción válida o `None`.

- `buscar_codigo(codigo, recorridos)`
	- Comprueba si `codigo` existe en `recorridos` (insensible a mayúsculas).
	- Parámetros: `codigo` (str), `recorridos` (dict).
	- Retorna: `bool`.

- `asientos_origen(origen, recorridos, venta)`
	- Calcula y muestra el total de asientos disponibles para una ciudad de origen.
	- Parámetros: `origen` (str), `recorridos` (dict), `venta` (dict).
	- Retorna: `None` (imprime resultado).

- `busqueda_precio(p_min, p_max, recorridos, venta)`
	- Busca recorridos cuyo precio esté entre `p_min` y `p_max`, con asientos disponibles, y los imprime ordenados.
	- Parámetros: `p_min` (int), `p_max` (int), `recorridos` (dict), `venta` (dict).
	- Retorna: `None` (imprime resultado).

- `actualizar_precio(codigo, nuevo_precio, recorridos, venta)`
	- Actualiza el precio de un recorrido si existe.
	- Parámetros: `codigo` (str), `nuevo_precio` (int), `recorridos` (dict), `venta` (dict).
	- Retorna: `bool` (True si se actualizó).

- `agregar_recorrido(codigo, origen, destino, distancia, tipo_bus, servicio, tiene_wifi, precio, asientos, recorridos, venta)`
	- Añade un nuevo recorrido a `recorridos` y `venta` si el código no existe.
	- Parámetros: ver firma. `tiene_wifi` se guarda como booleano según el flujo principal.
	- Retorna: `bool` (True si se agregó).

- `eliminar_recorrido(codigo, recorridos, venta)`
	- Elimina un recorrido de ambos diccionarios si existe.
	- Parámetros: `codigo` (str), `recorridos` (dict), `venta` (dict).
	- Retorna: `bool`.

- `solicitar_rango_precios()`
	- Pide al usuario un rango de precios válido y lo retorna.
	- Parámetros: ninguno. Retorna: `(p_min, p_max)`.

Funciones de validación (usadas en la opción de agregar recorrido)

- `validar_no_vacio(valor)` → `bool`  — Verifica que no sea cadena vacía.
- `validar_distancia(valor)` → `bool`  — Entero > 0.
- `validar_tipo_bus(valor)` → `bool`  — 'normal', 'semi-cama' o 'cama'.
- `validar_servicio(valor)` → `bool`  — 'dia' o 'noche'.
- `validar_wifi(valor)` → `bool`  — 's' o 'n'.
- `validar_precio(valor)` → `bool`  — Entero > 0.
- `validar_asientos(valor)` → `bool`  — Entero >= 0.

- `main()`
	- Bucle principal del programa que muestra el menú y gestiona la interacción con el usuario.

Notas y recomendaciones

- Las validaciones esperan tipos `int` ya convertidos cuando corresponda; el flujo principal maneja conversiones y excepciones.
- `recorridos` y `venta` son simples `dict` en memoria: para persistencia se debe agregar lectura/escritura a archivo.

¿Quieres que también genere ejemplos de uso o tests unitarios para algunas funciones? 
