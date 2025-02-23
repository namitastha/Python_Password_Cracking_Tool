import zipfile
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from termcolor import colored
from PIL import Image, ImageTk

def extract_zip(zip_path, wordlist_file, log_text):
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_file:
            with open(wordlist_file, 'r', encoding='utf-8', errors='ignore') as file:
                for line in file:
                    password = line.strip()
                    log_text.insert(tk.END, f"[?] Trying password: '{password}'\n")
                    log_text.see(tk.END)
                    log_text.update_idletasks()
                    try:
                        zip_file.extractall(pwd=password.encode('utf-8'))
                        log_text.insert(tk.END, colored(f"[+] Password found: {password}\n", 'green'))
                        messagebox.showinfo("Success", f"Password cracked: {password}")
                        return
                    except (RuntimeError, zipfile.BadZipFile):
                        continue
            log_text.insert(tk.END, "[-] Password not found.\n")
    except FileNotFoundError:
        messagebox.showerror("Error", "ZIP file or wordlist not found.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def start_cracking(zip_path, wordlist_path, log_text):
    if not zip_path or not wordlist_path:
        messagebox.showwarning("Input Error", "Please select both ZIP file and wordlist.")
        return
    log_text.delete(1.0, tk.END)
    thread = threading.Thread(target=extract_zip, args=(zip_path, wordlist_path, log_text))
    thread.start()

def create_gui():
    root = tk.Tk()
    root.title("🔥 ZIP Password Cracker 🔥")
    root.geometry("700x600")
    root.configure(bg="#222222")
    
    try:
        img = Image.open("header.png")
        img = img.resize((700, 150))
        img = ImageTk.PhotoImage(img)
        img_label = tk.Label(root, image=img, bg="#222222")
        img_label.image = img
        img_label.pack(pady=5)
    except:
        tk.Label(root, text="🔥 ZIP Password Cracker 🔥", font=("Helvetica", 24, "bold"), fg="#FFD700", bg="#222222").pack(pady=10)
    
    zip_label = tk.Label(root, text="Select ZIP File:", fg="white", bg="#222222")
    zip_label.pack(anchor='w', padx=10)
    zip_entry = tk.Entry(root, width=60)
    zip_entry.pack(pady=5)
    tk.Button(root, text="Browse", command=lambda: zip_entry.insert(0, filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")]))).pack()
    
    wordlist_label = tk.Label(root, text="Select Wordlist File:", fg="white", bg="#222222")
    wordlist_label.pack(anchor='w', padx=10, pady=(10, 0))
    wordlist_entry = tk.Entry(root, width=60)
    wordlist_entry.pack(pady=5)
    tk.Button(root, text="Browse", command=lambda: wordlist_entry.insert(0, filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]))).pack()
    
    start_button = tk.Button(root, text="Start Cracking", bg="#FF4500", fg="white", font=("Helvetica", 14, "bold"), command=lambda: start_cracking(zip_entry.get(), wordlist_entry.get(), log_text))
    start_button.pack(pady=10)
    
    log_text = scrolledtext.ScrolledText(root, height=15, width=80, bg="#333333", fg="lightgreen", font=("Courier", 10))
    log_text.pack(pady=5)
    
    tk.Label(root, text="© 2024 Namita Shrestha", fg="lightgray", bg="#222222").pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    create_gui()
