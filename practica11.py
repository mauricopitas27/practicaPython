import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading
from datetime import datetime

class ChatClient:
    def _init_(self, root):
        self.root = root
        self.root.title("Chat Client")
        self.root.geometry("500x600")
        self.root.configure(bg="#f0f0f0")
        
        self.socket = None
        self.username = None
        self.connected = False
        
        # Username frame
        self.username_frame = tk.Frame(root, bg="#f0f0f0")
        self.username_frame.pack(pady=10)
        
        tk.Label(self.username_frame, text="Username:", bg="#f0f0f0", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.username_entry = tk.Entry(self.username_frame, font=("Arial", 10), width=20)
        self.username_entry.pack(side=tk.LEFT, padx=5)
        
        self.connect_btn = tk.Button(self.username_frame, text="Connect", command=self.connect_to_server, bg="#4CAF50", fg="white", font=("Arial", 10))
        self.connect_btn.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(root, text="Disconnected", fg="red", bg="#f0f0f0", font=("Arial", 9))
        self.status_label.pack()
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(root, height=20, width=60, font=("Arial", 10), state=tk.DISABLED, wrap=tk.WORD)
        self.chat_display.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Configure tags for message styling
        self.chat_display.tag_config("own_message", foreground="#0066cc", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("other_message", foreground="#009900", font=("Arial", 10, "bold"))
        self.chat_display.tag_config("system", foreground="#666666", font=("Arial", 9, "italic"))
        self.chat_display.tag_config("timestamp", foreground="#999999", font=("Arial", 8))
        
        # Message input frame
        self.input_frame = tk.Frame(root, bg="#f0f0f0")
        self.input_frame.pack(pady=10, padx=10, fill=tk.X)
        
        self.message_input = tk.Entry(self.input_frame, font=("Arial", 10), state=tk.DISABLED)
        self.message_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.message_input.bind("<Return>", self.send_message)
        
        self.send_btn = tk.Button(self.input_frame, text="Send", command=self.send_message, bg="#2196F3", fg="white", font=("Arial", 10), state=tk.DISABLED)
        self.send_btn.pack(side=tk.LEFT, padx=5)
    
    def connect_to_server(self):
        username = self.username_entry.get().strip()
        
        if not username:
            messagebox.showerror("Error", "Please enter a username")
            return
        
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect(("localhost", 5000))  # Adjust IP and port as needed
            
            self.username = username
            self.socket.send(username.encode('utf-8'))
            
            self.connected = True
            self.status_label.config(text=f"Connected as {username}", fg="green")
            self.username_entry.config(state=tk.DISABLED)
            self.connect_btn.config(state=tk.DISABLED)
            self.message_input.config(state=tk.NORMAL)
            self.send_btn.config(state=tk.NORMAL)
            
            self.display_system_message(f"Connected to server as {username}")
            
            # Start receiving messages in a separate thread
            receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
            receive_thread.start()
            
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect: {str(e)}")
            self.connected = False
    
    def send_message(self, event=None):
        if not self.connected:
            messagebox.showwarning("Warning", "Not connected to server")
            return
        
        message = self.message_input.get().strip()
        
        if not message:
            return
        
        try:
            self.socket.send(message.encode('utf-8'))
            self.display_own_message(message)
            self.message_input.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Send Error", f"Failed to send message: {str(e)}")
            self.connected = False
    
    def receive_messages(self):
        while self.connected:
            try:
                message = self.socket.recv(1024).decode('utf-8')
                if message:
                    self.display_other_message(message)
                else:
                    break
            except Exception as e:
                self.connected = False
                self.display_system_message("Disconnected from server")
                break
    
    def display_own_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"You: ", "own_message")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def display_other_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] ", "timestamp")
        self.chat_display.insert(tk.END, f"Other: ", "other_message")
        self.chat_display.insert(tk.END, f"{message}\n")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def display_system_message(self, message):
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f">>> {message}\n", "system")
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)

if _name_ == "_main_":
    root = tk.Tk()
    client = ChatClient(root)
    root.mainloop()