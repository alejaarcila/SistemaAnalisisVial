"""
==========================================================
SAVI
Recomendaciones Inteligentes
==========================================================

Genera recomendaciones de ingeniería a partir de todos los
análisis realizados por SAVI.
"""


def generar_recomendaciones(
    reglas,
    movimiento,
    resultados,
    isd,
    meteorologia,
    sensores,
    logistica,
    costos
):

    recomendaciones = []

    # =====================================================
    # MODELO MATEMÁTICO
    # =====================================================

    promedio_r2 = sum(t["r2"] for t in resultados) / len(resultados)

    if promedio_r2 < 0.95:

        recomendaciones.append(
            "Revisar la segmentación automática del perfil topográfico o emplear funciones de mayor complejidad en los tramos con menor ajuste matemático."
        )

    # =====================================================
    # MOVIMIENTO DE TIERRAS
    # =====================================================

    if movimiento["volumen_corte"] > movimiento["volumen_relleno"]:

        excedente = (
            movimiento["volumen_corte"]
            - movimiento["volumen_relleno"]
        )

        recomendaciones.append(
            f"Evaluar la reutilización de aproximadamente {excedente:.2f} m³ de material de corte antes de considerar su disposición final."
        )

    elif movimiento["volumen_relleno"] > movimiento["volumen_corte"]:

        deficit = (
            movimiento["volumen_relleno"]
            - movimiento["volumen_corte"]
        )

        recomendaciones.append(
            f"Planificar el suministro de aproximadamente {deficit:.2f} m³ adicionales de material para relleno."
        )

    # =====================================================
    # PENDIENTES
    # =====================================================

    pendiente_max = movimiento["tabla"]["Pendiente Proyectada"].abs().max()

    if pendiente_max > 12:

        recomendaciones.append(
            "Implementar medidas de estabilización (bermas, drenajes, geotextiles o muros) en los sectores con pendientes superiores al 12 %."
        )

    # =====================================================
    # METEOROLOGÍA
    # =====================================================

    if meteorologia["precipitacion_promedio"] > 10:

        recomendaciones.append(
            "Diseñar un sistema eficiente de drenaje superficial y longitudinal para controlar la escorrentía durante eventos de lluvia."
        )

    if meteorologia["humedad_promedio"] > 80:

        recomendaciones.append(
            "Controlar el contenido de humedad del suelo durante las actividades de excavación y compactación."
        )

    if meteorologia["viento_maximo"] > 40:

        recomendaciones.append(
            "Evaluar restricciones temporales para la operación de equipos de gran altura durante eventos de viento fuerte."
        )

    # =====================================================
    # ISD
    # =====================================================

    tramos_criticos = isd[isd["Riesgo"].isin(["Alto", "Muy Alto"])]

    if len(tramos_criticos) > 0:

        recomendaciones.append(
            f"Priorizar los {len(tramos_criticos)} tramo(s) clasificados con riesgo Alto o Muy Alto durante el diseño definitivo."
        )

        recomendaciones.append(
            "Implementar programas de revegetación y control de erosión en los sectores con mayor susceptibilidad."
        )

    # =====================================================
    # SENSORES IoT
    # =====================================================

    if abs(sensores["inclinacion_critica"]) > 15:

        recomendaciones.append(
            "Mantener monitoreo continuo mediante sensores IoT en los sectores con mayores inclinaciones."
        )

    if sensores["humedad_critica"] > 95:

        recomendaciones.append(
            "Incrementar la frecuencia de inspección cuando los sensores registren altos niveles de humedad relativa."
        )

    # =====================================================
    # LOGÍSTICA
    # =====================================================

    if logistica["velocidad_minima"] < 32:

        recomendaciones.append(
            "Optimizar la programación del transporte de materiales en el tramo donde se presenta la menor velocidad de operación."
        )

    if logistica["correlacion_velocidad_carga"] < -0.70:

        recomendaciones.append(
            "Revisar la distribución de carga de los vehículos para mejorar la eficiencia logística del proyecto."
        )

    # =====================================================
    # COSTOS
    # =====================================================

    if costos["porcentaje_movimiento"] > 85:

        recomendaciones.append(
            "Optimizar las actividades de movimiento de tierras, ya que representan el mayor componente del presupuesto del proyecto."
        )

    if costos["porcentaje_clima"] > 10:

        recomendaciones.append(
            "Implementar estrategias constructivas que reduzcan los sobrecostos asociados a condiciones climáticas adversas."
        )

    # =====================================================
    # RECOMENDACIONES GENERALES
    # =====================================================

    recomendaciones.append(
        "Actualizar periódicamente el modelo matemático conforme se obtengan nuevos levantamientos topográficos."
    )

    recomendaciones.append(
        "Realizar seguimiento técnico durante la ejecución de la obra para validar los indicadores calculados por SAVI."
    )

    # =====================================================
    # ELIMINAR DUPLICADOS
    # =====================================================

    recomendaciones = list(dict.fromkeys(recomendaciones))

    return recomendaciones