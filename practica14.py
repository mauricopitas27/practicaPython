# practica14.py (Código final, sin cambios)
import tkinter as tk
from tkinter import scrolledtext, messagebox
from practica13 import ChatClient 

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Informaticos - Cliente")
        self.root.geometry("500x600")
        self.root.configure(bg="#E0F7FA")

        self.client = ChatClient()
        self.client.set_gui_callback(self.handle_server_message) 

        # --- 1. Widgets Superiores (Nickname y Conectar) ---
        self.nickname_label = tk.Label(root, text="Ingresa tu nombre :", bg="#E0F7FA", fg="#00796B", font=("Arial", 12, "bold"))
        self.nickname_label.pack(pady=10)

        self.nickname_entry = tk.Entry(root, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
        self.nickname_entry.pack(pady=5)

        self.connect_button = tk.Button(root, text="Conectar", command=self.connect, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.connect_button.pack(pady=10)

        # --- 2. Área de Mensajes ---
        self.messages_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#F1F8E9", fg="#2E7D32", font=("Arial", 10))
        self.messages_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # --- 3. Entrada de Mensaje ---
        self.message_entry = tk.Entry(root, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message) 

        # --- 4. Botón de Enviar ---
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message, bg="#FF9800", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.send_button.pack(pady=10) 

        # --- 5. Estado inicial ---
        self.message_entry.config(state='disabled')
        self.send_button.config(state='disabled')
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def connect(self):
        nickname = self.nickname_entry.get().strip()
        if not nickname:
            messagebox.showerror("Error", "Ingresa un nickname válido.")
            return

        if self.client.connect(nickname):
            self.nickname_label.config(text=f"Conectado como: {nickname}")
            self.nickname_entry.config(state='disabled')
            self.connect_button.config(state='disabled')
            self.message_entry.config(state='normal')
            self.send_button.config(state='normal')
            self.display_message("Sistema", "Conectado al chat. ¡Empieza a chatear!", "#00796B")
        else:
            messagebox.showerror("Error", "No se pudo conectar al servidor.")

    def send_message(self, event=None):
        message = self.message_entry.get().strip()
        if message:
            self.client.send_message(message)
            self.message_entry.delete(0, tk.END)

    def handle_server_message(self, message):
        """Procesa el mensaje recibido del servidor y lo programa para mostrarse."""
        
        if message.startswith("Sistema:"):
            # Mensajes del sistema
            content = message.replace("Sistema: ", "").strip()
            self.root.after(0, self.display_message, "Sistema", content, "#00796B")
            
        elif ":" in message:
            try:
                # Separar emisor y contenido
                sender, content = message.split(":", 1)
                sender = sender.strip()
                content = content.strip()
                
                # Color diferente para el usuario local vs. otros usuarios
                current_nickname = self.nickname_entry.get().strip()
                if sender == current_nickname:
                    color = "#1976D2" # Azul para mensajes propios
                    sender = "Tú"
                else:
                    color = "#FF9800" # Naranja para otros usuarios
                
                self.root.after(0, self.display_message, sender, content, color)
            except ValueError:
                self.root.after(0, self.display_message, "Error", message, "red")
        else:
            # Mensaje simple sin formato de emisor
            self.root.after(0, self.display_message, "Sistema", message, "#00796B")

    def display_message(self, sender, message, color):
        """Inserta el mensaje en el área de texto de la GUI (se ejecuta en el hilo principal)."""
        self.messages_area.config(state='normal')
        self.messages_area.insert(tk.END, f"{sender}: {message}\n", (color,))
        self.messages_area.tag_config(color, foreground=color)
        self.messages_area.config(state='disabled')
        self.messages_area.see(tk.END) 

    def on_closing(self):
        """Maneja la desconexión del cliente al cerrar la ventana."""
        if self.client.connected:
            self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()