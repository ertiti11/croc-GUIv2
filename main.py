import os
import subprocess
import threading
import customtkinter as tk
from tkinter import filedialog

def recibir():
    recibir_frame.pack(fill='both', expand=True)
    enviar_frame.pack_forget()

def enviar():
    enviar_frame.pack(fill='both', expand=True)
    recibir_frame.pack_forget()

def ejecutar_comando_recibir():
    codigo = codigo_entry.get()
    # Exportar la variable de entorno CROC_SECRET
    os.environ["CROC_SECRET"] = codigo
    
    # Ejecutar el comando croc
    comando = "croc"
    threading.Thread(target=ejecutar_comando, args=(comando,)).start()

def seleccionar_archivo():
    archivo = filedialog.askopenfilename()
    if archivo:
        archivo_label.config(text=archivo)
        enviar_btn.config(state=tk.NORMAL, command=lambda: ejecutar_comando_enviar(archivo))

def ejecutar_comando_enviar(archivo):
    comando = f"croc send --text --yes {archivo}"
    threading.Thread(target=ejecutar_comando, args=(comando, True)).start()

def ejecutar_comando(comando, buscar_codigo=False):
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in iter(proceso.stdout.readline, ''):
        resultado_label.after(0, resultado_label.config, {'text': resultado_label.cget('text') + linea})
        if buscar_codigo and "Code is:" in linea:
            codigo = linea.split("Code is:")[1].strip()
            enviar_btn.config(state=tk.NORMAL, command=lambda: copy_to_clipboard(codigo))
            resultado_label.after(0, resultado_label.config, {'text': f"Código: {codigo}\n"})
            break
    proceso.stdout.close()
    proceso.wait()

def copy_to_clipboard(texto):
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()  # Importante para que se actualice el portapapeles

# Configuración de la ventana principal
root = tk.CTk()
root.title("Croc GUI")

# Frame principal para seleccionar entre recibir o enviar
main_frame = tk.CTkFrame(root)
main_frame.pack(fill='both', expand=True)

recibir_btn = tk.CTkButton(main_frame, text="Recibir", command=recibir)
recibir_btn.pack(side='left', fill='both', expand=True)

enviar_btn = tk.CTkButton(main_frame, text="Enviar", command=enviar)
enviar_btn.pack(side='right', fill='both', expand=True)

# Frame para la opción de recibir
recibir_frame = tk.CTkFrame(root)
tk.CTkLabel(recibir_frame, text="Introduce el código para recibir:").pack(pady=10)
codigo_entry = tk.CTkEntry(recibir_frame)
codigo_entry.pack(pady=10)
recibir_comando_btn = tk.CTkButton(recibir_frame, text="Recibir", command=ejecutar_comando_recibir)
recibir_comando_btn.pack(pady=10)

# Frame para la opción de enviar
enviar_frame = tk.CTkFrame(root)
seleccionar_btn = tk.CTkButton(enviar_frame, text="Seleccionar archivo", command=seleccionar_archivo)
seleccionar_btn.pack(pady=10)
archivo_label = tk.CTkLabel(enviar_frame, text="Ningún archivo seleccionado")
archivo_label.pack(pady=10)
enviar_btn = tk.CTkButton(enviar_frame, text="Enviar", state=tk.DISABLED)
enviar_btn.pack(pady=10)
copiar_codigo_btn = tk.CTkButton(enviar_frame, text="Copiar código al portapapeles", state=tk.DISABLED)
copiar_codigo_btn.pack(pady=10)

# Label para mostrar el resultado del comando croc
resultado_label = tk.CTkLabel(root, text="", wraplength=400, justify="left")
resultado_label.pack(pady=10)

# Iniciar la aplicación con la ventana principal visible
root.mainloop()
