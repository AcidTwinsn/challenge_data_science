from tkinter.ttk import Scrollbar
import pandas as pd
from tkinter import Canvas, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg

class AnalisisFacturacion(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.archivos_procesados = set()
        self.title("Análisis de Facturación")
        self.geometry("650x600")
        self.configure(bg="#c3f1fd")
        
        Label(self, text="Análisis de Facturación", font=("Arial", 14, "bold"), bg="#c3f1fd").pack(pady=10)

        # Canvas para scroll
        self.canvas = Canvas(self, bg="#c3f1fd")
        self.scrollbar = Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.interior = Frame(self.canvas, bg="#c3f1fd")
        self.canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        diccionarioTotales = {}
        nombreTienda = ""

        # Botones
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
            command=lambda: self.obtener_ingresos_totales(diccionarioTotales)
        )
        self.button_procesar.pack(pady=10)

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

        self.button_graficar = None

    def obtener_ingresos_totales(self, diccionarioTotales):
        url_archivos = filedialog.askopenfilenames(filetypes=[("Archivos CSV", "*.csv")])
        if not url_archivos:
            messagebox.showwarning("Archivo Seleccionado", "No se seleccionó ningún archivo.", icon='warning')
            return

        for archivo in url_archivos:
            if archivo in self.archivos_procesados:
                continue  # Evitar reprocesar archivos
            nombreTienda = os.path.basename(archivo)

            if not fg.FuncionesGenerales.validar_archivo_csv(self, nombreTienda):
                continue

            self.archivos_procesados.add(archivo)

            tienda = fg.FuncionesGenerales.leer_archivo(archivo)
            if tienda is not None:
                Label(self.interior, text=f"Vista previa: {nombreTienda}", bg="#c3f1fd").pack(pady=10)
                self.crear_tabla(tienda)

                total = fg.FuncionesGenerales.calcular_ingreso_total(tienda)
                Label(self.interior, text=f"Ingreso total de {nombreTienda}: {total}", bg="#c3f1fd").pack(pady=10)
                diccionarioTotales[nombreTienda] = total
            else:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {nombreTienda}", icon='error')

        if diccionarioTotales and self.button_graficar is None:
            self.button_graficar = Button(
                self.interior,
                text="Graficar Resultados",
                font=("Arial", 11),
                bg="white",
                fg="#333",
                relief="flat",
                padx=10,
                pady=8,
                activebackground="#00bfff",
                activeforeground="white",
                command=lambda: self.graficar_resultados(diccionarioTotales)
            )
            self.button_graficar.pack(pady=10)

    def crear_tabla(self, data):
        try:
            frame = Frame(self.interior, bg="#c3f1fd")
            frame.pack(fill="both", expand=True)
            table = Table(frame, dataframe=pd.DataFrame(data), showtoolbar=True, showstatusbar=True)
            table.autoResizeColumns()
            table.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la tabla: {e}")

    def graficar_resultados(self, dict_totales):
        tiendas = list(dict_totales.keys())
        ingresos = list(dict_totales.values())
        minimo = min(ingresos)
        colores = ['green' if ingreso > minimo else 'red' for ingreso in ingresos]

        plt.bar(tiendas, ingresos, color=colores)
        plt.xlabel('Tiendas')
        plt.ylabel('Ingresos Totales')
        plt.title('Ingresos por Tienda')
        plt.show()
