# Coderhouse-DE-01
Repositorio para Curso de Ingenieria de datos - Entregables V1

Objetivos:

- Generar un script (formato .py o .ipynb) que funcione como prototipo (MVP) de un ETL para el proyecto final

- El script debería extraer datos desde una API en formato JSON para ser manipulado como diccionario utilizando el lenguaje Python

- Generar una tabla para ser almacenada en una base de datos a partir de información una API.


Funcionamiento:

- Version de Python: 3.11.2

- El script principal es el nombrado como "main.py", pero ademas cuenta con dos archivos importantes: una libreria nombrada como "maxLib.py" y un archivo de parametrizacion "config.env".

- Para poder ejecutar el script primero que nada se debera completar los datos de autenticacion del archivo .env (DB_USERNAME,DB_PASSWORD, DB_SCHEMA)

- Este utiliza una REST API de clima alojada en el sigueinte host "https://api.open-meteo.com".

- La misma fue parametrizada para recolectar los siguientes datos: temperatura, humedad relativa, precipitacion, lluvia y velocidad del viento.

- Se pasan como parametros GET la latitud, longitud, variables a recolectar, fecha de inicio y fecha de fin.

- Este fue concebido con la idea de que los datos obtenidos son entre un periodo de tiempo acotado entre la fecha previa a la ejecucion del script y la cantidad de dias hacia atras especificados en el archivo de parametrizacion.

- La granulidad de los datos obtenidos son por HORA.

- El script fue desarrollado para poder correr SOLO vez al dia en el horario que se desee.

- Los datos son almacenados en una tabla de RS.




Parametrizacion:

- El script posee un archivo para la parametrizacion de ciertos datos que pueden especificarse. Este es nombrado "config.env" y posee los siguientes parametros:

#Parametros generales del script
VERBOSE_MODE = (Se completa con un valor booleano True|False, y se utilizar para mostrar la salida del SQLACHEMY)

#Datos del Logger
LOG_FILE = (Nombre del archivo de logs que se generara o se sobreescribira en todo caso)
LOG_LEVEL = ( Seteo del tipo de log que se desea. Type: DEBUG = 10, INFO = 20, ERROR = 40)

#DATA REST API
URL_COOR_LAT = (Valor tipo float con signo  que especifica la LATITUD que se le solicita a la API)
URL_COOR_LON = (Valor tipo float con signo  que especifica la LONGITUD que se le solicita a la API)
URL_DAYS_BEFORE = (Valor entero positivo que se utiliza para especificar cuantos dias para atras se desean recolectar)

#Parametros de configuracion de BASE DE DATOS
DB_HOSTNAME = (Host de base de datos de REDSHIFT)
DB_PORT = (Puerto que se utilizar para la conexion a la DB)
DB_NAME = (Nombre de la base de datos RS)
DB_USERNAME = (Username utilizado para la autenticacion)
DB_PASSWORD= (Password utilizado para la autenticacion)
DB_SCHEMA= (Nombre del esquema dentro de la DB donde se trabajara)


========================================================================================

Mejoras en las cuales se encuentran actualmente trabajando para la version 2:


- Creacion de una tabla donde se puedan almacenar distintos datos de ubicaciones para luego recorrerlos en loop y poder recuperar historicos de clima de distintos lugares especificos.

- Podra parametrizarse la tablas y las columnas de las cuales se obtendran estos datos para poder integrarlos con distintos sistemas.

- Se agrega la notificacion de ERRORES de ejecucion via mail.
