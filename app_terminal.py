import requests  # Importa la biblioteca requests para realizar solicitudes HTTP

# URL base de la API
BASE_URL = "http://127.0.0.1:8000/api/"

def mostrar_menu():
    """
    Muestra el menú de opciones CRUD para interactuar con la API.
    """
    print("\n--- Menú CRUD ---")
    print("1. Crear Cliente")
    print("2. Listar Clientes")
    print("3. Actualizar Cliente")
    print("4. Eliminar Cliente")
    print("5. Salir")

def validar_respuesta(response, accion):
    """
    Valida la respuesta HTTP de una solicitud.
    - response: Respuesta de la solicitud HTTP.
    - accion: Acción realizada (crear, listar, actualizar, eliminar).
    """
    if response.status_code in [200, 201, 204]:  # Respuesta exitosa
        print(f"{accion} completado con éxito.\n")
    else:  # En caso de error
        print(f"Error al {accion.lower()}:\n{response.json()}\n")

def crear_cliente():
    """
    Solicita al usuario los datos de un cliente y realiza una solicitud POST para crearlo.
    """
    print("\n--- Crear Cliente ---")
    try:
        # Solicitar datos al usuario
        nombre = input("Nombre: ").strip()
        correo = input("Correo: ").strip()
        telefono = input("Teléfono: ").strip()

        # Validación básica: Ningún campo debe estar vacío
        if not nombre or not correo or not telefono:
            print("Todos los campos son obligatorios. Inténtalo de nuevo.\n")
            return

        # Datos a enviar en la solicitud
        data = {"nombre": nombre, "correo": correo, "telefono": telefono}
        response = requests.post(BASE_URL + "clientes/", json=data)  # Solicitud POST
        validar_respuesta(response, "crear cliente")
    except Exception as e:
        print(f"Error inesperado: {e}")  # Captura de errores no esperados

def listar_clientes():
    """
    Realiza una solicitud GET para obtener y mostrar la lista de clientes.
    """
    print("\n--- Lista de Clientes ---")
    try:
        response = requests.get(BASE_URL + "clientes/")  # Solicitud GET

        if response.status_code == 200:
            clientes = response.json()  # Convertir la respuesta a JSON
            if not clientes:  # Si la lista está vacía
                print("No hay clientes registrados.\n")
                return

            # Mostrar cada cliente en la lista
            for cliente in clientes:
                print(f"ID: {cliente['id']} | Nombre: {cliente['nombre']} | Correo: {cliente['correo']} | Teléfono: {cliente['telefono']}")
        else:
            validar_respuesta(response, "listar clientes")
    except Exception as e:
        print(f"Error inesperado: {e}")

def actualizar_cliente():
    """
    Solicita un ID de cliente y nuevos datos, luego realiza una solicitud PUT para actualizar.
    """
    print("\n--- Actualizar Cliente ---")
    try:
        # Solicitar ID del cliente
        cliente_id = input("ID del cliente a actualizar: ").strip()
        if not cliente_id.isdigit():  # Validar que el ID sea numérico
            print("El ID debe ser un número válido.\n")
            return

        # Solicitar los nuevos datos del cliente
        nombre = input("Nuevo Nombre: ").strip()
        correo = input("Nuevo Correo: ").strip()
        telefono = input("Nuevo Teléfono: ").strip()

        if not nombre or not correo or not telefono:
            print("Todos los campos son obligatorios. Inténtalo de nuevo.\n")
            return

        # Datos actualizados
        data = {"nombre": nombre, "correo": correo, "telefono": telefono}
        response = requests.put(BASE_URL + f"clientes/{cliente_id}/", json=data)  # Solicitud PUT
        validar_respuesta(response, "actualizar cliente")
    except Exception as e:
        print(f"Error inesperado: {e}")

def eliminar_cliente():
    """
    Solicita un ID de cliente y realiza una solicitud DELETE para eliminarlo.
    """
    print("\n--- Eliminar Cliente ---")
    try:
        cliente_id = input("ID del cliente a eliminar: ").strip()
        if not cliente_id.isdigit():  # Validar que el ID sea numérico
            print("El ID debe ser un número válido.\n")
            return

        response = requests.delete(BASE_URL + f"clientes/{cliente_id}/")  # Solicitud DELETE
        validar_respuesta(response, "eliminar cliente")
    except Exception as e:
        print(f"Error inesperado: {e}")

def main():
    """
    Función principal que ejecuta el programa, muestra el menú y maneja las opciones del usuario.
    """
    while True:
        mostrar_menu()  # Mostrar las opciones CRUD
        opcion = input("Selecciona una opción (1-5): ").strip()

        if opcion == "1":
            crear_cliente()
        elif opcion == "2":
            listar_clientes()
        elif opcion == "3":
            actualizar_cliente()
        elif opcion == "4":
            eliminar_cliente()
        elif opcion == "5":  # Salir del programa
            print("Saliendo del programa. ¡Hasta luego!\n")
            break
        else:
            print("Opción inválida, intenta de nuevo.\n")

if __name__ == "__main__":
    main()  # Ejecutar la función principal
