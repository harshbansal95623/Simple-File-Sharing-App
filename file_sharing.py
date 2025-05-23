import socket
import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import os

# Function to get local IP address
def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "Unable to get IP"

# Function to send a file
def send_file():
    file_path = filedialog.askopenfilename()
    if not file_path:
        return
    
    receiver_ip = receiver_ip_entry.get()
    if not receiver_ip:
        messagebox.showerror("Error", "Please enter receiver IP")
        return
    
    try:
        s = socket.socket()
        s.connect((receiver_ip, 5000))
        
        file_name = os.path.basename(file_path).encode()
        file_size = os.path.getsize(file_path)
        
        s.sendall(len(file_name).to_bytes(4, 'big'))  # Send filename length
        s.sendall(file_name)  # Send filename
        s.sendall(file_size.to_bytes(8, 'big'))  # Send file size
        
        with open(file_path, 'rb') as f:
            while chunk := f.read(4096):
                s.sendall(chunk)
        
        messagebox.showinfo("Success", "File sent successfully!")
        s.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send file: {e}")

# Function to receive a file
def receive_file():
    s = socket.socket()
    s.bind(("0.0.0.0", 5000))
    s.listen(1)
    
    conn, addr = s.accept()
    messagebox.showinfo("Connected", f"Receiving file from {addr[0]}")
    
    file_name_length = int.from_bytes(conn.recv(4), 'big')  # Read filename length
    file_name = conn.recv(file_name_length).decode()  # Read filename
    file_size = int.from_bytes(conn.recv(8), 'big')  # Read file size
    
    file_path = filedialog.asksaveasfilename(initialfile=file_name, defaultextension=os.path.splitext(file_name)[1], filetypes=[("All Files", ".")])
    if not file_path:
        conn.close()
        return
    
    received_size = 0
    with open(file_path, 'wb') as f:
        while received_size < file_size:
            data = conn.recv(4096)
            if not data:
                break
            f.write(data)
            received_size += len(data)
    
    if received_size == file_size:
        messagebox.showinfo("Success", "File received successfully!")
    else:
        messagebox.showerror("Error", "File transfer incomplete!")
    
    conn.close()
    s.close()

# Start the receiver thread
def start_receiver():
    threading.Thread(target=receive_file, daemon=True).start()
    messagebox.showinfo("Receiver", "Waiting for file...")

# GUI Setup
root = tk.Tk()
root.title("Simple File Sharing")
root.geometry("400x250")

tk.Label(root, text="Your IP Address:").pack()
local_ip_label = tk.Label(root, text=get_local_ip(), font=("Arial", 12, "bold"))
local_ip_label.pack()

tk.Label(root, text="Receiver IP:").pack()
receiver_ip_entry = tk.Entry(root)
receiver_ip_entry.pack()

tk.Button(root, text="Send File", command=send_file).pack(pady=10)

tk.Button(root, text="Receive File", command=start_receiver).pack(pady=10)

root.mainloop()

# Usage Guide:
# 1. Run this script on both sender and receiver machines.
# 2. On the receiver's machine, click "Receive File" to start listening.
# 3. On the sender's machine, enter the receiver's IP and click "Send File" to select and send a file.
# 4. The receiver will be prompted to save the file with its original name and extension.
# 5. The program ensures full file integrity by verifying received file size.