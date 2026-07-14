# RutaExpress — Sistema de Gestión de Recorridos y Ventas 🚌

Este repositorio contiene el sistema de administración de buses y disponibilidad de asientos para la empresa de transporte **RutaExpress**. El programa está desarrollado en Python, estructurado bajo un enfoque modular y diseñado para garantizar la integridad de los datos a través de validaciones robustas y manejo de excepciones.

---

## 🚀 Uso Rápido

### Requisitos Previos
* Python 3.10 o superior instalado en tu sistema.

### Instrucciones de Ejecución
1. Clona o descarga este repositorio.
2. Abre tu terminal de preferencia en la carpeta del proyecto.
3. Ejecuta el script principal con el siguiente comando:

   python3 RutaExpress.py

---

## 📋 Arquitectura de las Estructuras de Datos

El sistema trabaja con dos diccionarios principales relacionados de forma relacional utilizando el **código de recorrido** como clave común. Ambos diccionarios se inicializan vacíos en el programa principal y se actualizan dinámicamente durante la ejecución.

### 1. Diccionario `recorridos`
Mapea `codigo` (str) -> Lista con los atributos descriptivos del servicio:

| Índice | Campo | Tipo | Restricción / Formato |
| :---: | :--- | :--- | :--- |
| **0** | `origen` | `str` | Ciudad de origen (no vacía). |
| **1** | `destino` | `str` | Ciudad de destino (no vacía). |
| **2** | `distancia_km` | `int` | Distancia total > 0. |
| **3** | `tipo_bus` | `str` | 'normal', 'semi-cama' o 'cama'. |
| **4** | `servicio` | `str` | 'dia' o 'noche'. |
| **5** | `tiene_wifi` | `bool` | True o False. |

### 2. Diccionario `venta`
Mapea `codigo` (str) -> Lista con la información operativa de la venta:

| Índice | Campo | Tipo | Restricción / Formato |
| :---: | :--- | :--- | :--- |
| **0** | `precio` | `int` | Precio en pesos > 0. |
| **1** | `asientos` | `int` | Cantidad de asientos disponibles >= 0. |

> ⚠️ **Regla de Diseño Estricta:** Para evitar acoplamiento y asegurar el cumplimiento de la rúbrica académica, está **estrictamente prohibido** el uso de la sentencia `global`. Los diccionarios deben pasarse explícitamente como argumentos a cada función de control.

---

## 🛠️ Documentación de Funciones

### Funciones Auxiliares y de Interfaz

*   **`limpiar_texto(texto)`**
    *   **Descripción:** Normaliza una cadena de texto (elimina espacios adicionales en los extremos, convierte a minúsculas y remueve tildes y diacríticos).
    *   **Parámetros:** `texto` (`str`).
    *   **Retorna:** `str` normalizado.
*   **`mostrar_menu()`**
    *   **Descripción:** Despliega el menú principal interactivo de la aplicación por consola.
    *   **Parámetros:** Ninguno.
    *   **Retorna:** `None`.
*   **`leer_opcion()`**
    *   **Descripción:** Captura la opción del menú seleccionada por el usuario. Realiza un manejo de excepciones (`ValueError`) para garantizar que el valor ingresado sea un entero entre 1 y 6.
    *   **Parámetros:** Ninguno.
    *   **Retorna:** `int` (opción válida) o `None` (si hay error).

### Lógica de Negocio y Control

*   **`buscar_codigo(codigo, recorridos)`**
    *   **Descripción:** Determina si un código de recorrido ya existe en el sistema. La búsqueda es insensible a mayúsculas y minúsculas.
    *   **Parámetros:** `codigo` (`str`), `recorridos` (`dict`).
    *   **Retorna:** `bool`.
*   **`asientos_origen(origen, recorridos, venta)`**
    *   **Descripción:** Busca todos los servicios que coincidan con la ciudad de origen consultada (ignorando acentos y mayúsculas) y acumula el total de sus asientos disponibles.
    *   **Parámetros:** `origen` (`str`), `recorridos` (`dict`), `venta` (`dict`).
    *   **Retorna:** `None` (imprime el resultado directamente).
*   **`busqueda_precio(p_min, p_max, recorridos, venta)`**
    *   **Descripción:** Filtra y genera una lista ordenada alfabéticamente con los recorridos que se encuentran en el rango de precios solicitado y que cuentan con asientos disponibles (> 0).
    *   **Parámetros:** `p_min` (`int`), `p_max` (`int`), `recorridos` (`dict`), `venta` (`dict`).
    *   **Retorna:** `None` (imprime la lista formateada como "Origen-Destino--Código").
*   **`actualizar_precio(codigo, nuevo_precio, recorridos, venta)`**
    *   **Descripción:** Modifica el precio de un recorrido existente en el sistema. Llama internamente a `buscar_codigo` para validar su existencia.
    *   **Parámetros:** `codigo` (`str`), `nuevo_precio` (`int`), `recorridos` (`dict`), `venta` (`dict`).
    *   **Retorna:** `bool` (`True` si se actualizó con éxito, `False` en caso contrario).
*   **`agregar_recorrido(codigo, origen, destino, distancia, tipo_bus, servicio, tiene_wifi, precio, asientos, recorridos, venta)`**
    *   **Descripción:** Registra un nuevo recorrido en ambos diccionarios de forma estructurada siempre y cuando el código sea único.
    *   **Parámetros:** Ver firma completa.
    *   **Retorna:** `bool` (`True` si se registró correctamente, `False` si el código ya existía).
*   **`eliminar_recorrido(codigo, recorridos, venta)`**
    *   **Descripción:** Remueve completamente el registro de un recorrido de ambos diccionarios si el código ingresado existe.
    *   **Parámetros:** `codigo` (`str`), `recorridos` (`dict`), `venta` (`dict`).
    *   **Retorna:** `bool` (`True` si la operación fue exitosa, `False` si el código no existía).
*   **`solicitar_rango_precios()`**
    *   **Descripción:** Pide las entradas de precio mínimo y máximo al usuario, controlando mediante un bucle interactivo que los valores sean enteros válidos y lógicos.
    *   **Parámetros:** Ninguno.
    *   **Retorna:** `tuple` `(p_min, p_max)`.

---

## 🔒 Validaciones Independientes (Filtros de Entrada)

Cada una de estas funciones recibe únicamente **un parámetro** de entrada (el dato a validar) y retorna un valor booleano (`True` o `False`), de acuerdo con lo requerido en las especificaciones del desarrollo:

| Función | Parámetro | Condición de Aprobación (`True`) |
| :--- | :--- | :--- |
| `validar_no_vacio(valor)` | `str` | La cadena no debe estar vacía ni contener solo espacios en blanco. |
| `validar_distancia(valor)` | `int` | El valor debe ser un entero estrictamente mayor que cero. |
| `validar_tipo_bus(valor)` | `str` | Debe coincidir con 'normal', 'semi-cama' o 'cama'. |
| `validar_servicio(valor)` | `str` | Debe coincidir con 'dia' o 'noche'. |
| `validar_wifi(valor)` | `str` | Debe ser exactamente 's' o 'n'. |
| `validar_precio(valor)` | `int` | El valor del pasaje debe ser un entero mayor que cero. |
| `validar_asientos(valor)` | `int` | La capacidad de asientos debe ser un entero mayor o igual a cero. |