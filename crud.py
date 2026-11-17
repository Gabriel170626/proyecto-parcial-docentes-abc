from datetime import date
import sqlite3

print("-----------------------------------------------------------------------------------")
print("---------Bienvenido al sistema de gestión de docentes de la Universidad ABC--------")
print("-----------------------------------------------------------------------------------")

# Fecha límite de registro (igual para todos los registros).
# Si el profesor da una extensión, solo hay que cambiar esta línea.
FECHA_LIMITE = date(2026, 11, 19)

# ---------------------------------------------------------------
# Conexión a la base de datos SQLite
# ---------------------------------------------------------------
conexion = sqlite3.connect("docentes.db")
conexion.row_factory = sqlite3.Row  # permite usar docente["nombre"] en vez de docente[0]
cursor = conexion.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS docentes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        departamento TEXT NOT NULL,
        correo TEXT NOT NULL,
        cedula TEXT NOT NULL UNIQUE,
        asignatura TEXT NOT NULL,
        telefono TEXT NOT NULL,
        condicion_laboral TEXT NOT NULL
    )
''')
conexion.commit()


# ---------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------
def mostrar_menu():
    print("1. Registrar docente")
    print("2. Consultar docentes")
    print("3. Actualizar docente")
    print("4. Eliminar docente")
    print("5. Filtrar docentes por departamento")
    print("6. Salir")


def correo_valido(correo):
    """Devuelve True si el correo no tiene espacios, tiene un solo @ y un punto en el dominio."""
    if " " in correo:
        return False
    if correo.count("@") != 1:
        return False
    dominio = correo.split("@")[1]
    if "." not in dominio:
        return False
    return True


def cedula_existente(cedula):
    """Devuelve True si ya hay un docente con esa cédula en la base de datos."""
    cursor.execute("SELECT 1 FROM docentes WHERE cedula = ?", (cedula,))
    return cursor.fetchone() is not None


def imprimir_docente(docente):
    print(f"Nombre: {docente['nombre']}, Departamento: {docente['departamento']}, "
          f"Correo: {docente['correo']}, Cédula: {docente['cedula']}, "
          f"Asignatura: {docente['asignatura']}, Teléfono: {docente['telefono']}, "
          f"Condición laboral: {docente['condicion_laboral']}")


# ---------------------------------------------------------------
# Operaciones del CRUD
# ---------------------------------------------------------------
def registrar_docente():
    # Validación de la fecha límite de registro
    if date.today() > FECHA_LIMITE:
        print(f"El registro de docentes cerró el {FECHA_LIMITE.strftime('%d/%m/%Y')}. "
              "No se pueden registrar nuevos docentes.")
        return

    # La cédula se pide primero para no hacer escribir datos si ya existe
    cedula = input("Ingrese la cédula del docente: ")
    if cedula_existente(cedula):
        print("Ya existe un docente registrado con esa cédula.")
        return

    nombre = input("Ingrese el nombre del docente: ")
    departamento = input("Ingrese el departamento del docente: ")
    correo = input("Ingrese el correo del docente: ")
    while not correo_valido(correo):
        print("Correo inválido. Asegúrese de que no contenga espacios, tenga un solo '@' y un dominio válido.")
        correo = input("Ingrese el correo del docente: ")
    asignatura = input("Ingrese la asignatura del docente: ")
    telefono = input("Ingrese el teléfono del docente: ")
    condicion_laboral = input("Ingrese la condición laboral del docente: ")

    cursor.execute('''
        INSERT INTO docentes (nombre, departamento, correo, cedula, asignatura, telefono, condicion_laboral)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nombre, departamento, correo, cedula, asignatura, telefono, condicion_laboral))
    conexion.commit()
    print("Docente registrado exitosamente.")


def consultar_docentes():
    cursor.execute("SELECT * FROM docentes")
    filas = cursor.fetchall()
    if len(filas) == 0:
        print("No hay docentes registrados.")
    else:
        for docente in filas:
            imprimir_docente(docente)


def actualizar_docente():
    cedula = input("Ingrese la cédula del docente a actualizar: ")
    if not cedula_existente(cedula):
        print("No se encontró un docente con esa cédula.")
        return

    nombre = input("Ingrese el nuevo nombre del docente: ")
    departamento = input("Ingrese el nuevo departamento del docente: ")
    correo = input("Ingrese el nuevo correo del docente: ")
    while not correo_valido(correo):
        print("Correo inválido. Asegúrese de que no contenga espacios, tenga un solo '@' y un dominio válido.")
        correo = input("Ingrese el nuevo correo del docente: ")
    asignatura = input("Ingrese la nueva asignatura del docente: ")
    telefono = input("Ingrese el nuevo teléfono del docente: ")
    condicion_laboral = input("Ingrese la nueva condición laboral del docente: ")

    cursor.execute('''
        UPDATE docentes
        SET nombre = ?, departamento = ?, correo = ?, asignatura = ?, telefono = ?, condicion_laboral = ?
        WHERE cedula = ?
    ''', (nombre, departamento, correo, asignatura, telefono, condicion_laboral, cedula))
    conexion.commit()
    print("Docente actualizado exitosamente.")


def eliminar_docente():
    cedula = input("Ingrese la cédula del docente a eliminar: ")
    cursor.execute("DELETE FROM docentes WHERE cedula = ?", (cedula,))
    conexion.commit()
    # rowcount indica cuántas filas se borraron: 0 significa que no existía
    if cursor.rowcount == 0:
        print("No se encontró un docente con esa cédula.")
    else:
        print("Docente eliminado exitosamente.")


def filtrar_docentes_por_departamento():
    departamento = input("Ingrese el departamento para filtrar: ")
    cursor.execute("SELECT * FROM docentes WHERE LOWER(departamento) = LOWER(?)", (departamento,))
    filas = cursor.fetchall()
    if len(filas) == 0:
        print("No se encontraron docentes en ese departamento.")
    else:
        for docente in filas:
            imprimir_docente(docente)


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------
opcion = ""

while opcion != "6":
    mostrar_menu()
    opcion = input("Seleccione una opción: ")
    if opcion == "1":
        registrar_docente()
    elif opcion == "2":
        consultar_docentes()
    elif opcion == "3":
        actualizar_docente()
    elif opcion == "4":
        eliminar_docente()
    elif opcion == "5":
        filtrar_docentes_por_departamento()
    elif opcion != "6":
        print("Opción inválida. Elija un número del 1 al 6.")

conexion.close()
print("¡Gracias por usar el sistema de gestión de docentes!")