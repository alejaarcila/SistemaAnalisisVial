import numpy as np
import pandas as pd


def analizar_costos(costos):
    """
    Analiza los costos del proyecto vial.

    Parámetros
    ----------
    costos : DataFrame
        Hoja '12. Costos' del archivo Excel.

    Retorna
    -------
    dict
        Indicadores económicos del proyecto.
    """

    tabla = costos.copy()

    # ======================================================
    # Derivadas numéricas
    # ======================================================

    tabla["dCostoMovimiento/dPK"] = np.gradient(
        tabla["Costo de movimiento de tierras"],
        tabla["PK"]
    )

    tabla["dCostoClima/dPK"] = np.gradient(
        tabla["Costo asociado a condiciones climáticas"],
        tabla["PK"]
    )

    tabla["dCostoTotal/dPK"] = np.gradient(
        tabla["Costo total estimado"],
        tabla["PK"]
    )

    # ======================================================
    # Estadísticos
    # ======================================================

    costo_total_maximo = tabla["Costo total estimado"].max()
    costo_total_minimo = tabla["Costo total estimado"].min()
    costo_total_promedio = tabla["Costo total estimado"].mean()

    costo_movimiento_maximo = tabla["Costo de movimiento de tierras"].max()
    costo_movimiento_promedio = tabla["Costo de movimiento de tierras"].mean()

    costo_clima_maximo = tabla["Costo asociado a condiciones climáticas"].max()
    costo_clima_promedio = tabla["Costo asociado a condiciones climáticas"].mean()

    # ======================================================
    # Integrales
    # ======================================================

    costo_total_acumulado = np.trapezoid(
        tabla["Costo total estimado"],
        tabla["PK"]
    )

    costo_movimiento_acumulado = np.trapezoid(
        tabla["Costo de movimiento de tierras"],
        tabla["PK"]
    )

    costo_clima_acumulado = np.trapezoid(
        tabla["Costo asociado a condiciones climáticas"],
        tabla["PK"]
    )

    # ======================================================
    # Participación porcentual
    # ======================================================

    porcentaje_movimiento = (
        costo_movimiento_acumulado
        /
        costo_total_acumulado
        * 100
    )

    porcentaje_clima = (
        costo_clima_acumulado
        /
        costo_total_acumulado
        * 100
    )

    # ======================================================
    # PK críticos
    # ======================================================

    idx_max = tabla["Costo total estimado"].idxmax()
    idx_min = tabla["Costo total estimado"].idxmin()

    idx_gradiente_max = tabla["dCostoTotal/dPK"].idxmax()
    idx_gradiente_min = tabla["dCostoTotal/dPK"].idxmin()

    # ======================================================
    # Correlaciones
    # ======================================================

    correlacion_movimiento_total = tabla[
        "Costo de movimiento de tierras"
    ].corr(
        tabla["Costo total estimado"]
    )

    correlacion_clima_total = tabla[
        "Costo asociado a condiciones climáticas"
    ].corr(
        tabla["Costo total estimado"]
    )

    # ======================================================
    # Resultado
    # ======================================================

    return {

        "tabla": tabla,

        "costo_total_maximo": costo_total_maximo,
        "costo_total_minimo": costo_total_minimo,
        "costo_total_promedio": costo_total_promedio,

        "costo_movimiento_maximo": costo_movimiento_maximo,
        "costo_movimiento_promedio": costo_movimiento_promedio,

        "costo_clima_maximo": costo_clima_maximo,
        "costo_clima_promedio": costo_clima_promedio,

        "costo_total_acumulado": costo_total_acumulado,
        "costo_movimiento_acumulado": costo_movimiento_acumulado,
        "costo_clima_acumulado": costo_clima_acumulado,

        "porcentaje_movimiento": porcentaje_movimiento,
        "porcentaje_clima": porcentaje_clima,

        "pk_costo_maximo": tabla.loc[idx_max, "PK"],
        "pk_costo_minimo": tabla.loc[idx_min, "PK"],

        "pk_gradiente_maximo": tabla.loc[idx_gradiente_max, "PK"],
        "pk_gradiente_minimo": tabla.loc[idx_gradiente_min, "PK"],

        "correlacion_movimiento_total":
            correlacion_movimiento_total,

        "correlacion_clima_total":
            correlacion_clima_total

    }