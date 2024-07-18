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
    if os.name == "linux":
        os.environ["CROC_SECRET"] = codigo
        # Ejecutar el comando croc
        comando = "croc"
        threading.Thread(target=ejecutar_comando, args=(comando,)).start()
    if os.name == "nt":
        comando = f"croc --yes {codigo}"
        threading.Thread(target=ejecutar_comando, args=(comando,)).start()

# def seleccionar_archivo():
#     archivo = filedialog.askopenfilename()
#     if archivo:
#         archivo_label.configure(text=archivo)
#         enviar_btn.configure(state=tk.NORMAL, command=lambda: ejecutar_comando_enviar(archivo))

def ejecutar_comando_enviar(codigo):
    texto = text_entry.get()
    codigo = codigo.replace('"', '\\"').replace("'", "\\'")
    comando = f"croc send --text {codigo}"
    threading.Thread(target=ejecutar_comando, args=(comando, True)).start()

def ejecutar_comando_recibir():
    codigo = codigo_entry.get()
    comando = f"croc --yes {codigo}"
    
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
#     connecting...

# securing channel...

# Receiving text message (6 B)



# Receiving (<-127.0.0.1:58743)

# holaaa
    for linea in iter(proceso.stdout.readline, ''):
        print(linea[0])

    proceso.stdout.close()
    proceso.wait()

    


def ejecutar_comando(comando, buscar_codigo=False):
    proceso = subprocess.Popen(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    for linea in iter(proceso.stdout.readline, ''):
        resultado_label.after(0, resultado_label.configure, {'text': resultado_label.cget('text') + linea})
        # try:
        #     print(linea.split("Code is:")[1].strip() if "Code is:" in linea and buscar_codigo else None)
        # except IndexError:
        #     print(None)

        if buscar_codigo and "Code is:" in linea:
            codigo = linea.split("Code is:")[1].strip()
            # print(codigo)
            resultado_label.configure(text=f"Código: {codigo}\n")
            copiar_codigo_btn.configure(command=copy_to_clipboard(codigo))
            break
    if 'Sending' in proceso.stdout.read():
        resultado_label.configure(text="texto enviado✅")
        codigo_entry.delete(0, tk.END)
        print("Enviando archivo...")
    print(proceso.stdout.read())
    proceso.stdout.close()
    proceso.wait()

def copy_to_clipboard(texto):
    print("Copiando código al portapapeles...")
    root.clipboard_clear()
    root.clipboard_append(texto)
    root.update()  # Importante para que se actualice el portapapeles
    print("Código copiado al portapapeles")

# configureuración de la ventana principal
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
text_entry = tk.CTkEntry(enviar_frame)
text_entry.pack(pady=10)
enviar_btn = tk.CTkButton(enviar_frame, text="Enviar", command=lambda: ejecutar_comando_enviar(text_entry.get()))
enviar_btn.pack(pady=10)
copiar_codigo_btn = tk.CTkButton(enviar_frame, text="Copiar código al portapapeles", command=lambda: copy_to_clipboard(resultado_label.cget('text')))
copiar_codigo_btn.pack(pady=10)
estado_envio_label = tk.CTkLabel(enviar_frame, text="no enviado")
# Label para mostrar el resultado del comando croc
resultado_label = tk.CTkLabel(root, text="codig:", wraplength=400, justify="left")
resultado_label.pack(pady=10)

# Iniciar la aplicación con la ventana principal visible
root.mainloop()
