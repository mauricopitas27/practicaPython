# practica13.py
import socket
import threading
import requests

API_GET_URL = "http://127.0.0.1:8000/api/mensajes"

class ChatClient:
    def __init__(self):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.gui_callback = None

    def set_gui_callback(self, callback):
        """callback(msg: str) -> None  -> GUI debe proporcionar esta función."""
        self.gui_callback = callback

    def connect(self, nickname, host="127.0.0.1", port=12345):
        try:
            self.client_socket.connect((host, port))
            # enviar nickname al conectarse (el servidor lo espera)
            self.client_socket.send(nickname.encode('utf-8'))
            self.connected = True
            threading.Thread(target=self.receive_messages, daemon=True).start()
            return True
        except Exception as e:
            print("No se pudo conectar:", e)
            return False

    def receive_messages(self):
        while self.connected:
            try:
                msg = self.client_socket.recv(4096).decode('utf-8')
                if not msg:
                    self.connected = False
                    break
                if self.gui_callback:
                    self.gui_callback(msg)
            except Exception:
                self.connected = False
                break

    def send_message(self, msg):
        try:
            self.client_socket.send(msg.encode('utf-8'))
        except Exception as e:
            print("Error enviar mensaje:", e)
            self.connected = False

    def get_history(self):
        """Obtiene historial desde Laravel (GET). Devuelve lista de dicts."""
        try:
            resp = requests.get(API_GET_URL, timeout=5)
            if resp.status_code == 200:
                return resp.json()
            else:
                print("Error GET historial:", resp.status_code, resp.text)
                return []
        except Exception as e:
            print("Error GET historial:", e)
            return []

    def disconnect(self):
        try:
            self.connected = False
            self.client_socket.close()
        except:
            pass
