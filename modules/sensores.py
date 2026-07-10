"""
=========================================================
SAVI
Módulo de Sensores IoT
=========================================================

Este módulo procesa la información proveniente de los
sensores IoT instalados a lo largo del corredor vial.

Calcula:

- Velocidad segura
- Tiempo incremental
- Tiempo de despeje
- Tiempo recomendado para Pare y Siga
"""

import numpy as np
import pandas as pd


def analizar_sensores(tabla):

    sensores = tabla.copy()

    # ----------------------------------------------
    # Modelo de velocidad segura
    # ----------------------------------------------
    #
    # v(x)=40−1.8|I(x)|−0.15H(x)
    #
    # Velocidad mínima = 5 km/h
    #
    # ----------------------------------------------

    sensores["Velocidad Segura"] = (

        40

        -

        1.8 * sensores["Inclinación"].abs()

        -

        0.15 * sensores["Humedad relativa"]

    )

    sensores["Velocidad Segura"] = sensores[
        "Velocidad Segura"
    ].clip(lower=5)

    # ----------------------------------------------
    # Tiempo incremental
    # dx = diferencia entre progresivas
    # dt = dx / v
    # ----------------------------------------------

    sensores["dx"] = sensores["PK"].diff().fillna(0)

    sensores["Tiempo_horas"] = (

        sensores["dx"]

        /

        sensores["Velocidad Segura"]

    )

    sensores["Tiempo_min"] = (

        sensores["Tiempo_horas"]

        *

        60

    )

    # ----------------------------------------------
    # Integral numérica
    # ----------------------------------------------

    tiempo_total_horas = np.trapezoid(

        1 / sensores["Velocidad Segura"],

        sensores["PK"]

    )

    tiempo_total_min = tiempo_total_horas * 60

    tiempo_total_seg = tiempo_total_min * 60

    # ----------------------------------------------
    # Punto crítico
    # ----------------------------------------------

    fila = sensores.loc[
        sensores["Velocidad Segura"].idxmin()
    ]

    # ----------------------------------------------

    return {

        "tabla": sensores,

        "velocidad_minima": round(
            sensores["Velocidad Segura"].min(), 2
        ),

        "velocidad_promedio": round(
            sensores["Velocidad Segura"].mean(), 2
        ),

        "tiempo_despeje_min": round(
            tiempo_total_min, 2
        ),

        "tiempo_semaforo_seg": round(
            tiempo_total_seg, 0
        ),

        "pk_critico": round(
            fila["PK"], 2
        ),

        "inclinacion_critica": round(
            fila["Inclinación"], 2
        ),

        "humedad_critica": round(
            fila["Humedad relativa"], 2
        )

    }