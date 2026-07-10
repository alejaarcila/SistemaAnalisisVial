import pandas as pd


# ==========================================================
# Función auxiliar
# ==========================================================

def normalizar(serie):
    """
    Normaliza una serie entre 0 y 100.
    """

    minimo = serie.min()
    maximo = serie.max()

    if maximo == minimo:
        return pd.Series([0] * len(serie), index=serie.index)

    return (serie - minimo) / (maximo - minimo) * 100


# ==========================================================
# Conversión de cobertura vegetal
# ==========================================================

def convertir_cobertura(valor):

    valor = str(valor).lower()

    if "bosque" in valor:
        return 10

    if "pasto" in valor:
        return 80

    return 50


# ==========================================================
# Índice SAVI de Susceptibilidad a Deslizamientos
# ==========================================================

def calcular_isd(
    tramos,
    perfil_topografico,
    meteorologia,
    suelos,
    cobertura
):
    """
    Calcula el ISD para cada tramo.

    ISD =
        0.45 Pendiente +
        0.30 Precipitación +
        0.15 Humedad +
        0.05 Plasticidad +
        0.05 Cobertura
    """

    # ------------------------------------------------------
    # Preparar información
    # ------------------------------------------------------

    perfil = perfil_topografico.copy()

    # Calcular la pendiente a partir del perfil proyectado
    perfil["Pendiente"] = (
    perfil["Elevación proyectada"].diff()
    /
    perfil["PK"].diff()
    )

    perfil["Pendiente"] = perfil["Pendiente"].fillna(0)

    perfil["Pendiente_norm"] = normalizar(
    perfil["Pendiente"].abs()
    )




    met = meteorologia.copy()

    met["Precipitacion_norm"] = normalizar(
        met["Precipitación"]
    )

    suelo = suelos.copy()

    suelo["Humedad_norm"] = normalizar(
        suelo["Humedad natural"]
    )

    suelo["Plasticidad_norm"] = normalizar(
        suelo["Índice de plasticidad"]
    )

    cob = cobertura.copy()

    cob["Cobertura_num"] = cob["Tipo"].apply(
        convertir_cobertura
    )

    cob["Cobertura_norm"] = normalizar(
        cob["Cobertura_num"]
    )

    # ------------------------------------------------------
    # Calcular ISD por tramo
    # ------------------------------------------------------

    resultados = []

    for tramo in tramos:

        pk1 = tramo["pk_inicio"]
        pk2 = tramo["pk_fin"]

        p = perfil[
            (perfil["PK"] >= pk1)
            &
            (perfil["PK"] <= pk2)
        ]

        m = met[
            (met["PK"] >= pk1)
            &
            (met["PK"] <= pk2)
        ]

        s = suelo[
            (suelo["PK"] >= pk1)
            &
            (suelo["PK"] <= pk2)
        ]

        c = cob[
            (cob["PK"] >= pk1)
            &
            (cob["PK"] <= pk2)
        ]

        pendiente = p["Pendiente_norm"].mean()

        lluvia = m["Precipitacion_norm"].mean()

        humedad = s["Humedad_norm"].mean()

        plasticidad = s["Plasticidad_norm"].mean()

        cobertura_v = c["Cobertura_norm"].mean()

        isd = (

            0.45 * pendiente

            +

            0.30 * lluvia

            +

            0.15 * humedad

            +

            0.05 * plasticidad

            +

            0.05 * cobertura_v

        )

        # ---------------------------------------------

        if isd < 20:

            riesgo = "Muy Bajo"

        elif isd < 40:

            riesgo = "Bajo"

        elif isd < 60:

            riesgo = "Medio"

        elif isd < 80:

            riesgo = "Alto"

        else:

            riesgo = "Muy Alto"

        resultados.append({

            "Tramo": tramo["id"],

            "Tipo": tramo["tipo"],

            "PK Inicio": round(pk1, 3),

            "PK Fin": round(pk2, 3),

            "Pendiente": round(pendiente, 3),

            "Precipitación": round(lluvia, 3),

            "Humedad": round(humedad, 3),

            "Plasticidad": round(plasticidad, 3),

            "Cobertura": round(cobertura_v, 3),

            "ISD": round(isd, 3),

            "Riesgo": riesgo

        })

    return pd.DataFrame(resultados)