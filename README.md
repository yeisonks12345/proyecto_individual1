# Proyecto analisis de peliculas con sistema de recomendacion:
Estructura de carpetas:

Data input: contiene los archivos orignales suministrados para el proyecto, se aclara que el archivo "credits_2" se convirtio a tipo excel ya que de esta manera pesa menos el archivo
Data output: contiene los archivos csv con datos transformados y que son consumidos por a API.
Trans-EDA: contiene notebooks de python, donde se realizaron las transformaciones de los datos
y el EDA.
Archivo main: contiene la logica de la API

Requirements:
Se uso python version 3.9.13 y las siguientes librerias se instalaron para la ejecucion
fastapi
numpy
pandas
scikit-learn
uvicorn
Fases:
Transformacin de datos:
Se transforman columnas en formatos requeridos, fechas, int, float.
Transformacion de datos:Se eliminan campos que no se van a requerir en el proyecto.
se completan valores faltantes para variables numericas con ceros.
se exportan los datos en archivos tipo csv.
Funciones API:
En el archivo main se codifican 7 funciones.
Las primeras 6 capturan datos de los dataframe de output y se crean funciones de agregacion,
la ultima funcion usa modelos de machine learning para recomendar 5 peliculas.

EDA:
Se analizan los diferentes campos para encontrar informacion relevante por ejemplo:
Se evidencia que si una pelicula fue estrenada en el mes de noviembre se obtiene un mayor return promedio.
de igual forma si se estrena un jueves.
Se evidnencia correlacion lineal entre las variables vote_count y revenue.
