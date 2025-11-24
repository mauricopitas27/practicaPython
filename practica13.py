import socket
import threading

class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connected = False
        self.receive_thread = None

    def connect(self, nickname):
        """Conecta al servidor y envía el nickname."""
        try:
            self.client.connect((self.host, self.port))
            self.client.send(nickname.encode('utf-8'))
            self.connected = True
            # Iniciar hilo para recibir mensajes
            self.receive_thread = threading.Thread(target=self.receive_messages)
            self.receive_thread.start()
            return True
        except Exception as e:
            print(f"Error al conectar: {e}")
            return False

    def send_message(self, message):
        """Envía un mensaje al servidor."""
        if self.connected:
            try:
                self.client.send(message.encode('utf-8'))
            except:
                self.disconnect()

    def receive_messages(self):
        """Recibe mensajes del servidor en un hilo."""
        while self.connected:
            try:
                message = self.client.recv(1024).decode('utf-8')
                if message:
                    # Aquí se podría emitir una señal o callback para la interfaz
                    print(f"Mensaje recibido: {message}")  # Para depuración; en la interfaz se maneja visualmente
                else:
                    self.disconnect()
            except:
                self.disconnect()

    def disconnect(self):
        """Desconecta del servidor."""
        self.connected = False
        self.client.close()