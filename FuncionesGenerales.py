import pandas as pd
from tkinter import messagebox
class FuncionesGenerales:
   def leer_archivo(url):
      try:
         tienda = pd.read_csv(url)
         return tienda
      except Exception as e:
         return None

   def contiene_elementos_dict(diccionario):
      if len(diccionario) > 0:
         return True
      else:
         return False

   def calcular_ingreso_total(tienda):
      return tienda['Precio'].sum()
   
   def agrupar_x_criterio(tienda, criterio):
    try:        
        ventas_por_categoria = (
            tienda.groupby(criterio) 
            .size()
            .reset_index(name='cantidad_vendida')
            .sort_values(by='cantidad_vendida', ascending=False)
            .reset_index(drop=True)
        )
        return ventas_por_categoria
    except Exception as e:
        return None

   def sumIng_TotVen_x_criterio(tienda, criterio):
      try:
         ventas_por_categoria = (
                tienda.groupby(criterio)
                .agg(
                    cantidad_vendida =('Producto','count'),
                    ingreso_total=('Precio','sum')
                )
                .reset_index()
                .sort_values(by='ingreso_total', ascending=False)
                .reset_index(drop=True) 
               )          
         return ventas_por_categoria
      except Exception as e:
         return None  
   
   def obtener_ranking_prod(tienda, orden):
      try:
         if orden == 'Productos más vendidos':
            ord = False
         elif orden == 'Productos menos vendidos':
            ord = True
         else:
            ord = False

         ranking_productos = (
            tienda.groupby('Producto')
            .agg(
                cantidad_vendida=('Producto', 'count')
            )
            .reset_index()
            .sort_values(by='cantidad_vendida', ascending=ord)
            .reset_index(drop=True)
         )
         return ranking_productos
      except Exception as e:
         return None

   def calcular_prom_x_criterio(tienda, criterio):
      return tienda[criterio].mean()
  
   def cerrar_ventana(self):
      if messagebox.askokcancel("Salir", "¿Desea salir de la aplicación?"):
         self.destroy()
         
   def validar_archivo_csv(self, archivo):
      if not archivo.endswith('.csv'):
         messagebox.showerror("Error", f"El archivo {archivo} no es un archivo CSV", icon='error')
         return False
      return True