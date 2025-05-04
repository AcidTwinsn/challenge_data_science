from tkinter.ttk import *
import pandas as pd
from tkinter import Canvas, PhotoImage, StringVar, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg

class ClasificacionPromedio(Toplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Clasificación Promedio")
        self.geometry("800x600")
        color_fondo = "#c3f1fd"

        #Estilos de fuentes
        fuente_titulo = ("Arial", 14)
        fuente_subtitulo = ("Arial", 12, "italic")
        fuente_texto = ("Arial", 11)

        #Propiedades de iconos y tamaño de botones
        ancho_icono = 32
        largo_icono = 32

        #variables generales
        diccionarioPromedios = {}
        nombreTienda = ""

        #Propiedades de canvas
        canvas = Canvas(self, width=800, height=600, bg=color_fondo)
        #scrollbar vertical para desplazamiento
        scroll_vertical = Scrollbar(self, orient="vertical", command=canvas.yview)
        scroll_vertical.pack(side="right", fill="y")
        #scrollbar horizontal para desplazamiento
        scroll_horizontal = Scrollbar(self, orient="horizontal", command=canvas.xview)
        scroll_horizontal.pack(side="bottom", fill="x")
        #se agregan el objeto canvas junto con las barras de desplazamiento
        canvas.pack(side="left", fill="both", expand=True)
        canvas.configure(yscrollcommand=scroll_vertical.set, xscrollcommand=scroll_horizontal)
        #se agrega objeto canvas al frame
        self.interior = Frame(canvas)
        #se crea la ventana canvas con el frame
        canvas.create_window((0, 0), window=self.interior, anchor="nw")
        self.interior.config(bg=color_fondo)
        self.interior.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        #se agregan componentes de titulos al frame
        Label(self.interior, text="Bienvenido al Módulo para obtener la Clasificacion Promedio", font=fuente_titulo, bg=color_fondo).pack(anchor="w", padx=10, pady=10)
        Label(self.interior, text="Seleccione la categoría por la cual desde obtener el Promedio", font=fuente_subtitulo, bg=color_fondo).pack(anchor="w", padx=10, pady=10)

        #Menu de opciones para seleccion de categoria
        opciones = [("Cantidad de cuotas"),
                    ("Precio"),
                    ("Calificación"),
                    ("Costo de envío")]

        self.label = Label(self.interior, font=fuente_texto, bg=color_fondo, text=f"Seleccion: {opciones[0]}",)
        #self.label = Label(self.interior,text=f"Seleccion: {opciones[0]}",)
        self.label.pack(anchor="w", padx=10, pady=10)

        def selection():
            self.label.config(text=f"Seleccion: {criterio.get()}")

        criterio = StringVar(self.interior, f"{opciones[0]}")

        #Asignando propiedades a los objetos RadioButton 
        style = Style(self.interior) 
        style.configure("TRadiobutton", background = color_fondo, 
				foreground = "black", font = fuente_texto) 
        
        for opcion in opciones:
            Radiobutton(
                self.interior,
                text=opcion,
                variable=criterio,
                value=opcion,
                command=selection,
            ).pack(anchor="w", padx=10, pady=5)
        
        #Bloque para alinear compomentes de tablas de resultados  
        contenedor_tablas = Frame(self.interior, bg=color_fondo)
        contenedor_tablas.pack(side="bottom", fill="x", pady=10)
        
        #Bloque para alinear compomentes de cerrar sesión
        contenedor_btn_salir = Frame(self.interior, bg=color_fondo)
        contenedor_btn_salir.pack(side="bottom", fill="x", pady=10)
        
        #Etiqueta y Boton para cerrar sesion o salir
        lbl_salir = Label(
                        contenedor_btn_salir,
                        text="Salir",
                        font=fuente_texto,
                        bg=color_fondo,
                        fg="#333",
                        relief="flat",
                        justify="left"
        )
        lbl_salir.pack(side="left", padx=10)
        
        #Imagen para el boton
        icono_btn_salir = PhotoImage(file="Recursos/iconos/x32/salir.png")
        btn_salir = Button(contenedor_btn_salir, 
                        image=icono_btn_salir, 
                        bg=color_fondo, 
                        width=ancho_icono, 
                        height=largo_icono,
                        relief="flat",
                        command=lambda: fg.FuncionesGenerales.cerrar_ventana(self))
        btn_salir.image = icono_btn_salir
        btn_salir.pack(side="right", padx=300)
        
        #Bloque para alinear compomentes de procesar tiendas
        contenedor_btn_archivo = Frame(self.interior, bg=color_fondo)
        contenedor_btn_archivo.pack(side="bottom", fill="x", pady=10)

        #Etiqueta y Boton para seleccionar las Tiendas a procesar
        lbl_archivo = Label(
                contenedor_btn_archivo,
                text="Seleccione Tiendas a analizar",
                font=fuente_texto,
                bg=color_fondo,
                fg="#333",
                relief="flat",
                justify="left"
        )
        lbl_archivo.pack(side="left", padx=10)

        icono_btn_archivo = PhotoImage(file="Recursos/iconos/x32/abrir_archivos.png")
        btn_archivo = Button(contenedor_btn_archivo,
                             image=icono_btn_archivo,
                             bg=color_fondo,
                             width=ancho_icono,
                             height=largo_icono,
                             relief="flat",
                             command=lambda: ClasificacionPromedio.obtener_promedio_categoria(contenedor_tablas, 
                                                                        diccionarioPromedios, 
                                                                        nombreTienda, 
                                                                        criterio.get(), 
                                                                        fuente_subtitulo, 
                                                                        color_fondo))
        btn_archivo.image = icono_btn_archivo
        btn_archivo.pack(side="right", padx=300)        

    def obtener_promedio_categoria(self, diccionarioPromedios, nombreTienda, criterio, fuente, color_fondo):
        url_Archivos = filedialog.askopenfilenames()
        if url_Archivos:
            cantidadArchivos = len(url_Archivos)
            messagebox.showinfo("Archivos Seleccionados", f"Se seleccionaron {cantidadArchivos} archivos", icon='info')
            for archivo in url_Archivos:
                nombreTienda = os.path.basename(archivo)
                #valida si el archivo cargado no es csv, de ser así no se procesa
                if not fg.FuncionesGenerales.validar_archivo_csv(self, nombreTienda):                
                    continue
                #si el archivo cargado es csv procesa su lectura
                tienda = fg.FuncionesGenerales.leer_archivo(archivo)
                if tienda is not None:
                    titulo_encabezado = f"Registros de {nombreTienda}, agrupados por {criterio}"
                    Label(self, text=titulo_encabezado, font=fuente, bg=color_fondo).pack(pady=10)
                    #valida si se ingresó un criterio de agrupación
                    if criterio == "":
                        messagebox.showwarning("Criterio de Agrupación", "Por favor, ingrese un criterio de agrupación.", icon='warning')
                        return
                    #Se obtiene el promedio de ventas por criterio seleccionado
                    promedio = fg.FuncionesGenerales.calcular_prom_x_criterio(tienda, criterio)
                    Label(self, text=f"El promedio de {criterio} de {nombreTienda} es: {promedio:,.2f}", font=fuente, bg=color_fondo).pack(pady=10)                    
                    #Informacion por cada tienda
                    diccionarioPromedios[nombreTienda] = promedio
                    #se invoca a la funcion para crear las tablas que muestran la informacion                    
                    ClasificacionPromedio.crear_tabla(self, tienda, color_fondo)
                else:
                    messagebox.showerror("Error", f"Error al procesar el archivo {nombreTienda}", icon='error')    
        else:
            messagebox.showwarning("Archivo Seleccionado", f"No se seleccionó ningún archivo.", icon='warning')

        #Se valida si se procesaron tiendas y si no se encuentra doblemente procesadas
        if fg.FuncionesGenerales.contiene_elementos_dict(diccionarioPromedios):   
            #Etiqueta y boton para visualiazar graficas 
            lbl_mostrar_grafica = Label(
                    self,
                    text="Mostrar Gráfica",
                    font=fuente,
                    bg=color_fondo,
                    fg="#333",
                    relief="flat",
                    justify="left"
            )
            lbl_mostrar_grafica.pack(padx=10, pady=5)
            
            #Imagen para el boton
            icono_btn_mostrar_grafica = PhotoImage(file="Recursos/iconos/x32/mostrar_grafica.png")
            btn_mostrar_grafica = Button(self,
                        text="Mostrar Gráfica",
                        image=icono_btn_mostrar_grafica, 
                        bg=color_fondo, 
                        width=32, 
                        height=32,
                        relief="flat",
                        command=lambda: ClasificacionPromedio.graficar_resultados(diccionarioPromedios, criterio))
            btn_mostrar_grafica.image = icono_btn_mostrar_grafica
            btn_mostrar_grafica.pack(padx=10, pady=20)

        return diccionarioPromedios, nombreTienda

    def crear_tabla(self, data, color_fondo):
        try:
            dataFrame = pd.DataFrame(data)
            dataFrame['Precio'] = dataFrame['Precio'].apply(lambda x: "${:,.2f}".format(x))
            dataFrame['Costo de envío'] = dataFrame['Costo de envío'].apply(lambda x: "${:,.2f}".format(x))
            frame = Frame(self, bg=color_fondo)
            frame.pack(fill="both", expand=True, padx=10, pady=10)
            table = Table(frame, dataframe=dataFrame, showtoolbar=True, showstatusbar=True, tablefmt='plain')
            table.autoResizeColumns()
            table.adjustColumnWidths()
            table.editable = False
            table.show() 
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el DataFrame: {e}", icon='error')

    def graficar_resultados(diccionarioPromedios, criterio):
        try:
            tienda = list(diccionarioPromedios.keys())
            promedio = list(diccionarioPromedios.values())    
            plt.barh(tienda, promedio)
            plt.xlabel(f'{criterio} por tienda')
            plt.ylabel('Tiendas')
            plt.title(f'Promedio de {criterio} por tienda')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la gráfica: {e}", icon='error')