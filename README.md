# Sistema de Gestión de Docentes - Universidad ABC

Proyecto de la 2da Evaluación Parcial de INF-161 Introducción a la Programación (UNPHU).

## Descripción

Programa de consola en Python para administrar los docentes de la Universidad ABC. Permite registrar, consultar, actualizar y eliminar docentes, y guarda todos los datos en una base de datos SQLite, de modo que la información se conserva al cerrar el programa.

De cada docente se guarda: nombre, cédula, correo electrónico, teléfono, departamento, asignatura y condición laboral.

## Funciones

- Registrar, consultar, actualizar y eliminar docentes.
- Filtrar docentes por departamento (sin importar mayúsculas o minúsculas).
- Evitar cédulas duplicadas.
- Validar el formato del correo electrónico al registrar y al actualizar.
- Fecha límite de registro: pasada la fecha, no se pueden registrar nuevos docentes.
- Datos guardados en una base de datos SQLite (`docentes.db`).

## Requisitos

- Python 3 (el módulo `sqlite3` viene incluido, e instalar SQLITE Viewer despues de eso no hay que instalar nada más).

## Cómo ejecutarlo

Desde la carpeta del proyecto:

``` text
py crud.py
```

El archivo `docentes.db` se crea automáticamente la primera vez que se ejecuta el programa.

## Menú del programa

``` text
1. Registrar docente
2. Consultar docentes
3. Actualizar docente
4. Eliminar docente
5. Filtrar docentes por departamento
6. Salir
```

## Validaciones

- **Cédula:** no se permite registrar dos docentes con la misma cédula.
- **Correo:** no puede tener espacios, debe tener un solo `@` y un punto en el dominio.
- **Fecha límite:** el registro de nuevos docentes está abierto hasta el 19/11/2026. Si hay una extensión, se cambia la constante `FECHA_LIMITE` al inicio de `crud.py`.

## Estructura del proyecto

- `crud.py`: programa principal con el CRUD de docentes.
- `docentes.db`: base de datos SQLite (se genera sola y no se sube al repositorio).
- `.gitignore`: archivos que Git debe ignorar.

## Autor

Gabriel Del Jesus Mendez Aybar - Matrícula 26-0382
