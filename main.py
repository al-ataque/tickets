import extractor
import save_data

import tkinter as tk
from tkinter import filedialog
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinterdnd2 import DND_FILES, TkinterDnD

class ArrastreArchivo(ttk.Frame):
    def __init__(self, master=None):
        super().__init__(master, padding=20)
        self.master = master
        self.pack(fill=tk.BOTH, expand=True)
        self.crear_widgets()

    def crear_widgets(self):
        # Título
        titulo = ttk.Label(self, text="Ticket data extractor", font=("Helvetica", 18, "bold"))
        titulo.pack(pady=(0, 20))

        # Área de arrastre
        self.area_arrastre = ttk.Frame(self, style="Custom.TFrame", padding=20)
        self.area_arrastre.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Texto del área de arrastre
        texto_arrastre = ttk.Label(self.area_arrastre, text="📁\nArrastra un archivo aquí\no usa el botón para seleccionar", 
                                   font=("Helvetica", 14), justify="center")
        texto_arrastre.pack(expand=True)

        # Configurar eventos de arrastrar y soltar
        self.area_arrastre.drop_target_register(DND_FILES)
        self.area_arrastre.dnd_bind('<<Drop>>', self.on_drop)

        # Frame para entrada y botón de selección
        frame_seleccion = ttk.Frame(self)
        frame_seleccion.pack(fill=X, pady=(20, 10))

        # Campo de entrada para la ruta del archivo
        self.ruta_archivo = ttk.Entry(frame_seleccion, width=40)
        self.ruta_archivo.pack(side=LEFT, expand=True, fill=X)

        # Botón para seleccionar archivo
        self.boton_seleccionar = ttk.Button(frame_seleccion, text="Seleccionar", command=self.seleccionar_archivo, bootstyle="info")
        self.boton_seleccionar.pack(side=RIGHT, padx=(10, 0))

        # Botón de guardar
        self.boton_guardar = ttk.Button(self, text="Guardar", command=self.guardar, bootstyle="success")
        self.boton_guardar.pack(pady=10)

        # Etiqueta de estado
        self.etiqueta_estado = ttk.Label(self, text="", font=("Helvetica", 10))
        self.etiqueta_estado.pack(pady=(10, 0))

    def on_drop(self, event):
        ruta_archivo = event.data
        if ruta_archivo:
            ruta_archivo = ruta_archivo.strip('{}')
            self.actualizar_ruta(ruta_archivo)

    def seleccionar_archivo(self):
        ruta_archivo = filedialog.askopenfilename()
        if ruta_archivo:
            self.actualizar_ruta(ruta_archivo)

    def actualizar_ruta(self, ruta):
        self.ruta_archivo.delete(0, tk.END)
        self.ruta_archivo.insert(0, ruta)
        self.etiqueta_estado.config(text="Archivo seleccionado", bootstyle="success")

    def guardar(self):
        ruta = self.ruta_archivo.get()
        if ruta:
            data = extractor.extract(ruta)
            save_data.save(data[0], data[1])
            print(f"Archivo guardado: {ruta}")
            self.etiqueta_estado.config(text="Archivo guardado exitosamente", bootstyle="success")
        else:
            self.etiqueta_estado.config(text="No se ha seleccionado ningún archivo", bootstyle="danger")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    root.title("Gestor de Archivos")
    root.geometry("500x400")
    
    style = ttk.Style(theme="cosmo")
    style.configure("Custom.TFrame", background="#f0f0f0", borderwidth=2, relief="groove")
    
    app = ArrastreArchivo(master=root)
    root.mainloop()