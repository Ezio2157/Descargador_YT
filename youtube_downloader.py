import yt_dlp
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# Variable para almacenar la ruta de descarga
folder_path = ""


# Función para seleccionar la carpeta de destino
def seleccionar_carpeta():
    global folder_path
    folder_path = filedialog.askdirectory()
    carpeta_label.config(text=f"📂 Carpeta: {folder_path}")


# Función de actualización de progreso
def actualizar_progreso(d):
    if d['status'] == 'downloading':
        total_size = d.get('total_bytes') or d.get('total_bytes_estimate')
        downloaded = d.get('downloaded_bytes', 0)

        if total_size and downloaded:
            porcentaje = int((downloaded / total_size) * 100)
            progress_bar["value"] = porcentaje
            progress_label.config(text=f"Descargando... {porcentaje}% ({downloaded / 1024:.2f} KB / {total_size / 1024:.2f} KB)")
            root.update_idletasks()


# Función para descargar video o audio
def descargar(opcion):
    url = url_entry.get()

    if not url:
        messagebox.showerror("Error", "Por favor, ingresa una URL válida")
        return

    if not folder_path:
        messagebox.showerror("Error", "Selecciona una carpeta de destino")
        return

    # Opciones para yt-dlp
    opciones = {
        'format': 'bestaudio' if opcion == "audio" else 'best',
        'outtmpl': f"{folder_path}/%(title)s.%(ext)s",
        'progress_hooks': [actualizar_progreso],  # Agregar barra de progreso
    }

    try:
        progress_bar["value"] = 0
        progress_label.config(text="Iniciando descarga...")
        root.update_idletasks()

        with yt_dlp.YoutubeDL(opciones) as ydl:
            ydl.download([url])

        messagebox.showinfo("Éxito", "Descarga completada con éxito")
        progress_label.config(text="✅ Descarga finalizada")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")


# Crear la ventana principal
root = tk.Tk()
root.title("YouTube Downloader 🎥")
root.geometry("500x350")

# Etiqueta de URL
tk.Label(root, text="URL del Video:", font=("Arial", 12)).pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)

# Botón para seleccionar la carpeta
tk.Button(root, text="Seleccionar Carpeta", command=seleccionar_carpeta).pack(pady=5)
carpeta_label = tk.Label(root, text="📂 Carpeta: No seleccionada", font=("Arial", 10))
carpeta_label.pack(pady=5)

# Barra de progreso
progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_bar.pack(pady=10)
progress_label = tk.Label(root, text="Esperando descarga...", font=("Arial", 10))
progress_label.pack(pady=5)

# Botones de descarga
tk.Button(root, text="📹 Descargar Video", command=lambda: descargar("video"), bg="blue", fg="white").pack(pady=5)
tk.Button(root, text="🎵 Descargar Audio", command=lambda: descargar("audio"), bg="green", fg="white").pack(pady=5)

# Ejecutar la aplicación
root.mainloop()
