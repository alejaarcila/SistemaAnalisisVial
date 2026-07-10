"""
Motor de reglas de negocio de SAVI.

Este módulo evalúa las condiciones técnicas obtenidas por los
módulos matemáticos y de movimiento de tierras.

Ahora el análisis matemático se realiza por tramos, por lo que
se recibe una lista de resultados y no un único modelo.
"""


def evaluar_reglas(resultados_matematicos, movimiento):

    reglas = {}

    # =====================================================
    # R1 - Calidad del modelo matemático
    # Se considera válido si TODOS los tramos tienen
    # un R² mayor o igual a 0.98
    # =====================================================

    r2_promedio = sum(t["r2"] for t in resultados_matematicos) / len(resultados_matematicos)

    reglas["modelo_valido"] = all(
        t["r2"] >= 0.98
        for t in resultados_matematicos
    )

    reglas["r2_promedio"] = round(r2_promedio, 4)

    # =====================================================
    # R2 - Pendientes críticas
    # =====================================================

    reglas["pendiente_critica"] = any(
        t["altura_maxima"] > 12
        for t in resultados_matematicos
    )

    # =====================================================
    # R3 - Predomina corte
    # =====================================================

    reglas["predomina_corte"] = (

        movimiento["volumen_corte"]

        >

        movimiento["volumen_relleno"]

    )

    # =====================================================
    # R4 - Predomina relleno
    # =====================================================

    reglas["predomina_relleno"] = (

        movimiento["volumen_relleno"]

        >

        movimiento["volumen_corte"]

    )

    # =====================================================
    # R5 - Balance corte/relleno
    # =====================================================

    diferencia = abs(

        movimiento["volumen_corte"]

        -

        movimiento["volumen_relleno"]

    )

    reglas["balanceado"] = diferencia < 100

    # =====================================================
    # R6 - Movimiento alto
    # =====================================================

    volumen_total = (

        movimiento["volumen_corte"]

        +

        movimiento["volumen_relleno"]

    )

    reglas["movimiento_alto"] = volumen_total > 1000

    reglas["volumen_total"] = volumen_total

    # =====================================================
    # R7 - Existe corte
    # =====================================================

    reglas["hay_corte"] = movimiento["volumen_corte"] > 0

    # =====================================================
    # R8 - Existe relleno
    # =====================================================

    reglas["hay_relleno"] = movimiento["volumen_relleno"] > 0

    # =====================================================
    # Información adicional
    # =====================================================

    reglas["numero_tramos"] = len(resultados_matematicos)

    reglas["tramos_correctos"] = sum(

        1

        for t in resultados_matematicos

        if t["r2"] >= 0.98

    )

    return reglas