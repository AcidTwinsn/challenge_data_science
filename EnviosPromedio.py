from tkinter.ttk import *
import pandas as pd
from tkinter import Canvas, PhotoImage, filedialog, messagebox, Toplevel, Frame, Button, Label
from pandastable import Table
import os
import matplotlib.pyplot as plt
import FuncionesGenerales as fg

class EnviosPromedio(Toplevel):
    def __init__(self, master=None):
        self.archivos_procesados = set()
        super().__init__(master)
        self.title("Envío promedio por Tienda")
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
        diccionarioTotales = {}
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
        Label(self.interior, text="Bienvenido al Módulo para el Análisis de Envíos Promedio", font=fuente_titulo, bg=color_fondo).pack(anchor="w", padx=10, pady=10)

        #Bloque para alinear compomentes de tablas de resultados  
        contenedor_tablas = Frame(self.interior, bg=color_fondo)
        contenedor_tablas.pack(side="bottom", fill="x", pady=10)
        
        #Bloque para alinear compomentes de cerrar sesión
        contenedor_btn_salir = Frame(self.interior, bg=color_fondo)
        contenedor_btn_salir.pack(side="bottom", fill="x", pady=10)

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
                             command=lambda: EnviosPromedio.obtener_ingresos_totales(contenedor_tablas, 
                                                                        diccionarioTotales, 
                                                                        nombreTienda,
                                                                        fuente_subtitulo, 
                                                                        color_fondo,
                                                                        self.archivos_procesados))
        btn_archivo.image = icono_btn_archivo
        btn_archivo.pack(side="right", padx=300)

        contenedor_tablas.boton_graficar = None

    def obtener_ingresos_totales(self, diccionarioTotales, nombreTienda, fuente, color_fondo, archivos_procesados):
        url_Archivos = filedialog.askopenfilenames()
        if url_Archivos:
            cantidadArchivos = len(url_Archivos)
            messagebox.showinfo("Archivos Seleccionados", f"Se seleccionaron {cantidadArchivos} archivos", icon='info')
            for archivo in url_Archivos:
                #valida si el archivo obtenido ya fue procesado previamente, de ser así no se procesa
                if archivo in archivos_procesados:
                    continue
                nombreTienda = os.path.basename(archivo)
                #valida si el archivo cargado no es csv, de ser así no se procesa
                if not fg.FuncionesGenerales.validar_archivo_csv(self, nombreTienda):                
                    continue
                #self.archivos_procesados.add(archivo)
                tienda = fg.FuncionesGenerales.leer_archivo(archivo)
                if tienda is not None:
                    titulo_encabezado = f"Registros de {nombreTienda}"
                    Label(self, text=titulo_encabezado, font=fuente, bg=color_fondo).pack(pady=10)
                    #Informacion por cada tienda
                    data = tienda
                    #se invoca a la funcion para crear las tablas que muestran la informacion
                    EnviosPromedio.crear_tabla(self, tienda)
                    #Se calcula el promedio de envios para cada tienda
                    promedioEnvios = fg.FuncionesGenerales.calcular_prom_x_criterio(tienda, 'Costo de envío')
                    #Se muestra el promedio total para cada tienda
                    Label(self, text=f"El Promedio de Envíos de {nombreTienda} es: ${promedioEnvios:,.2f}", font=fuente, bg=color_fondo).pack(pady=10)
                    #Se almacena el promedio de envios de cada tienda              
                    diccionarioTotales[nombreTienda] = promedioEnvios
                    archivos_procesados.add(archivo)
                else:
                    messagebox.showerror("Error", f"Error al procesar el archivo {nombreTienda}", icon='error')    
        else:
            messagebox.showwarning("Archivo Seleccionado", f"No se seleccionó ningún archivo.", icon='warning')

        #Se valida si se procesaron tiendas y si no se encuentra doblemente proesadas
        if fg.FuncionesGenerales.contiene_elementos_dict(diccionarioTotales) and self.boton_graficar is None:
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
                        command=lambda: EnviosPromedio.graficar_resultados(diccionarioTotales))
            btn_mostrar_grafica.image = icono_btn_mostrar_grafica
            btn_mostrar_grafica.pack(padx=10, pady=20)

        return diccionarioTotales, nombreTienda

    def crear_tabla(self, data):
        try:
            dataFrame = pd.DataFrame(data)
            frame = Frame(self)
            dataFrame['Precio'] = dataFrame['Precio'].apply(lambda x: "${:,.2f}".format(x))
            dataFrame['Costo de envío'] = dataFrame['Costo de envío'].apply(lambda x: "${:,.2f}".format(x))
            frame.pack(fill="both", expand=True)
            table = Table(frame, dataframe=dataFrame, showtoolbar=True, showstatusbar=True, tablefmt='plain')
            table.autoResizeColumns()
            table.adjustColumnWidths()
            table.editable = False
            table.show() 
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear el DataFrame: {e}", icon='error')

    def graficar_resultados(dictTotales):
        try:
            tienda = list(dictTotales.keys())
            costo_prom_envios = list(dictTotales.values())
            prom_envios_tiendas = sum(costo_prom_envios) / len(costo_prom_envios)
            maximo = max(costo_prom_envios)
            colorNota = ['red' if costo_prom_envio == maximo else 'green' for costo_prom_envio in costo_prom_envios]
            plt.bar(tienda, costo_prom_envios, color=colorNota)
            plt.xlabel('Tiendas')
            plt.ylabel(f'Promedio de Costos de Envíos. El Promedio de Costos de Envíos de todas las Tiendas = ${prom_envios_tiendas:,.2f}')
            plt.title(f'Costo promedio de Envíos por Tienda')
            plt.axhline(y=prom_envios_tiendas, color='black', linestyle='--')
            plt.show()
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la gráfica: {e}", icon='error')