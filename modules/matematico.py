"""
==========================================================
SAVI
Motor Matemático
==========================================================

Este módulo recibe un tramo previamente identificado por el
módulo de Movimiento de Tierras y realiza el análisis
matemático mediante un ajuste parabólico.

Para cada tramo calcula:

- Función cuadrática
- Primera derivada
- Integral indefinida
- Punto crítico
- Máximo o mínimo
- Coeficiente de determinación R²
"""

import numpy as np
import sympy as sp


def analizar_tramo(tramo):
    """
    Analiza un tramo de corte o relleno.

    Parámetro
    ---------
    tramo : dict

        Diccionario generado por movimiento_tierras.py

    Retorna
    -------
    dict
    """

    datos = tramo["datos"]

    x = datos["PK"].to_numpy()

    # Si el tramo es de corte usamos la diferencia positiva
    # Si es relleno usamos el relleno positivo

    if tramo["tipo"] == "Corte":

        y = datos["Corte"].to_numpy()

    else:

        y = datos["Relleno"].to_numpy()

    # --------------------------------------------------
    # Ajuste parabólico
    # --------------------------------------------------

    coef = np.polyfit(x, y, 2)

    modelo = np.poly1d(coef)

    y_pred = modelo(x)

    # --------------------------------------------------
    # R²
    # --------------------------------------------------

    ss_res = np.sum((y - y_pred) ** 2)

    ss_tot = np.sum((y - np.mean(y)) ** 2)

    if ss_tot == 0:

        r2 = 1.0

    else:

        r2 = 1 - ss_res / ss_tot

    # --------------------------------------------------
    # Matemática simbólica
    # --------------------------------------------------

    X = sp.Symbol("x")

    funcion = (

         round(float(coef[0]), 3) * X**2

        +

        round(float(coef[1]), 3) * X

        +

        round(float(coef[2]), 3)

    )

    derivada = sp.diff(funcion, X)

    integral = sp.integrate(round(float(coef[2]), 3), X)

    # --------------------------------------------------
    # Punto crítico
    # --------------------------------------------------

    puntos = sp.solve(derivada, X)

    punto_critico = None

    valor_critico = None

    tipo = "No determinado"

    if len(puntos) > 0:

        punto = float(puntos[0])

        punto_critico = punto

        valor_critico = float(funcion.subs(X, punto))

        segunda = sp.diff(derivada, X)

        segunda_valor = float(segunda.subs(X, punto))

        if segunda_valor > 0:

            tipo = "Mínimo"

        elif segunda_valor < 0:

            tipo = "Máximo"

    # --------------------------------------------------
    # Resultado
    # --------------------------------------------------

    return {

        "id": tramo["id"],

        "tipo_tramo": tramo["tipo"],

        "pk_inicio": tramo["pk_inicio"],

        "pk_fin": tramo["pk_fin"],

        "longitud": tramo["longitud"],

        "altura_maxima": tramo["altura_maxima"],

        "funcion": funcion,

        "funcion_latex": sp.latex(sp.expand(funcion)),

        "derivada": derivada,

        "derivada_latex": sp.latex(sp.expand(derivada)),

        "integral": integral,

        "integral_latex": sp.latex(sp.expand(integral)),

        "r2": round(r2, 4),

        "modelo": modelo,

        "punto_critico": punto_critico,

        "valor_critico": valor_critico,

        "tipo_extremo": tipo

    }


def analizar_tramos(tramos):
    """
    Analiza todos los tramos generados por el módulo
    Movimiento de Tierras.
    """

    resultados = []

    for tramo in tramos:

        resultados.append(

            analizar_tramo(tramo)

        )

    return resultados