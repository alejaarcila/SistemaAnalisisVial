import numpy as np
import pandas as pd


def analizar_logistica(logistica):
    """
    Analiza las condiciones logísticas del corredor vial.

    Parámetros
    ----------
    logistica : DataFrame
        Hoja 'Logistica' del archivo Excel.

    Retorna
    -------
    dict
        Resultados del análisis.
    """

    tabla = logistica.copy()

    # ======================================================
    # Derivadas numéricas
    # ======================================================

    tabla["dV/dPK"] = np.gradient(
        tabla["Velocidad promedio"],
        tabla["PK"]
    )

    tabla["dT/dPK"] = np.gradient(
        tabla["Tiempo de recorrido"],
        tabla["PK"]
    )

    tabla["dCarga/dPK"] = np.gradient(
        tabla["Carga transportada"],
        tabla["PK"]
    )

    # ======================================================
    # Estadísticos
    # ======================================================

    velocidad_maxima = tabla["Velocidad promedio"].max()
    velocidad_minima = tabla["Velocidad promedio"].min()
    velocidad_promedio = tabla["Velocidad promedio"].mean()

    tiempo_maximo = tabla["Tiempo de recorrido"].max()
    tiempo_promedio = tabla["Tiempo de recorrido"].mean()

    carga_maxima = tabla["Carga transportada"].max()
    carga_promedio = tabla["Carga transportada"].mean()

    # ======================================================
    # Integral (regla del trapecio)
    # ======================================================

    tiempo_acumulado = np.trapezoid(
        tabla["Tiempo de recorrido"],
        tabla["PK"]
    )

    # ======================================================
    # PK críticos
    # ======================================================

    idx_vel_min = tabla["Velocidad promedio"].idxmin()

    idx_vel_max = tabla["Velocidad promedio"].idxmax()

    idx_carga_max = tabla["Carga transportada"].idxmax()

    idx_tiempo_max = tabla["Tiempo de recorrido"].idxmax()

    # ======================================================
    # Correlación
    # ======================================================

    correlacion = tabla["Velocidad promedio"].corr(
        tabla["Carga transportada"]
    )

    # ======================================================
    # Resultado
    # ======================================================

    return {

        "tabla": tabla,

        "velocidad_maxima": velocidad_maxima,
        "velocidad_minima": velocidad_minima,
        "velocidad_promedio": velocidad_promedio,

        "tiempo_maximo": tiempo_maximo,
        "tiempo_promedio": tiempo_promedio,
        "tiempo_acumulado": tiempo_acumulado,

        "carga_maxima": carga_maxima,
        "carga_promedio": carga_promedio,

        "pk_velocidad_minima": tabla.loc[idx_vel_min, "PK"],
        "pk_velocidad_maxima": tabla.loc[idx_vel_max, "PK"],

        "pk_tiempo_maximo": tabla.loc[idx_tiempo_max, "PK"],

        "pk_carga_maxima": tabla.loc[idx_carga_max, "PK"],

        "correlacion_velocidad_carga": correlacion

    }