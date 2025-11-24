import tkinter as tk
from tkinter import scrolledtext, messagebox
from practica13 import ChatClient  # Importa la lógica de negocio

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Informaticos - Cliente")
        self.root.geometry("500x600")
        self.root.configure(bg="#E0F7FA")  # Fondo azul claro

        # Instancia del cliente
        self.client = ChatClient()

        # Etiqueta de nickname
        self.nickname_label = tk.Label(root, text="Ingresa tu nombre :", bg="#E0F7FA", fg="#00796B", font=("Arial", 12, "bold"))
        self.nickname_label.pack(pady=10)

        # Entrada de nickname
        self.nickname_entry = tk.Entry(root, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
        self.nickname_entry.pack(pady=5)

        # Botón de conectar
        self.connect_button = tk.Button(root, text="Conectar", command=self.connect, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.connect_button.pack(pady=10)

        # Área de mensajes (scrolledtext para scroll)
        self.messages_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#F1F8E9", fg="#2E7D32", font=("Arial", 10))
        self.messages_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # Entrada de mensaje
        self.message_entry = tk.Entry(root, font=("Arial", 12), bg="#FFFFFF", fg="#000000")
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)  # Enviar con Enter

        # Botón de enviar
        self.send_button = tk.Button(root, text="Enviar", command=self.send_message, bg="#FF9800", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.send_button.pack(pady=10)

        # Estado inicial
        self.message_entry.config(state='disabled')
        self.send_button.config(state='disabled')

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
            self.display_message("Tú", message, "#1976D2")  # Azul para mensajes propios
            self.message_entry.delete(0, tk.END)

    def display_message(self, sender, message, color):
        self.messages_area.config(state='normal')
        self.messages_area.insert(tk.END, f"{sender}: {message}\n", (color,))
        self.messages_area.tag_config(color, foreground=color)
        self.messages_area.config(state='disabled')
        self.messages_area.see(tk.END)  # Auto-scroll

# Ejecutar la interfaz
if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()
