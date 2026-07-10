"""
==========================================================
SAVI
Interpretación Inteligente
==========================================================

Genera un diagnóstico técnico a partir de los resultados
obtenidos por los diferentes módulos del sistema.
"""


def interpretar_modelo(reglas, movimiento, resultados, isd,sensores, logistica, costos, meteorologia):

    mensajes = []

    # =====================================================
    # MODELO MATEMÁTICO
    # =====================================================

    promedio_r2 = sum(t["r2"] for t in resultados) / len(resultados)

    mensajes.append(

        f"Se analizaron {len(resultados)} tramos homogéneos del perfil topográfico mediante modelos cuadráticos independientes. "
        f"El coeficiente promedio de determinación obtenido fue R² = {promedio_r2:.3f}."

    )

    if promedio_r2 >= 0.98:

        mensajes.append(

            "Los modelos matemáticos presentan un excelente ajuste respecto al perfil topográfico, permitiendo realizar estimaciones confiables de pendientes, áreas y volúmenes."

        )

    elif promedio_r2 >= 0.95:

        mensajes.append(

            "Los modelos matemáticos representan adecuadamente el comportamiento del terreno, aunque algunos tramos podrían beneficiarse de un ajuste adicional."

        )

    else:

        mensajes.append(

            "Algunos tramos presentan un ajuste limitado. Se recomienda revisar la segmentación del perfil o considerar funciones de mayor complejidad."

        )

    # =====================================================
    # MOVIMIENTO DE TIERRAS
    # =====================================================

    volumen_corte = movimiento["volumen_corte"]
    volumen_relleno = movimiento["volumen_relleno"]

    if volumen_corte > volumen_relleno:

        mensajes.append(

            f"Predomina el movimiento de corte ({volumen_corte:.2f} m³) sobre el relleno ({volumen_relleno:.2f} m³), indicando una mayor necesidad de excavación."

        )

    elif volumen_relleno > volumen_corte:

        mensajes.append(

            f"Predomina el movimiento de relleno ({volumen_relleno:.2f} m³) sobre el corte ({volumen_corte:.2f} m³)."

        )

    else:

        mensajes.append(

            "Los volúmenes de corte y relleno se encuentran prácticamente balanceados."

        )

    diferencia = abs(volumen_corte - volumen_relleno)

    if diferencia < 100:

        mensajes.append(

            "El balance entre corte y relleno favorece el aprovechamiento del material dentro del proyecto."

        )

    else:

        mensajes.append(

            "Se observa un desbalance importante entre corte y relleno, lo que puede incrementar los costos de transporte y disposición del material."

        )

    # =====================================================
    # PENDIENTES
    # =====================================================

    pendiente_max = movimiento["tabla"]["Pendiente Proyectada"].abs().max()

    if pendiente_max > 12:

        mensajes.append(

            f"La pendiente máxima del perfil proyectado alcanza {pendiente_max:.2f} %, superando el umbral de referencia (12 %). Existen sectores que podrían requerir medidas especiales de estabilización."

        )

    else:

        mensajes.append(

            f"La pendiente máxima del proyecto ({pendiente_max:.2f} %) se encuentra dentro del rango considerado adecuado."

        )

    # =====================================================
    # ÍNDICE DE SUSCEPTIBILIDAD
    # =====================================================

    muy_alto = len(isd[isd["Riesgo"] == "Muy Alto"])
    alto = len(isd[isd["Riesgo"] == "Alto"])
    medio = len(isd[isd["Riesgo"] == "Medio"])
    bajo = len(isd[isd["Riesgo"] == "Bajo"])
    muy_bajo = len(isd[isd["Riesgo"] == "Muy Bajo"])

    mensajes.append(

        f"El Índice de Susceptibilidad a Deslizamientos (ISD) identificó "
        f"{muy_alto} tramo(s) con riesgo Muy Alto, "
        f"{alto} con riesgo Alto, "
        f"{medio} con riesgo Medio, "
        f"{bajo} con riesgo Bajo y "
        f"{muy_bajo} con riesgo Muy Bajo."

    )

    tramo_critico = isd.sort_values("ISD", ascending=False).iloc[0]

    mensajes.append(

        f"El tramo más crítico corresponde a {tramo_critico['Tramo']} "
        f"(PK {tramo_critico['PK Inicio']:.2f} - {tramo_critico['PK Fin']:.2f}), "
        f"con un ISD de {tramo_critico['ISD']:.3f}, clasificado como riesgo "
        f"{tramo_critico['Riesgo']}."

    )

    # =====================================================
    # METEOROLOGÍA
    # =====================================================

    mensajes.append(
            f"Las condiciones meteorológicas presentan una precipitación máxima de "
            f"{meteorologia['precipitacion_maxima']:.2f} mm, "
            f"una humedad relativa promedio de "
            f"{meteorologia['humedad_promedio']:.2f} % y "
            f"una velocidad máxima del viento de "
            f"{meteorologia['viento_maximo']:.2f} km/h."
        )

    if meteorologia["precipitacion_maxima"] > 120:
            mensajes.append(

                "Las lluvias intensas podrían favorecer procesos de erosión superficial e incrementar la susceptibilidad a deslizamientos en algunos sectores."

            )

    if meteorologia["humedad_promedio"] > 80:

            mensajes.append(

                "La elevada humedad relativa favorece la saturación del terreno, condición que debe considerarse durante la planificación de las actividades constructivas."

            )
    # =====================================================
    # SENSORES IOT
    # =====================================================

    mensajes.append(

    f"Los sensores IoT identifican como punto más crítico el PK {sensores['pk_critico']:.2f}, "
    f"donde la inclinación alcanza {sensores['inclinacion_critica']:.2f}° "
    f"y la humedad relativa {sensores['humedad_critica']:.2f}%."

    )

    if abs(sensores["inclinacion_critica"]) > 15:

        mensajes.append(

            "La elevada inclinación registrada por los sensores confirma la presencia de sectores que requieren seguimiento durante la ejecución del proyecto."

        )

    if sensores["humedad_critica"] > 95:

        mensajes.append(

            "Los sensores reportan condiciones de alta humedad en el punto crítico, situación que puede favorecer la pérdida de estabilidad del terreno."

        )

    # =====================================================
    # LOGÍSTICA
    # =====================================================

    mensajes.append(

        f"La velocidad promedio de operación es de "
        f"{logistica['velocidad_promedio']:.2f} km/h, "
        f"alcanzando un mínimo de "
        f"{logistica['velocidad_minima']:.2f} km/h "
        f"en el PK {logistica['pk_velocidad_minima']:.2f}."

    )

    if logistica["velocidad_minima"] < 32:

        mensajes.append(

            "El corredor presenta un posible cuello de botella logístico asociado a la reducción de velocidad en uno de sus sectores."

        )

    if logistica["correlacion_velocidad_carga"] < -0.70:

        mensajes.append(

            "Existe una fuerte relación inversa entre la carga transportada y la velocidad de circulación."

        )

        # =====================================================
        # COSTOS
        # =====================================================

    mensajes.append(

        f"El costo acumulado estimado del proyecto asciende a "
        f"{costos['costo_total_acumulado']:.2f} unidades monetarias."

    )

    mensajes.append(

        f"El {costos['porcentaje_movimiento']:.2f}% del presupuesto corresponde al movimiento de tierras y "
        f"el {costos['porcentaje_clima']:.2f}% a condiciones climáticas."

    )

    if costos["porcentaje_movimiento"] > 85:

        mensajes.append(

            "El movimiento de tierras constituye el componente económico predominante del proyecto."

        )

    if costos["porcentaje_clima"] > 10:

        mensajes.append(

            "Las condiciones climáticas representan un porcentaje significativo del costo total de la obra."

        )

    # =====================================================
    # CONCLUSIÓN GENERAL
    # =====================================================

    if promedio_r2 >= 0.98 and alto == 0 and muy_alto == 0:

        mensajes.append(

            "El análisis integral desarrollado por SAVI evidencia un excelente ajuste matemático del perfil topográfico, un comportamiento geométrico adecuado y condiciones favorables desde el punto de vista geotécnico, ambiental, logístico y económico para la etapa de planificación del proyecto."

        )

    elif muy_alto > 0 or alto > 0:

        mensajes.append(

            "Aunque el modelo matemático representa adecuadamente el terreno, el análisis integral identifica sectores que requieren especial atención debido a la combinación de factores geométricos, geotécnicos, meteorológicos, logísticos y económicos que pueden incrementar el riesgo durante la ejecución del proyecto."

        )

    else:

        mensajes.append(

            "El proyecto presenta condiciones generales aceptables; sin embargo, el análisis integral recomienda mantener el seguimiento de los indicadores geométricos, ambientales, logísticos y económicos para optimizar la planificación y reducir posibles riesgos durante la construcción."

        )

    return mensajes