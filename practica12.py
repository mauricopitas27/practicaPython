import socket

# -------------------------------------------------
# ACTIVIDAD 12: Servidor Avanzado
# -------------------------------------------------
def actividad12_servidor(host='127.0.0.1', port=8000):
    print("\n--- ACTIVIDAD 12: SERVIDOR AVANZADO ---")

    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, port))
    servidor.listen(1)

    print(f"Servidor avanzado iniciado en {host}:{port}")
    print("Esperando conexión del cliente...")

    conn, addr = servidor.accept()
    print(f"Cliente conectado desde: {addr}")

    while True:
        # Recibir mensaje
        recibido = conn.recv(1024).decode()

        if not recibido or recibido.lower() == "salir":
            print("El cliente se desconectó.")
            break

        print(f"Cliente dice: {recibido}")

        # Responder
        respuesta = f"Servidor12: Mensaje recibido -> {recibido}"
        conn.send(respuesta.encode())

    conn.close()
    servidor.close()
    print("Servidor 12 finalizado.")
