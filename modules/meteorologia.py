import pandas as pd


def analizar_meteorologia(datos):
    """
    Analiza las condiciones meteorológicas del corredor vial.
    """

    resultados = {

        "tabla": datos,

        "temperatura_maxima":
            datos["Temperatura"].max(),

        "temperatura_promedio":
            datos["Temperatura"].mean(),

        "humedad_maxima":
            datos["Humedad relativa"].max(),

        "humedad_promedio":
            datos["Humedad relativa"].mean(),

        "precipitacion_maxima":
            datos["Precipitación"].max(),

        "precipitacion_promedio":
            datos["Precipitación"].mean(),

        "viento_maximo":
            datos["Velocidad del viento"].max(),

        "viento_promedio":
            datos["Velocidad del viento"].mean()

    }

    return resultados