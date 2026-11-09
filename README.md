# Sistema IFN - Inventario Forestal Nacional (IDEAM)

Proyecto de aula desarrollado en **Python** con interfaz gráfica en **Tkinter**. La aplicación permite registrar y consultar inspecciones de campo del Inventario Forestal Nacional (IFN), almacenando la información en un archivo de texto plano.

## Integrantes

- Jonathan Mauricio Quintero Serrano
- Juan David Contreras

## Descripción

El sistema simula una herramienta de apoyo para las brigadas de campo que levantan información de los conglomerados forestales. Con ella se puede:

- Registrar los datos generales de una inspección (ID, conglomerado y brigada).
- Anotar el conteo de árboles según su categoría de diámetro: **fustales**, **latizales** y **brinzales**.
- Registrar las **muestras vegetales** recolectadas, con su código, nombre común y uso (medicinal, alimenticio o maderable).
- Guardar toda la inspección en un archivo de texto.
- Consultar una inspección guardada a partir de su ID y ver un reporte con todos sus datos.

## Requisitos

- Python 3.x
- Tkinter (viene incluido con la instalación estándar de Python; no requiere instalar librerías externas)

> En algunas distribuciones de Linux hay que instalarlo aparte, por ejemplo: `sudo apt install python3-tk`

## Cómo ejecutar

1. Descargar o clonar el proyecto.
2. Abrir una terminal en la carpeta donde está el archivo.
3. Ejecutar:

```bash
python proyecto_de_aula.py
```

## Estructura del código

El programa está organizado en dos clases:

### `InventarioForestal` (lógica de datos)

Se encarga de leer y escribir en el archivo `datos_inventario.txt`.

| Método | Función |
|---|---|
| `guardarInspeccion(...)` | Convierte los datos de la inspección en una línea de texto y la agrega al final del archivo. |
| `consultarInspeccion(idBusqueda)` | Recorre el archivo y devuelve los datos de la primera inspección cuyo ID coincida; si no existe, devuelve `None`. |

### `FrontIFN` (interfaz gráfica)

Construye la ventana principal con dos pestañas:

**1. Registrar Inspección**
- *Datos del Conglomerado y Brigada:* ID de inspección, conglomerado y brigada.
- *Conteo de Árboles:* cantidad de fustales, latizales y brinzales.
- *Toma de Muestras Vegetales:* formulario para agregar muestras a una tabla temporal (`Treeview`) antes de guardar.
- Botón **GUARDAR INSPECCIÓN**, que valida los datos, guarda el registro y limpia el formulario.

**2. Consultar Inspección**
- Campo de búsqueda por ID de inspección.
- Visor de resultados de solo lectura con el reporte de la inspección encontrada (datos generales, conteo de árboles y lista de muestras).

## Validaciones

- Todos los campos de datos generales y de conteo son obligatorios.
- Los conteos de fustales, latizales y brinzales deben ser números enteros.
- Para agregar una muestra es obligatorio ingresar el código y el nombre común.
- Para consultar se debe ingresar un ID.

## Formato del archivo de datos

Los registros se guardan en `datos_inventario.txt` (se crea automáticamente al guardar la primera inspección). Cada inspección ocupa una línea, con los campos separados por `|`:

```
idInspeccion|conglomerado|brigada|fustales|latizales|brinzales|muestras
```

Las muestras van separadas por `;` y los atributos de cada muestra por `,`:

```
codigo1,nombre1,uso1;codigo2,nombre2,uso2
```

**Ejemplo de una línea guardada:**

```
INS-001|C-245|Brigada 3|12|30|85|M01,Cedro,maderable;M02,Sábila,medicinal
```

## Limitaciones conocidas

- No se permite el uso de los caracteres `|`, `;` y `,` dentro de los campos de texto, ya que se usan como separadores y podrían dañar el formato del archivo.
- No se verifica que el ID de inspección sea único: si se repite, la consulta devuelve solo el primer registro encontrado.
- No existe opción para editar o eliminar inspecciones ya guardadas.

## Posibles mejoras

- Validar que el ID no esté repetido antes de guardar.
- Agregar opciones para editar y eliminar registros.
- Permitir quitar muestras de la tabla temporal antes de guardar.
- Exportar los reportes a PDF o Excel.
- Migrar el almacenamiento a una base de datos (por ejemplo, SQLite).
