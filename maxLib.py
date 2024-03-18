# https://api.open-meteo.com/v1/forecast?latitude=-34.709396&longitude=-58.279639&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain,wind_speed_10m&start_date=2024-02-26&end_date=2024-02-27
# Libreria Custom con funciones
# ===============================
from urllib.request import urlopen
import json
import pandas as pd
import pathlib


# Definicion de funciones -


def rutaActual():
    return pathlib.Path(__file__).parent.absolute()


def getWeatherHistory(coor, date_from, date_to):
    try:
        url_data = (
            "https://api.open-meteo.com/v1/forecast?latitude="
            + str(coor[0])
            + "&longitude="
            + str(coor[1])
            + "&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,rain,wind_speed_10m&start_date="
            + str(date_from)
            + "&end_date="
            + str(date_to)
        )
        response = urlopen(url_data)
        data_json = json.loads(response.read())
        return {"result": True, "response": data_json}
    except Exception as e:
        return {"result": False, "response": e}


def WeatherJsonToDF(json_data):
    try:
        df = pd.DataFrame.from_dict(json_data["hourly"])
        return {"result": True, "response": df}
    except Exception as e:
        return {"result": False, "response": e}
