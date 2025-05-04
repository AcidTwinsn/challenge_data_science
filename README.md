# Análisis de Datos de Ventas de Tiendas con Visualización Interactiva

## Descripción General
Esta aplicación permite analizar datos de ventas de diferentes tiendas utilizando archivos CSV. Consta de módulos para calcular ingresos, analizar productos vendidos, evaluar la satisfacción del cliente y más, todo respaldado por visualizaciones interactivas que facilitan la toma de decisiones.

## Requisitos

### Librerías Necesarias
- `tkinter`: Para la interfaz gráfica.
- `pandas`: Para el manejo de archivos CSV y análisis de datos.
- `matplotlib`: Para la creación de gráficos.
- `pandastable`: Para mostrar las tablas de datos de forma interactiva.

### Formato de Archivos CSV
Los archivos CSV deben contener, como mínimo, las siguientes columnas:
- **Producto**: Nombre del producto vendido.
- **Categoría del Producto**: Categoría a la que pertenece el producto.
- **Precio**: Precio del producto.
- **Costo de envío**: Costo del envío asociado al producto.
- **Fecha de Compra**: Fecha en que se realizó la compra.
- **Vendedor**: Nombre del vendedor.
- **Lugar de Compra**: Ubicación de la tienda o el lugar de compra.
- **Calificación**: Puntuación asignada al producto por los clientes.
- **Método de pago**: Forma de pago utilizada.
- **Cantidad de cuotas**: Número de cuotas en las que se dividió el pago.
- **lat**: Latitud de la tienda.
- **lon**: Longitud de la tienda.

## Módulos y Funcionalidades

### 1. Ingreso Total por Tienda
- **Descripción**: Calcula el ingreso total de cada tienda sumando los precios de los productos vendidos.
- **Visualización**: Gráfico de barras comparativo.
- **Funciones Clave**:
  - `obtener_ingresos_totales`: Carga archivos CSV y calcula los ingresos.
  - `graficar_resultados`: Muestra un gráfico de barras con los resultados.

### 2. Productos por Categoría
- **Descripción**: Agrupa los datos por categoría y cuenta el número de ventas de cada tipo.
- **Visualización**: Gráfico circular para mostrar la proporción de ventas por categoría.
- **Funciones Clave**:
  - `agrupar_x_criterio`: Agrupa los datos por una categoría específica.
  - `graficar_resultados`: Genera una visualización de las categorías más vendidas.

### 3. Calificaciones Promedio
- **Descripción**: Calcula la calificación promedio de los clientes para cada tienda.
- **Visualización**: Gráfico de barras que compara las calificaciones promedio entre tiendas.
- **Funciones Clave**:
  - `calcular_prom_x_criterio`: Calcula el promedio de una columna específica.
  - `graficar_resultados`: Visualiza las calificaciones promedio.

### 4. Productos Más y Menos Vendidos
- **Descripción**: Identifica los productos más y menos populares según el número de ventas.
- **Visualización**: Gráfico de líneas que resalta los productos destacados.
- **Funciones Clave**:
  - `obtener_ranking_productos`: Calcula el ranking de productos.
  - `graficar_resultados`: Genera un gráfico para visualizar el ranking.

### 5. Costo de Envío Promedio
- **Descripción**: Calcula el costo promedio de envío por tienda.
- **Visualización**: Gráfico de barras horizontales que compara los costos de envío.
- **Funciones Clave**:
  - `calcular_prom_x_criterio`: Calcula el promedio del costo de envío.
  - `graficar_resultados`: Muestra los resultados en un gráfico interactivo.

## Proceso de Uso
1. Seleccione los archivos CSV correspondientes a las tiendas.
2. Elija el módulo de análisis deseado:
   - Ingresos Totales
   - Productos por Categoría
   - Calificaciones Promedio
   - Productos Más y Menos Vendidos
   - Costo de Envío Promedio
3. Visualice los resultados en una tabla interactiva.
4. Genere gráficos para comprender mejor los datos.
5. Con base en el análisis, cree una recomendación fundamentada sobre dónde vender.

## Ejemplo de Gráficos
- **Ingreso Total**: Gráfico de barras que compara ingresos entre tiendas.
- **Distribución de Categorías**: Gráfico circular que muestra las categorías más populares.
- **Satisfacción del Cliente**: Gráfico de barras que compara calificaciones promedio.

## Recomendación Final
Al final del análisis, la aplicación genera una recomendación sobre cuál tienda es la mejor opción para vender, destacando:
- Ingresos elevados.
- Buenas calificaciones de clientes.
- Bajos costos de envío.

## Conclusión
Esta aplicación proporciona una solución integral para analizar y visualizar datos de ventas, ayudando a tomar decisiones informadas sobre dónde y cómo vender. Las visualizaciones interactivas facilitan la identificación de tendencias y patrones relevantes en los datos.
