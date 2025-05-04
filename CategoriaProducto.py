from tkinter.ttk import *
import numpy as np
import pandas as pd
from tkinter import Canvas, IntVar, StringVar, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg
from tkinter.ttk import Radiobutton

class CategoriaProducto(Toplevel):
    def __init__(self, master=None):
        
        super().__init__(master)
        self.title("Categoría de Producto")
        self.geometry("800x600")
        self.configure(bg="#c3f1fd")

        self.label = Label(
            self, 
            text="Elija el criterio de agrupacion", 
            font=("Arial", 14), 
            bg="#c3f1fd", 
            anchor="center"  # Centra el texto dentro del Label
        )
        self.label.pack(padx=10, pady=10)

        

        self.canvas = Canvas(self,bg="#c3f1fd")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.interior = Frame(self.canvas, bg = "#c3f1fd")
        
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        ventas_por_categoria = {}
        nombreTienda = ""

        opciones = [("Categoría del Producto"), 
                    ("Producto"), 
                    ("Vendedor"),
                    ("Costo de envío"),
                    ("Fecha de Compra"),
                    ("Lugar de Compra"),
                    ("Cantidad"),
                    ("Calificación"),
                    ("Método de pago"),
                    ("Cantidad de cuotas")]
        
        self.label = Label(
            self.interior,text=f"Seleccion: {opciones[0]}",
            font=("Arial", 12), 
            bg="#c3f1fd", 
            anchor="center"  # Centra el texto dentro del Label
        )
        self.label.pack(padx=10, pady=10)
        
        self.label = Label(
            self.interior, 
            text="Elija el criterio de agrupacion", 
            font=("Arial", 14), 
            bg="#c3f1fd", 
            anchor="center"  # Centra el texto dentro del Label
        )
        self.label.pack(padx=10, pady=10)

        

        def selection():
            self.label.config(text=f"Seleccion: {criterio.get()}")

        criterio = StringVar(self.interior, f"{opciones[0]}")
        
        style = Style(self.canvas) 
        style.configure("TRadiobutton", background = "#c3f1fd", foreground = "black")
        for opcion in opciones:
            Radiobutton(
                self.interior,
                text=opcion,
                variable=criterio,
                value=opcion,
                command=selection,
                
                

            ).pack(anchor="w", padx=10, pady=5)
        

        self.button_cerrar = Button(
            self.interior,
            text="Cerrar",
            font=("Arial", 11),
            bg="white",
            fg="#333",
            relief="flat",
            padx=10,
            pady=8,
            activebackground="#f00",
            activeforeground="white",
            command=lambda: fg.FuncionesGenerales.cerrar_ventana(self)
        )
        self.button_cerrar.pack(pady=10)

        self.button_procesar = Button(
            self.interior,
            text="Seleccionar Archivos a Procesar",
            font=("Arial", 11),
            bg="white",
            fg="#333",
            relief="flat",
            anchor="center",
            padx=10,
            pady=8,
            activebackground="#00bfff",
            activeforeground="white",
            command=lambda: obtener_agrupado_categoria(self, ventas_por_categoria, nombreTienda, criterio.get())
        )
        self.button_procesar.pack(pady=10)

def obtener_agrupado_categoria(self, ventas_por_categoria, nombreTienda, criterio):
    url_Archivos = filedialog.askopenfilenames()
    if url_Archivos:
        cantidadArchivos = len(url_Archivos)
        messagebox.showinfo("Archivos Seleccionados", f"Se seleccionaron {cantidadArchivos} archivos. El criterio de agrupacion es {criterio}", icon='info')
        for archivo in url_Archivos:
            nombreTienda = os.path.basename(archivo)
            tienda = fg.FuncionesGenerales.leer_archivo(archivo)
            if tienda is not None:
                Label(self.interior, text=f"Vista previa {nombreTienda}").pack(pady=10)                
                if criterio == "":
                    messagebox.showwarning("Criterio de Agrupación", "Por favor, ingrese un criterio de agrupación.", icon='warning')
                    return
                ventas_por_categoria[nombreTienda] = fg.FuncionesGenerales.sumIng_TotVen_x_criterio(tienda, criterio)
                
                data = ventas_por_categoria[nombreTienda]
                crear_tabla(self, data)
            else:
                messagebox.showerror("Error", f"Error al procesar el archivo {nombreTienda}", icon='error')  
             
            self.button = Button(self.interior, text="Graficar Resultados", command=lambda v= ventas_por_categoria[nombreTienda]: graficar_resultados_pie(v, criterio))
            self.button.pack(pady=10)                  
    else:
        messagebox.showwarning("Archivo Seleccionado", f"No se seleccionó ningún archivo.", icon='warning')

    return ventas_por_categoria, nombreTienda

def crear_tabla(self, data ):
    try:
        dataFrame = pd.DataFrame(data)
        frame = Frame(self.interior)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        table = Table(frame, dataframe=dataFrame, showtoolbar=True, showstatusbar=True, tablefmt='plain')
        table.autoResizeColumns()
        table.show() 
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el DataFrame: {e}", icon='error')

def graficar_resultados_pie(tienda, criterio): 
    categorias = tienda[criterio]
    ingresos = tienda['ingreso_total']
    plt.pie(ingresos, labels=categorias, autopct="%0.1f %%")
    plt.axis("equal")
    plt.show()