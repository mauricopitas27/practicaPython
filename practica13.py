# practiga13.py (Sin cambios funcionales, ya que tiene el callback correcto)
import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.receive_thread = None
        self.gui_callback = None  # Almacena la función de la GUI

    def set_gui_callback(self, callback_function):
        """Establece la función de la GUI a la que se llamará al recibir un mensaje."""
        self.gui_callback = callback_function

    def connect(self, nickname):
        """Conecta al servidor y envía el nickname."""
        try:
            self.client.connect((self.host, self.port))
            self.client.send(nickname.encode('utf-8'))
            self.connected = True
            # Iniciar hilo para recibir mensajes
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.daemon = True 
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def send_message(self, message):
        """Envía un mensaje (SOLO EL CONTENIDO) al servidor."""
        if self.connected:
            try:
                # Se envía solo el texto, el servidor se encarga de reestructurarlo.
                self.client.send(message.encode('utf-8')) 
            except:
                self.disconnect()

    def receive_messages(self):
        """Recibe mensajes del servidor en un hilo."""
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    if self.gui_callback:
                        self.gui_callback(message) # <-- Llama a la GUI con el mensaje del servidor
                else:
                    self.disconnect()
            except:
                self.disconnect()
                break

    def disconnect(self):
        """Desconecta del servidor."""
        if self.connected:
            self.connected = False
            try:
                self.client.close()
            except:
                pass
            if self.gui_callback:
                self.gui_callback("Sistema: Te has desconectado del servidor.")