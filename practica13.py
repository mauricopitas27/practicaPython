import socket

# -------------------------------------------------
# ACTIVIDAD 13: Cliente Avanzado
# -------------------------------------------------
def actividad13_cliente(host='127.0.0.1', port=8000):
    print("\n--- ACTIVIDAD 13: CLIENTE AVANZADO ---")

    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, port))

    print("Conectado al Servidor (Actividad 12).")
    print("Escribe 'salir' para terminar.\n")

    while True:
        # Enviar mensaje
        mensaje = input("Tú: ")
        cliente.send(mensaje.encode())

        if mensaje.lower() == "salir":
            break

        # Recibir respuesta del servidor
        respuesta = cliente.recv(1024).decode()
        print(f"Servidor12: {respuesta}")

    cliente.close()
    print("Cliente 13 finalizado.")
