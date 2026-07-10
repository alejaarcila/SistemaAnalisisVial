import pandas as pd
import numpy as np
from scipy.integrate import trapezoid

ANCHO_VIA = 8  # metros


# =====================================================
# DETECCIÓN DE TRAMOS
# =====================================================

def detectar_tramos(comparacion):
    """
    Detecta automáticamente los tramos de corte y relleno.
    """

    tramos = []

    inicio = 0
    accion_actual = comparacion.loc[0, "Acción"]
    contador = 1

    for i in range(1, len(comparacion)):

        nueva_accion = comparacion.loc[i, "Acción"]

        if nueva_accion != accion_actual:

            tramo = comparacion.iloc[inicio:i+1].copy()

            tramos.append({

                "id": f"T{contador}",

                "tipo": accion_actual,

                "pk_inicio": float(tramo["PK"].iloc[0]),

                "pk_fin": float(tramo["PK"].iloc[-1]),

                "longitud": float(
                    tramo["PK"].iloc[-1] - tramo["PK"].iloc[0]
                ),

                "altura_maxima": float(
                    abs(tramo["Diferencia"]).max()
                ),

                "datos": tramo

            })

            inicio = i
            accion_actual = nueva_accion
            contador += 1

    # Último tramo

    tramo = comparacion.iloc[inicio:].copy()

    tramos.append({

        "id": f"T{contador}",

        "tipo": accion_actual,

        "pk_inicio": float(tramo["PK"].iloc[0]),

        "pk_fin": float(tramo["PK"].iloc[-1]),

        "longitud": float(
            tramo["PK"].iloc[-1] - tramo["PK"].iloc[0]
        ),

        "altura_maxima": float(
            abs(tramo["Diferencia"]).max()
        ),

        "datos": tramo

    })

    return tramos


# =====================================================
# MOVIMIENTO DE TIERRAS
# =====================================================

def analizar_movimiento_tierras(
    perfil_real,
    perfil_proyectado
):
    """
    Analiza el movimiento de tierras comparando
    el perfil real y el perfil proyectado.
    """

    real = perfil_real.copy()
    proyectado = perfil_proyectado.copy()

    # ------------------------------------------
    # Pendiente del perfil proyectado
    # ------------------------------------------

    proyectado["Pendiente"] = (
        proyectado["Elevación proyectada"].diff()
        /
        proyectado["PK"].diff()
    ).fillna(0)

    # ------------------------------------------
    # Tabla de comparación
    # ------------------------------------------

    comparacion = pd.DataFrame()

    comparacion["PK"] = real["PK"]

    comparacion["Elevación Real"] = real["Elevación"]

    comparacion["Elevación Proyectada"] = proyectado["Elevación proyectada"]

    comparacion["Pendiente Real"] = real["Pendiente"]

    comparacion["Pendiente Proyectada"] = proyectado["Pendiente"]

    # ------------------------------------------
    # Diferencia
    # ------------------------------------------

    comparacion["Diferencia"] = (

        comparacion["Elevación Real"]

        -

        comparacion["Elevación Proyectada"]

    )

    # ------------------------------------------
    # Clasificación
    # ------------------------------------------

    def clasificar(valor):

        if valor > 0:
            return "Corte"

        elif valor < 0:
            return "Relleno"

        return "Sin intervención"

    comparacion["Acción"] = comparacion["Diferencia"].apply(clasificar)

    # ------------------------------------------
    # Corte y relleno
    # ------------------------------------------

    comparacion["Corte"] = comparacion["Diferencia"].clip(lower=0)

    comparacion["Relleno"] = (-comparacion["Diferencia"]).clip(lower=0)

    # ------------------------------------------
    # Áreas
    # ------------------------------------------

    area_corte = trapezoid(
        comparacion["Corte"],
        comparacion["PK"]
    )

    area_relleno = trapezoid(
        comparacion["Relleno"],
        comparacion["PK"]
    )

    # ------------------------------------------
    # Volúmenes
    # ------------------------------------------

    volumen_corte = area_corte * ANCHO_VIA

    volumen_relleno = area_relleno * ANCHO_VIA

    # ------------------------------------------
    # Tramos
    # ------------------------------------------

    tramos = detectar_tramos(comparacion)

    # ------------------------------------------
    # Resultados
    # ------------------------------------------

    resultados = {

        "tabla": comparacion,

        "tramos": tramos,

        "area_corte": area_corte,

        "area_relleno": area_relleno,

        "volumen_corte": volumen_corte,

        "volumen_relleno": volumen_relleno,

        "pk_corte": comparacion.loc[
            comparacion["Acción"] == "Corte",
            "PK"
        ].tolist(),

        "pk_relleno": comparacion.loc[
            comparacion["Acción"] == "Relleno",
            "PK"
        ].tolist()

    }

    return resultados