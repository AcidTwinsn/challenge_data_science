from tkinter.ttk import *
import pandas as pd
from tkinter import Canvas, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg

class EnviosPromedio(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Envío promedio por Tienda")
        self.geometry("1000x800")
        self.configure(bg="#c3f1fd")
        Label(self, text="Envios promedio", font=("Arial", 14), bg="#c3f1fd").pack(pady=10)

        self.canvas = Canvas(self, bg="#c3f1fd")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.interior = Frame(self.canvas , bg = "#c3f1fd")
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")

        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        

        diccionarioTotales = {}
        nombreTienda = ""
        
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
            command=lambda: obtener_ingresos_totales(self, diccionarioTotales, nombreTienda),
        )
        self.button_procesar.pack(pady=10)

def obtener_ingresos_totales(self, diccionarioTotales, nombreTienda):
    url_Archivos = filedialog.askopenfilenames()
    if url_Archivos:
        cantidadArchivos = len(url_Archivos)
        messagebox.showinfo("Archivos Seleccionados", f"Se seleccionaron {cantidadArchivos} archivos", icon='info')
        for archivo in url_Archivos:
            nombreTienda = os.path.basename(archivo)
            tienda = fg.FuncionesGenerales.leer_archivo(archivo)
            if tienda is not None:
                Label(self.interior, text=f"Vista previa {nombreTienda}").pack(pady=10)
                                
                data = tienda
                crear_tabla(self, data)

                promedioEnvios = fg.FuncionesGenerales.calcular_prom_x_criterio(tienda, 'Costo de envío')
                Label(self.interior, text=f"El Costo promedio de Envíos de {nombreTienda} es: {promedioEnvios}").pack(pady=10)
                
                diccionarioTotales[nombreTienda] = promedioEnvios
            else:
                messagebox.showerror("Error", f"Error al procesar el archivo {nombreTienda}", icon='error')    
    else:
        messagebox.showwarning("Archivo Seleccionado", f"No se seleccionó ningún archivo.", icon='warning')

    if fg.FuncionesGenerales.contiene_elementos_dict(diccionarioTotales):   
        self.button = Button(self.interior, text="Graficar Resultados", command=lambda: graficar_resultados(diccionarioTotales))
        self.button.pack(pady=10) 

    return diccionarioTotales, nombreTienda

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

def graficar_resultados(dictTotales):
    tienda = list(dictTotales.keys())
    costo_prom_envios = list(dictTotales.values())   

    maximo = max(costo_prom_envios)
    colores = ['green' if costo != maximo else 'red' for costo in costo_prom_envios]
    

    plt.bar(tienda, costo_prom_envios, color=colores)

    plt.xlabel('Tiendas')
    plt.ylabel('Promedio de Costos de Envíos')
    plt.title(f'Costo promedio de Envíos por Tienda')
    plt.show()