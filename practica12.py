# practica12.py
import socket
import threading
import requests

# Config
HOST = '0.0.0.0'
PORT = 12345
API_POST_URL = "http://127.0.0.1:8000/api/mensajes/crear"

clients = []
nicknames = []

def save_message_api(sender, message):
    url = "http://127.0.0.1:8000/api/mensajes/crear"

    # Laravel pide estos 3 campos
    payload = {
        "usuario": sender,
        "mensaje": message,
        "fecha_hora": "2025-01-01 12:00:00"  # puedes poner fecha automática abajo
    }

    try:
        resp = requests.post(url, json=payload)

        if resp.status_code == 201:
            print("✔ Mensaje guardado en API")
        else:
            print(f"❌ API Error POST: No se pudo guardar. Estado: {resp.status_code} - {resp.text}")

    except Exception as e:
        print("❌ Error enviando a API:", e)

def broadcast(message):
    """Envía message (string) a todos los clientes conectados."""
    for client in clients.copy():
        try:
            client.send(message.encode('utf-8'))
        except Exception:
            remove_client(client)

def handle_client(client):
    """Recibe mensajes de un cliente y los retransmite; guarda en API."""
    try:
        index = clients.index(client)
        nickname = nicknames[index]
    except ValueError:
        return

    while True:
        try:
            message = client.recv(4096).decode('utf-8')
            if not message:
                # desconectó
                remove_client(client)
                break

            full_message = f"{nickname}: {message}"
            print(f"[{nickname}] {message}")

            # reenviar a todos
            broadcast(full_message)

            # guardar en API
            save_message_api(nickname, message)

        except Exception as e:
            print("Error handle_client:", e)
            remove_client(client)
            break

def remove_client(client):
    """Remueve cliente desconectado y notifica."""
    if client in clients:
        try:
            idx = clients.index(client)
            nickname = nicknames[idx]
            clients.remove(client)
            nicknames.pop(idx)
            client.close()
            broadcast(f"Sistema: {nickname} se ha desconectado.")
            print(f"{nickname} desconectado y removido.")
        except Exception as e:
            print("Error remove_client:", e)

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        server.bind((HOST, PORT))
        server.listen()
        print(f"Servidor chat escuchando en {HOST}:{PORT}")
    except OSError as e:
        print("Error al iniciar el servidor:", e)
        return

    while True:
        client, address = server.accept()
        print("Conexión entrante desde", address)

        # esperamos que el cliente envíe el nickname inmediatamente
        try:
            client.settimeout(5)
            nickname = client.recv(1024).decode('utf-8').strip()
            client.settimeout(None)
            if not nickname:
                print("No se recibió nickname, cerrando conexión.")
                client.close()
                continue
        except Exception as e:
            print("Error recibiendo nickname:", e)
            client.close()
            continue

        clients.append(client)
        nicknames.append(nickname)
        print(f"Nickname conectado: {nickname}")

        # Notificar a todos
        broadcast(f"Sistema: {nickname} se ha unido al chat!")
        client.send("Sistema: Conectado al servidor!".encode('utf-8'))

        # arrancar hilo
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    main()
