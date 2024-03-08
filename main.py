# ===============================
# =  DEV: Maximiliano Mansilla
# =  Proyecto: Data Engineering
# =
# =  Versionado:
# =      Version 01 - 2024-03-01
# =      Version 02 - 2024-03-05
# ===============================
from maxLib import *
from dotenv import load_dotenv
import os
import logging
import sys
from sqlalchemy import create_engine
import time
from datetime import datetime, timedelta

# ======CUSTOMIZACION============
path_main = str(rutaActual()) + "/"

# == Archivo de Configuraion ==
load_dotenv("config.env")

# ============VARIABLES - VALORES DE CONFIG FILE ====================
verbose_mode = bool(os.getenv("VERBOSE_MODE"))

url_coor_lat = os.getenv("URL_COOR_LAT")
url_coor_lon = os.getenv("URL_COOR_LON")
url_days_before = os.getenv("URL_DAYS_BEFORE")

db_host = str(os.getenv("DB_HOSTNAME"))
db_port = str(os.getenv("DB_PORT"))
db_dbname = str(os.getenv("DB_NAME"))
db_username = str(os.getenv("DB_USERNAME"))
db_password = str(os.getenv("DB_PASSWORD"))
db_schema = str(os.getenv("DB_SCHEMA"))


# ==============ARCHIVO LOG =============
logFilename = path_main + str(os.getenv("LOG_FILE"))
log_level = int(os.getenv("LOG_LEVEL"))
print(logFilename)

# ==LOGS - Functions
logger = logging.getLogger(__name__)
logger.setLevel(log_level)
handler = logging.FileHandler(logFilename)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.info("Se configuro el LOGGING")


# ======================================================
# ==ETL - EXTRACT======================================

# ==============SET VARS=========================
coor = [url_coor_lat, url_coor_lon]
date_from = (datetime.now() - timedelta(int(url_days_before))).strftime("%Y-%m-%d")
date_to = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")

# =======================================
logger.info("Getting Weather Data")
logger.info("Coor. Latitude: " + coor[0])
logger.info("Coor. Longitud: " + coor[1])
logger.info("Date From: " + date_from)
logger.info("Date To: " + date_to)

# ==================================================

dataGet = getWeather(coor, date_from, date_to)

if dataGet["result"] == False:
    logger.error(dataGet["response"])
    sys.exit(1)
else:
    logger.info("Read Weather OK")
    resp = WeatherJsonToDF(dataGet["response"])
    if resp["result"] == False:
        logger.error(resp["response"])
        sys.exit(1)
    else:
        logger.info("JSON->DF OK")
        df = resp["response"]


# ==================================================================
# ==ETL - TRANSFORM======================================

# renombro la columna 'time' -> 'datetime_log' con un nombre mas representativo
df.rename(columns={"time": "datetime_log"}, inplace=True)
# cambio el tipo de datos de la columna a 'datetime'
df["datetime_log"] = pd.to_datetime(df["datetime_log"])
# Agrego una columna TIMESTAMP para registrar el momento donde se agregaron los registros
date_today = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
df.insert(0, "datetime_reg", str(date_today))
df["datetime_reg"] = pd.to_datetime(df["datetime_reg"])
# agrego las dos columnas de cordenadas para luego poder utilizar el mismo proceso ETL para recolectar datos de otra ubicacion.
df.insert(1, "coor_lat", url_coor_lat)
df.insert(2, "coor_lon", url_coor_lon)


# ==================================================================
# ==ETL - LOAD======================================
try:
    conn_string = f'redshift+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_dbname}'
    engine = create_engine(conn_string, echo=verbose_mode)
    connection = engine.connect()
    logger.info("Connection - OK")
    res = df.to_sql(
        name="logs_weather",
        schema=db_schema,
        con=connection,
        if_exists="append",
        index=False,
    )
    logger.info("Reading Reg: " + str(res))
    logger.info("Add Rows - OK")
except Exception as e:
    logger.error(e)
    sys.exit(1)
logger.info("END")