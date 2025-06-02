# Simple-File-Sharing-App
Simple File Sharing App is a Python GUI tool that lets you send and receive files over a local network using sockets. It shows your IP, lets you enter the receiver’s IP, and transfers files securely with file size verification. Easy, fast, and cross-platform with a user-friendly interface.

A lightweight Python GUI application to send and receive files over a local network using sockets. Built with Tkinter for easy use.

# 🛡️ Features

Automatically detects and displays your local IP address

Send files to another machine by entering their IP address

Receive files with a simple "Receive File" button

File integrity verification by checking file size

User-friendly GUI with progress notifications

Runs on Windows, Linux, and macOS (Python required)

# 🛠 Requirements

Python 3.x

Tkinter (usually included with Python)

No external libraries required

# 📦 Installation & Usage

Clone the repository:

```bash
git clone https://github.com/yourusername/simple-file-sharing.git
cd simple-file-sharing
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

Run the script:

```bash
python3 file_sharing.py
```

# Usage

On the receiver’s machine:

Launch the app and click "Receive File" to start listening for incoming files.

The app will display your local IP address.

On the sender’s machine:

Enter the receiver’s IP address in the input box.

Click "Send File" and select the file you want to send.

# File transfer:

The receiver will be prompted to choose where to save the file.

After the transfer completes, you will see a success or error notification.

# How it works

Uses TCP sockets on port 5000 for file transfer.

Sends metadata (filename length, filename, and filesize) before the actual file data.

Transfers file data in chunks to handle large files efficiently.

Runs the receiver in a separate thread to keep the GUI responsive.

# Notes

Make sure both machines are on the same local network and can reach each other’s IP on port 5000.

Firewalls may need to be configured to allow traffic on port 5000.

# License
```
This project is open-source and free to use.
