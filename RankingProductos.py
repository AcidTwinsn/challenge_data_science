from tkinter.ttk import *
import pandas as pd
from tkinter import Canvas, StringVar, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg

class RankingProductos(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Ranking de Productos")
        self.geometry("1000x800")
        self.configure(bg="#c3f1fd")
        

        self.canvas = Canvas(self, bg = "#c3f1fd")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.interior = Frame(self.canvas, bg = "#c3f1fd")
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.label = Label(
            self.interior, 
            text="Elija el criterio de agrupacion", 
            font=("Arial", 14), 
            bg="#c3f1fd", 
            anchor="center"  # Centra el texto dentro del Label
        )
        diccionarioProductos = {}
        nombreTienda = ""
        
        
        
        self.label.pack(padx=10, pady=10)

        opciones = [("Productos más vendidos"),
                    ("Productos menos vendidos")]

        
        self.label = Label(
            self.interior,text=f"Seleccion: {opciones[0]}",
            font=("Arial", 12), 
            bg="#c3f1fd", 
            anchor="center"  # Centra el texto dentro del Label
        )
        self.label.pack(padx=10, pady=10)

        def selection():
            self.label.config(text=f"Seleccion: {orden.get()}")

        orden = StringVar(self.interior, f"{opciones[0]}")

        for opcion in opciones:
            Radiobutton(
                self.interior,
                text=opcion,
                variable=orden,
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
            command=lambda: obtener_ranking_productos(self, diccionarioProductos, nombreTienda, orden.get()),
        )
        self.button_procesar.pack(pady=10)

def obtener_ranking_productos(self, diccionarioProductos, nombreTienda, orden):
    url_Archivos = filedialog.askopenfilenames()
    if url_Archivos:
        cantidadArchivos = len(url_Archivos)
        messagebox.showinfo("Archivos Seleccionados", f"Se seleccionaron {cantidadArchivos} archivos", icon='info')
        for archivo in url_Archivos:
            nombreTienda = os.path.basename(archivo)
            tienda = fg.FuncionesGenerales.leer_archivo(archivo)
            if tienda is not None:
                Label(self.interior, text=f"Vista previa {nombreTienda}").pack(pady=10)

                diccionarioProductos[nombreTienda] = fg.FuncionesGenerales.obtener_ranking_prod(tienda, orden)

                data = diccionarioProductos[nombreTienda]
                crear_tabla(self, data)

            else:
                messagebox.showerror("Error", f"Error al procesar el archivo {nombreTienda}", icon='error') 

            self.button = Button(self.interior, text="Graficar Resultados", command=lambda v= diccionarioProductos[nombreTienda]: graficar_resultados(v))
            self.button.pack(pady=10)  
    else:
        messagebox.showwarning("Archivo Seleccionado", f"No se seleccionó ningún archivo.", icon='warning')

    return diccionarioProductos, nombreTienda

def crear_tabla(self, data):
    try:
        dataFrame = pd.DataFrame(data)
        frame = Frame(self.interior)
        frame.pack(fill="both", expand=True)
        table = Table(frame, dataframe=dataFrame, showtoolbar=True, showstatusbar=True, tablefmt='plain')
        table.autoResizeColumns()
        table.show() 
    except Exception as e:
        messagebox.showerror("Error", f"Error al crear el DataFrame: {e}", icon='error')

def graficar_resultados(tienda):
    producto = tienda['Producto']
    cantidad = tienda['cantidad_vendida']

    plt.plot(producto, cantidad, marker='o', linestyle='-', color='b')
    plt.xticks(rotation=70)
    plt.title('Ranking de Productos')
    plt.xlabel('Producto',rotation=70)
    plt.ylabel('Cantidad Vendida')
    plt.show()