import socket
import threading

# Configuración del servidor
HOST = '0.0.0.0'
PORT = 12345

# Lista de clientes conectados
clients = []
nicknames = []

def broadcast(message):
    """Envía un mensaje a todos los clientes."""
    for client in clients:
        try:
            # El servidor envía el mensaje a *todos*, incluyendo al remitente.
            client.send(message.encode('utf-8'))
        except:
            remove_client(client)

def handle_client(client):
    """Maneja la comunicación con un cliente."""
    # Obtener el nickname del cliente actual
    try:
        index = clients.index(client)
        nickname = nicknames[index]
    except ValueError:
        # Si el cliente no está en la lista (posiblemente desconectado), salir.
        return

    while True:
        try:
            # Recibe el mensaje (solo el contenido, el nickname ya fue registrado por el servidor)
            message = client.recv(1024).decode('utf-8') 
            
            if message:
                # Formatea el mensaje con el nickname antes de reenviar a todos.
                full_message = f"{nickname}: {message}"
                
                print(f"[{nickname}] dice: {message}")
                broadcast(full_message) 
            else:
                # Cliente se desconectó limpiamente
                remove_client(client)
                break
        except:
            # Error de conexión
            remove_client(client)
            break

def remove_client(client):
    """Remueve un cliente desconectado."""
    if client in clients:
        try:
            index = clients.index(client)
            clients.remove(client)
            nickname = nicknames[index]
            nicknames.remove(nickname)
            client.close()
            # Envía un mensaje del sistema a todos
            broadcast(f"Sistema: {nickname} se ha desconectado.")
        except ValueError:
            # Ya fue removido o hubo un fallo en el índice
            pass

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # ******************************************************
    # 🌟 SOLUCIÓN AL ERROR WinError 10048 (SO_REUSEADDR) 🌟
    # ******************************************************
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
    
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor de chat iniciado en {HOST}:{PORT}")
    except OSError as e:
        print(f"Error al iniciar el servidor: {e}")
        print("El puerto puede estar ocupado. Espera un momento o reinicia la aplicación.")
        return

    while True:
        client, address = server.accept()
        print(f"Conexión desde {address}")

        try:
            # Recibir nickname (el cliente lo envía en cuanto se conecta)
            client.settimeout(5) # Opcional: Establecer un tiempo de espera
            nickname = client.recv(1024).decode('utf-8')
            client.settimeout(None) # Restablecer el timeout
            
            if not nickname:
                print(f"Conexión rechazada: No se recibió nickname de {address}")
                client.close()
                continue
            
        except socket.timeout:
            print(f"Tiempo de espera agotado al recibir nickname.")
            client.close()
            continue
        except:
            client.close()
            continue

        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname: {nickname}")
        
        # Notificar a todos
        broadcast(f"Sistema: {nickname} se ha unido al chat!")
        client.send("Sistema: Conectado al servidor!".encode('utf-8'))

        # Iniciar hilo para el cliente
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

if __name__ == "__main__":
    main()