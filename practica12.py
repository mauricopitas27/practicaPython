import socket
import threading

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 12345

# Lista de clientes conectados
clients = []
nicknames = []

def broadcast(message, sender_client=None):
    """Envía un mensaje a todos los clientes, excepto al remitente si se especifica."""
    for client in clients:
        if client != sender_client:
            try:
                client.send(message.encode('utf-8'))
            except:
                remove_client(client)

def handle_client(client):
    """Maneja la comunicación con un cliente."""
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message:
                print(f"Mensaje recibido: {message}")
                broadcast(message, client)
            else:
                remove_client(client)
                break
        except:
            remove_client(client)
            break

def remove_client(client):
    """Remueve un cliente desconectado."""
    if client in clients:
        index = clients.index(client)
        clients.remove(client)
        nickname = nicknames[index]
        nicknames.remove(nickname)
        client.close()
        broadcast(f"{nickname} se ha desconectado.")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Servidor de chat iniciado en {HOST}:{PORT}")

    while True:
        client, address = server.accept()
        print(f"Conexión desde {address}")

        # Solicitar nickname
        client.send("NICK".encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        broadcast(f"{nickname} se ha unido al chat!")
        client.send("Conectado al servidor!".encode('utf-8'))

        # Iniciar hilo para el cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()