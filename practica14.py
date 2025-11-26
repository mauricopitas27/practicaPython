# practica14.py
import tkinter as tk
from tkinter import scrolledtext, messagebox
from practica13 import ChatClient

class ChatGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Informáticos - Cliente")
        self.root.geometry("520x640")
        self.root.configure(bg="#E0F7FA")

        self.client = ChatClient()
        self.client.set_gui_callback(self.handle_server_message)

        # --- Nickname / Conectar ---
        self.nickname_label = tk.Label(root, text="Ingresa tu nombre :", bg="#E0F7FA", fg="#00796B", font=("Arial", 12, "bold"))
        self.nickname_label.pack(pady=10)

        self.nickname_entry = tk.Entry(root, font=("Arial", 12))
        self.nickname_entry.pack(pady=5)

        self.connect_button = tk.Button(root, text="Conectar", command=self.connect, bg="#4CAF50", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.connect_button.pack(pady=8)

        # --- Area mensajes ---
        self.messages_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', bg="#F1F8E9", fg="#2E7D32", font=("Arial", 10))
        self.messages_area.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        # --- Entrada mensaje ---
        self.message_entry = tk.Entry(root, font=("Arial", 12))
        self.message_entry.pack(pady=5, padx=10, fill=tk.X)
        self.message_entry.bind("<Return>", self.send_message)

        # --- Botones ---
        btn_frame = tk.Frame(root, bg="#E0F7FA")
        btn_frame.pack(pady=8)

        self.send_button = tk.Button(btn_frame, text="Enviar", command=self.send_message, bg="#FF9800", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.send_button.grid(row=0, column=0, padx=6)

        self.history_button = tk.Button(btn_frame, text="Ver Historial", command=self.show_history, bg="#0288D1", fg="#FFFFFF", font=("Arial", 12, "bold"))
        self.history_button.grid(row=0, column=1, padx=6)

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
        if message.startswith("Sistema:"):
            content = message.replace("Sistema:", "").strip()
            self.root.after(0, self.display_message, "Sistema", content, "#00796B")
        elif ":" in message:
            try:
                sender, content = message.split(":", 1)
                sender = sender.strip()
                content = content.strip()
                current_nickname = self.nickname_entry.get().strip()
                color = "#1976D2" if sender == current_nickname else "#FF9800"
                if sender == current_nickname:
                    sender = "Tú"
                self.root.after(0, self.display_message, sender, content, color)
            except ValueError:
                self.root.after(0, self.display_message, "Error", message, "red")
        else:
            self.root.after(0, self.display_message, "Sistema", message, "#00796B")

    def display_message(self, sender, message, color="#000000"):
        self.messages_area.config(state='normal')
        self.messages_area.insert(tk.END, f"{sender}: {message}\n", (color,))
        self.messages_area.tag_config(color, foreground=color)
        self.messages_area.config(state='disabled')
        self.messages_area.see(tk.END)

    def show_history(self):
        history = self.client.get_history()
        if not history:
            self.display_message("Sistema", "No hay historial o no fue posible obtenerlo.", "#00796B")
            return

        self.display_message("Sistema", "--- Historial del Chat ---", "#00796B")
        for msg in history:   # ← ESTE FOR DEBE ESTAR DENTRO DE LA FUNCIÓN
            sender = msg.get("nombre_usuario", "Desconocido")
            text = msg.get("mensaje", "")
            fecha = msg.get("fecha_hora", "")

            self.display_message(f"{sender} ({fecha})", text, "#6A1B9A")


    def on_closing(self):
        if self.client.connected:
            self.client.disconnect()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    gui = ChatGUI(root)
    root.mainloop()
