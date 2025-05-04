from tkinter import Label, Tk, Frame, Button, PhotoImage
from AnalisisFacturacion import *
from CategoriaProducto import *
from ClasificacionPromedio import *
from RankingProductos import *
from EnviosPromedio import *
import FuncionesGenerales as fg

class Home:
    def __init__(self, master):
        self.master = master
        self.master.title("Inicio")
        self.master.geometry("500x400")
        self.master.resizable(False, False)
        self.master.configure(bg="#c3f1fd")

         #Propiedades de iconos y tamaño de botones
        formato_icono = "x32"
        if formato_icono == "x32":
            ancho_icono = 32
            largo_icono = 32
        else: 
            ancho_icono = 16
            largo_icono = 16


        #Estilos de fuentes
        fuente_titulo = ("Arial", 14)
        fuente_subtitulo = ("Arial", 10, "italic")
        fuente_texto = ("Arial", 11)


        # Título
        Label(master, text="Bienvenido a la aplicación de Análisis de Tiendas",font=fuente_titulo, bg="#c3f1fd", pady=10).pack()
        
        #Subtitulo
        Label(master, text="Por favor seleccione una opción del menú:", font=fuente_subtitulo, pady=10, bg="#c3f1fd").pack()

        # Contenedor del menú lateral
        contenedor = Frame(master, bg="white")
        contenedor.place(x=50, y=100, width=400, height=260)

         #Propiedades de textos, funciones para cada boton y rutas de imagenes.
        opciones = [
            ("1.- Análisis de Facturación", lambda: AnalisisFacturacion(master),f"iconos/{formato_icono}/analisis_facturacion.png"),
            ("2.- Categoría de Producto", lambda: CategoriaProducto(master),f"iconos/{formato_icono}/categorias.png"),
            ("3.- Clasificación Promedio", lambda: ClasificacionPromedio(master), f"iconos/{formato_icono}/clasificacion_promedio.png"),
            ("4.- Productos más y menos vendidos", lambda: RankingProductos(master), f"iconos/{formato_icono}/ranking_productos.png"),
            ("5.- Envío promedio por Tienda", lambda: EnviosPromedio(master), f"iconos/{formato_icono}/envio_promedio.png"),
            ("6.- Cerrar", lambda: fg.FuncionesGenerales.cerrar_ventana(master), f"iconos/{formato_icono}/salir.png")
        ]
        
        #almacenamiento de botones generados dinamicamente de acuerdo con la lista de opciones
        self.botones = []
        
        #se iteran las opciones y se crean botones para cada una
        for i, (texto, accion,imagen) in enumerate(opciones):
            fila = Frame(contenedor, bg="white")
            fila.pack(fill="x")

            icono_boton = PhotoImage(file=imagen)

            lbl_texto = Button(
                fila,
                text=texto,
                font=("Arial", 11),
                bg="white",
                fg="#333",
                relief="flat",
                anchor="w",
                justify="left",
                padx=10,
                pady=8,
                bd=0,
                highlightthickness=0,
                activebackground="#00bfff",
                activeforeground="white",
                command=lambda idx=i, acc=accion: [self.activar(idx), acc()]
                
            )
            lbl_texto.pack(side="left", fill="x", expand=True)

            btn = Button(
                fila,
                image = icono_boton,
                command = lambda idx = i, acc =accion:[self.activar(idx),acc()],
                width = ancho_icono,
                height = largo_icono,
                bg = "white",
                relief = "flat"
            )

            btn.image = icono_boton
            btn.pack(side = 'right', padx = 10) # pegado al borde derecho

            self.botones.append(lbl_texto)  # Para seguir usando activar()

        self.activar(0)  # Selecciona el primero como activo

    #efecto de sombra en el boton
    def activar(self, index):
        for i, btn in enumerate(self.botones):
            if i == index:
                btn.configure(bg="#00bfff", fg="white")
            else:
                btn.configure(bg="white", fg="#333")


ventana = Tk()
app = Home(ventana)
ventana.mainloop()
