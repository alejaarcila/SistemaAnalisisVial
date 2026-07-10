import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from utils.lector_excel import cargar_proyecto

from modules.movimiento_tierras import analizar_movimiento_tierras
from modules.matematico import analizar_tramos

from modules.interpretacion import interpretar_modelo
from modules.meteorologia import analizar_meteorologia
from modules.indice_deslizamiento import calcular_isd
from modules.sensores import analizar_sensores
from modules.logistica import analizar_logistica
from modules.costos import analizar_costos
from modules.recomendaciones import generar_recomendaciones
from modules.reglas import evaluar_reglas


# ==========================================================
# Configuración
# ==========================================================

st.set_page_config(
    page_title="SAVI",
    page_icon="🛣️",
    layout="wide"
)

# ==========================================================
# Encabezado
# ==========================================================

st.title("🛣️ SAVI")
st.subheader("Sistema de Apoyo para la Valoración Integral de Infraestructura")

st.divider()

# ==========================================================
# Cargar proyecto
# ==========================================================

proyecto = cargar_proyecto()

st.success("Proyecto cargado correctamente.")

# ==========================================================
# Botón principal
# ==========================================================

if st.button("🚀 Ejecutar análisis integral"):

    st.header("📊 Análisis Integral")

    # ======================================================
    # Lectura de perfiles
    # ======================================================

    perfil_real = proyecto["1. Perfil_Topografico"]

    perfil_proyectado = proyecto["2.Perfil_Topografico_Proyectado"]

    # ======================================================
    # Movimiento de tierras
    # ======================================================

    movimiento = analizar_movimiento_tierras(
        perfil_real,
        perfil_proyectado
    )

    # ======================================================
    # Análisis matemático
    # ======================================================

    resultados = analizar_tramos(
        movimiento["tramos"]
    )

    # ======================================================
    # Indicadores generales
    # ======================================================

    st.subheader("📈 Indicadores del Perfil")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Elevación máxima",
            f"{perfil_real['Elevación'].max():.2f} m"
        )

        st.metric(
            "Pendiente máxima",
            f"{perfil_real['Pendiente'].max():.2f} %"
        )

    with col2:

        st.metric(
            "Elevación mínima",
            f"{perfil_real['Elevación'].min():.2f} m"
        )

        st.metric(
            "Pendiente promedio",
            f"{perfil_real['Pendiente'].mean():.2f} %"
        )

    st.divider()

    # ======================================================
    # Modelo matemático
    # ======================================================

    st.header("📐 Modelo Matemático por Tramos")

    st.info(
        f"Se detectaron automáticamente {len(resultados)} tramos de análisis."
    )

    # ======================================================
    # Mostrar análisis de cada tramo
    # ======================================================

    for tramo in resultados:

        st.divider()

        st.subheader(
            f"{tramo['id']} • {tramo['tipo_tramo']} • PK "
            f"{tramo['pk_inicio']:.2f} - {tramo['pk_fin']:.2f}"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Longitud",
                f"{tramo['longitud']:.2f} m"
            )

        with col2:

            st.metric(
                "Altura máxima",
                f"{tramo['altura_maxima']:.2f} m"
            )

        with col3:

            st.metric(
                "Precisión (R²)",
                f"{tramo['r2']*100:.2f}%"
            )

        if tramo["r2"] >= 0.98:

            st.success("Excelente ajuste parabólico.")

        elif tramo["r2"] >= 0.95:

            st.info("Muy buen ajuste.")

        elif tramo["r2"] >= 0.90:

            st.warning("Ajuste aceptable.")

        else:

            st.error("Conviene revisar este tramo.")

        st.markdown("### Función")

        st.latex(
            "f(x)=" + tramo["funcion_latex"]
        )

        st.markdown("### Primera derivada")

        st.latex(
            "f'(x)=" + tramo["derivada_latex"]
        )

        st.caption(
            "La derivada representa la pendiente instantánea del tramo."
        )

        st.markdown("### Integral")

        st.latex(
            r"\int f(x)\,dx=" + tramo["integral_latex"]
        )

        st.caption(
            "La integral permitirá calcular posteriormente áreas y volúmenes de movimiento de tierras."
        )

    st.divider()

    # ======================================================
    # Movimiento de tierras
    # ======================================================

    st.header("🚜 Movimiento de Tierras")

    st.subheader("Comparación entre el perfil real y el perfil proyectado")

    # ======================================================
    # Gráfica comparativa
    # ======================================================

    fig, ax = plt.subplots(figsize=(12, 5))

    ax.plot(
        movimiento["tabla"]["PK"],
        movimiento["tabla"]["Elevación Real"],
        linewidth=2,
        label="Perfil Real"
    )

    ax.plot(
        movimiento["tabla"]["PK"],
        movimiento["tabla"]["Elevación Proyectada"],
        linewidth=2,
        label="Perfil Proyectado"
    )

    # Áreas de corte

    ax.fill_between(

        movimiento["tabla"]["PK"],

        movimiento["tabla"]["Elevación Real"],

        movimiento["tabla"]["Elevación Proyectada"],

        where=movimiento["tabla"]["Elevación Real"] >
        movimiento["tabla"]["Elevación Proyectada"],

        color="red",

        alpha=0.35,

        interpolate=True,

        label="Corte"

    )

    # Áreas de relleno

    ax.fill_between(

        movimiento["tabla"]["PK"],

        movimiento["tabla"]["Elevación Real"],

        movimiento["tabla"]["Elevación Proyectada"],

        where=movimiento["tabla"]["Elevación Real"] <
        movimiento["tabla"]["Elevación Proyectada"],

        color="green",

        alpha=0.35,

        interpolate=True,

        label="Relleno"

    )

    ax.set_xlabel("PK")

    ax.set_ylabel("Elevación (m)")

    ax.set_title("Perfil Topográfico Real vs Perfil Proyectado")

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

    # ======================================================
    # Tabla de comparación
    # ======================================================

    st.dataframe(

        movimiento["tabla"],

        use_container_width=True

    )

    # ======================================================
    # Resumen de volúmenes
    # ======================================================

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Área de Corte",
            f"{movimiento['area_corte']:.2f} m²"
        )

        st.metric(
            "Volumen de Corte",
            f"{movimiento['volumen_corte']:.2f} m³"
        )

    with col2:

        st.metric(
            "Área de Relleno",
            f"{movimiento['area_relleno']:.2f} m²"
        )

        st.metric(
            "Volumen de Relleno",
            f"{movimiento['volumen_relleno']:.2f} m³"
        )

    # ======================================================
    # Resumen de tramos
    # ======================================================

    st.divider()

    st.header("📍 Tramos Detectados")

    resumen = []

    for tramo in movimiento["tramos"]:

       resumen.append({

        "Tramo": tramo["id"],

        "Tipo": tramo["tipo"],

        "PK Inicio": round(tramo["pk_inicio"], 2),

        "PK Fin": round(tramo["pk_fin"], 2),

        "Longitud (m)": round(tramo["longitud"], 2),

        "Altura Máxima (m)": round(tramo["altura_maxima"], 2)

    })

    st.dataframe(

        resumen,

        use_container_width=True,

        hide_index=True

    )

    # ======================================================
    # Meteorología
    # ======================================================

    st.divider()

    st.header("🌦️ Condiciones Meteorológicas")

    meteorologia = analizar_meteorologia(
        proyecto["7. Meteorologia"]
    )

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Temperatura máxima",
            f"{meteorologia['temperatura_maxima']:.1f} °C"
        )

        st.metric(
            "Temperatura promedio",
            f"{meteorologia['temperatura_promedio']:.1f} °C"
        )

        st.metric(
            "Humedad máxima",
            f"{meteorologia['humedad_maxima']:.1f} %"
        )

        st.metric(
            "Humedad promedio",
            f"{meteorologia['humedad_promedio']:.1f} %"
        )
    

    with col2:

        st.metric(
            "Precipitación máxima",
            f"{meteorologia['precipitacion_maxima']:.1f} mm"
        )

        st.metric(
            "Precipitación promedio",
            f"{meteorologia['precipitacion_promedio']:.1f} mm"
        )

        st.metric(
            "Velocidad máxima del viento",
            f"{meteorologia['viento_maximo']:.1f} m/s"
        )

        st.metric(
            "Velocidad promedio del viento",
            f"{meteorologia['viento_promedio']:.1f} m/s"
        )

    st.subheader("Datos meteorológicos")

    st.dataframe(
        meteorologia["tabla"],
        use_container_width=True
    )

        # ======================================================
    # Índice de Susceptibilidad al Deslizamiento (ISD)
    # ======================================================

    st.divider()

    st.header("⛰️ Índice de Susceptibilidad al Deslizamiento")

    isd = calcular_isd(

        tramos=movimiento["tramos"],

        perfil_topografico=proyecto["2.Perfil_Topografico_Proyectado"],

        meteorologia=proyecto["7. Meteorologia"],

        suelos=proyecto["6. Suelos"],

        cobertura=proyecto["5. Cobertura_Vegetal"]


        )

    # ------------------------------------------------------
    # Resumen
    # ------------------------------------------------------

    st.subheader("Resumen")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "ISD Máximo",
            f"{isd['ISD'].max():.3f}"
        )

    with col2:

        st.metric(
            "ISD Promedio",
            f"{isd['ISD'].mean():.3f}"
        )

    with col3:

        st.metric(
            "Mayor Riesgo",
            isd.sort_values("ISD", ascending=False).iloc[0]["Riesgo"]
        )

    st.dataframe(

        isd,

        use_container_width=True,

        hide_index=True

    )

    # ------------------------------------------------------
    # Perfil topográfico coloreado por riesgo
    # ------------------------------------------------------

    st.subheader("Perfil Topográfico con Riesgo por Deslizamiento")

    fig, ax = plt.subplots(figsize=(14,6))

    # Perfil real
    ax.plot(

        movimiento["tabla"]["PK"],

        movimiento["tabla"]["Elevación Real"],

        color="black",

        linewidth=2,

        label="Perfil Real"

    )

    # Perfil proyectado
    ax.plot(

        movimiento["tabla"]["PK"],

        movimiento["tabla"]["Elevación Proyectada"],

        color="blue",

        linewidth=2,

        label="Perfil Proyectado"

    )

    colores = {

        "Muy Bajo": "#2ecc71",

        "Bajo": "#8bc34a",

        "Medio": "#f1c40f",

        "Alto": "#e67e22",

        "Muy Alto": "#e74c3c"

    }

    for _, fila in isd.iterrows():

        color = colores[fila["Riesgo"]]

        datos = movimiento["tabla"]

        tramo = datos[

            (datos["PK"] >= fila["PK Inicio"])

            &

            (datos["PK"] <= fila["PK Fin"])

        ]

        ax.fill_between(

            tramo["PK"],

            tramo["Elevación Real"],

            tramo["Elevación Proyectada"],

            color=color,

            alpha=0.45

        )

        pk_centro = (fila["PK Inicio"] + fila["PK Fin"]) / 2

        elev = tramo["Elevación Proyectada"].mean()

        ax.text(

            pk_centro,

            elev + 2,

            f"{fila['Tramo']}\n{fila['ISD']:.1f}",

            ha="center",

            fontsize=8,

            fontweight="bold"

        )

    ax.set_xlabel("PK")

    ax.set_ylabel("Elevación (m)")

    ax.set_title("Perfil Topográfico con Clasificación del Riesgo de Deslizamiento")

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

    # ======================================================
    # Sensores IoT
    # ======================================================

    st.divider()

    st.header("📡 Sensores IoT y Sistema Inteligente de Pare y Siga")

    sensores = analizar_sensores(

        proyecto["10. Sensores_IoT"]

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Velocidad mínima segura",

            f"{sensores['velocidad_minima']:.2f} km/h"

        )

    with col2:

        st.metric(

            "Tiempo de despeje",

            f"{sensores['tiempo_despeje_min']:.2f} min"

        )

    with col3:

        st.metric(

            "Tiempo recomendado Pare y Siga",

            f"{int(sensores['tiempo_semaforo_seg'])} s"

        )

    st.info(

        f"""
    El punto más crítico del corredor se localiza en el PK
    {sensores['pk_critico']:.2f}.

    En este sector la inclinación alcanza
    {sensores['inclinacion_critica']:.2f}° y la humedad relativa
    {sensores['humedad_critica']:.1f} %.

    Aplicando el modelo matemático de velocidad segura y la
    integración numérica, SAVI estima un tiempo de despeje de
    {sensores['tiempo_despeje_min']:.2f} minutos,
    por lo que recomienda un tiempo de Pare y Siga de
    {int(sensores['tiempo_semaforo_seg'])} segundos.
    """
    )

   # ======================================================
    # Perfil de velocidad segura
    # ======================================================

    st.subheader("📈 Perfil de velocidad segura")

    import matplotlib.pyplot as plt
    import numpy as np

    tabla = sensores["tabla"]

    pk = tabla["PK"]
    vel = tabla["Velocidad Segura"]
    hum = tabla["Humedad relativa"]

    fig, ax1 = plt.subplots(figsize=(12,5))

    # --------------------------------------------------
    # Zonas de riesgo
    # --------------------------------------------------

    ax1.fill_between(

        pk,

        0,

        vel,

        where=(vel > 20),

        alpha=0.25,

        color="green",

        label="Zona segura"

    )

    ax1.fill_between(

        pk,

        0,

        vel,

        where=((vel >= 15) & (vel <= 20)),

        alpha=0.30,

        color="gold",

        label="Precaución"

    )

    ax1.fill_between(

        pk,

        0,

        vel,

        where=(vel < 15),

        alpha=0.35,

        color="red",

        label="Zona crítica"

    )

    # --------------------------------------------------
    # Curva de velocidad
    # --------------------------------------------------

    ax1.plot(

        pk,

        vel,

        linewidth=2.5,

        color="royalblue",

        label="Velocidad segura"

    )

    ax1.set_xlabel("PK (km)")

    ax1.set_ylabel(

        "Velocidad segura (km/h)",

        color="royalblue"

    )

    ax1.tick_params(

        axis="y",

        labelcolor="royalblue"

    )

    ax1.grid(True, alpha=0.3)

    # --------------------------------------------------
    # PK crítico
    # --------------------------------------------------

    pk_critico = sensores["pk_critico"]

    ax1.axvline(

        pk_critico,

        linestyle="--",

        color="black",

        linewidth=2,

        label=f"PK crítico ({pk_critico:.2f})"

    )

    # --------------------------------------------------
    # Humedad relativa
    # --------------------------------------------------

    ax2 = ax1.twinx()

    ax2.plot(

        pk,

        hum,

        color="darkgreen",

        linewidth=2,

        alpha=0.8,

        label="Humedad relativa"

    )

    ax2.set_ylabel(

        "Humedad relativa (%)",

        color="darkgreen"

    )

    ax2.tick_params(

        axis="y",

        labelcolor="darkgreen"

    )

    # --------------------------------------------------
    # Leyenda combinada
    # --------------------------------------------------

    lineas1, etiquetas1 = ax1.get_legend_handles_labels()

    lineas2, etiquetas2 = ax2.get_legend_handles_labels()

    ax1.legend(

        lineas1 + lineas2,

        etiquetas1 + etiquetas2,

        loc="upper right"

    )

    plt.title(

        "Análisis IoT de velocidad segura y humedad relativa"

    )

    st.pyplot(fig)

    st.caption(
    """
    🟢 Velocidad > 20 km/h: operación segura.

    🟡 Velocidad entre 15 y 20 km/h: se recomienda precaución.

    🔴 Velocidad < 15 km/h: zona crítica con posible restricción operacional.
    """
    )

    st.dataframe(

            sensores["tabla"],

            use_container_width=True,

            hide_index=True

        )

    # ======================================================
    # Logística
    # ======================================================

    logistica = analizar_logistica(
        proyecto["11. Logistica"]
    )

    # ======================================================
    # LOGÍSTICA
    # ======================================================

    st.divider()

    st.header("🚛 Logística del Proyecto")

    st.subheader("Resumen")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Velocidad promedio",

            f"{logistica['velocidad_promedio']:.2f} km/h"

        )

    with col2:

        st.metric(

            "Tiempo acumulado",

            f"{logistica['tiempo_acumulado']:.2f}"

        )

    with col3:

        st.metric(

            "Carga máxima",

            f"{logistica['carga_maxima']:.1f} t"

        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Velocidad mínima",

            f"{logistica['velocidad_minima']:.2f} km/h"

    )

    with col2:

        st.metric(

            "PK velocidad mínima",

            f"{logistica['pk_velocidad_minima']:.2f}"

        )

    with col3:

        st.metric(

            "Correlación V-C",

            f"{logistica['correlacion_velocidad_carga']:.3f}"

        )

    
    st.subheader("📈 Perfil Logístico")

    import matplotlib.pyplot as plt

    fig, ax1 = plt.subplots(figsize=(12,5))

    tabla = logistica["tabla"]

    # --------------------------------------------------
    # Velocidad
    # --------------------------------------------------

    ax1.plot(

        tabla["PK"],

        tabla["Velocidad promedio"],

        color="royalblue",

        linewidth=2,

        label="Velocidad"

    )

    ax1.set_xlabel("PK (km)")

    ax1.set_ylabel(

        "Velocidad (km/h)",

        color="royalblue"

    )

    ax1.tick_params(

        axis="y",

        labelcolor="royalblue"

    )

    ax1.grid(True, alpha=0.3)

    # --------------------------------------------------
    # PK crítico
    # --------------------------------------------------

    ax1.axvline(

        logistica["pk_velocidad_minima"],

        color="red",

        linestyle="--",

        linewidth=2,

        label="Velocidad mínima"

    )

    # --------------------------------------------------
    # Tiempo
    # --------------------------------------------------

    ax2 = ax1.twinx()

    ax2.plot(

        tabla["PK"],

        tabla["Tiempo de recorrido"],

        color="darkgreen",

        linewidth=2,

        label="Tiempo"

    )

    ax2.set_ylabel(

        "Tiempo de recorrido",

        color="darkgreen"

    )

    ax2.tick_params(

        axis="y",

        labelcolor="darkgreen"

    )

    lineas1, etiquetas1 = ax1.get_legend_handles_labels()

    lineas2, etiquetas2 = ax2.get_legend_handles_labels()

    ax1.legend(

        lineas1 + lineas2,

        etiquetas1 + etiquetas2,

        loc="upper right"

    )

    st.pyplot(fig)

    st.subheader("🧠 Hallazgos")

    st.success(

    f"""
    • La velocidad mínima se presenta en el PK {logistica['pk_velocidad_minima']:.2f}.

    • La velocidad promedio del corredor es de {logistica['velocidad_promedio']:.2f} km/h.

    • La carga máxima registrada es de {logistica['carga_maxima']:.1f} toneladas.

    • El tiempo acumulado del recorrido, obtenido mediante integración numérica,
    es de {logistica['tiempo_acumulado']:.2f}.

    • La correlación entre velocidad y carga es
    {logistica['correlacion_velocidad_carga']:.3f}.
    """
    )


    st.subheader("📋 Tabla logística")

    st.dataframe(

        logistica["tabla"],

        use_container_width=True,

        hide_index=True

    )

    # ======================================================
    # Costos
    # ======================================================

    costos = analizar_costos(
        proyecto["12. Costos"]
    )

    # ======================================================
    # COSTOS
    # ======================================================

    st.divider()

    st.header("💰 Costos del Proyecto")

    st.subheader("Resumen")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Costo acumulado",
            f"{costos['costo_total_acumulado']:.2f}"
    )

    with col2:

        st.metric(
            "Costo máximo",
            f"{costos['costo_total_maximo']:.2f}"
        )

    with col3:

        st.metric(
            "Costo promedio",
            f"{costos['costo_total_promedio']:.2f}"
        )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "% Movimiento",
            f"{costos['porcentaje_movimiento']:.2f}%"
        )

    with col2:

        st.metric(
            "% Clima",
            f"{costos['porcentaje_clima']:.2f}%"
        )

    with col3:

        st.metric(
            "PK costo máximo",
            f"{costos['pk_costo_maximo']:.2f}"
        )

    st.subheader("📈 Perfil de Costos")

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(12,5))

    tabla = costos["tabla"]

    ax.plot(
        tabla["PK"],
        tabla["Costo de movimiento de tierras"],
        label="Movimiento de tierras",
        linewidth=2
    )

    ax.plot(
        tabla["PK"],
        tabla["Costo asociado a condiciones climáticas"],
        label="Condiciones climáticas",
        linewidth=2
    )

    ax.plot(
        tabla["PK"],
        tabla["Costo total estimado"],
        label="Costo total",
        linewidth=3
    )

    ax.axvline(
        costos["pk_costo_maximo"],
        color="red",
        linestyle="--",
        label="Costo máximo"
    )

    ax.set_xlabel("PK (km)")
    ax.set_ylabel("Costo")

    ax.grid(True, alpha=0.3)

    ax.legend()

    st.pyplot(fig)

    st.subheader("🧠 Hallazgos")

    st.success(f"""
    • El costo acumulado del proyecto es de {costos['costo_total_acumulado']:.2f}.

    • El costo máximo ocurre en el PK {costos['pk_costo_maximo']:.2f}.

    • El {costos['porcentaje_movimiento']:.2f}% del presupuesto corresponde al movimiento de tierras.

    • El {costos['porcentaje_clima']:.2f}% corresponde a las condiciones climáticas.

    • La mayor variación del costo se presenta alrededor del PK {costos['pk_gradiente_maximo']:.2f}.
    """)

    st.subheader("📋 Tabla de Costos")

    st.dataframe(
        costos["tabla"],
        use_container_width=True,
        hide_index=True
    )


    # ======================================================
    # Motor de reglas
    # ======================================================

    reglas = evaluar_reglas(

        resultados,

        movimiento

    )

    # ======================================================
    # Diagnóstico
    # ======================================================

    st.divider()

    st.header("🧠 Diagnóstico Técnico")

    interpretacion = interpretar_modelo(

        reglas=reglas,

        movimiento=movimiento,

        resultados=resultados,

        isd=isd,
       
        sensores=sensores,

        logistica=logistica,

        costos=costos,

        meteorologia=meteorologia

        )

    for texto in interpretacion:

        st.write("✅", texto)

    st.success("Motor de reglas ejecutado correctamente.")

    # ======================================================
    # PANEL EJECUTIVO SAVI
    # ======================================================

    st.divider()

    st.header("📊 Panel Ejecutivo SAVI")

    st.info(
    """
    Los siguientes indicadores integran los resultados obtenidos por los módulos
    matemático, meteorológico, geotécnico, logístico y económico del sistema SAVI.
    El objetivo es identificar visualmente los sectores donde convergen las
    condiciones más críticas del corredor vial. 
    """
    )

    # ======================================================
    # KPIs
    # ======================================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        riesgo_max = isd["Riesgo"].iloc[
            isd["ISD"].idxmax()
        ]

        st.metric(
            "Riesgo máximo",
            riesgo_max
        )

    with col2:

        st.metric(
            "Velocidad mínima",
            f"{logistica['velocidad_minima']:.1f} km/h"
        )

    with col3:

        st.metric(
            "Costo acumulado",
            f"{costos['costo_total_acumulado']:.0f}"
        )

    with col4:

        st.metric(
            "Tiempo despeje",
            f"{sensores['tiempo_despeje_min']:.1f} min"
        )

    # ======================================================
    # Preparación de datos
    # ======================================================

    pk = sensores["tabla"]["PK"]

    pendiente = abs(
        sensores["tabla"]["Inclinación"]
    )

    humedad = sensores["tabla"]["Humedad relativa"]

    velocidad = logistica["tabla"]["Velocidad promedio"]

    costo = costos["tabla"]["Costo total estimado"]

    isd_interp = np.interp(

        pk,

        (
            isd["PK Inicio"]
            +
            isd["PK Fin"]
        ) / 2,

        isd["ISD"]

    )

    # ======================================================
    # Normalización
    # ======================================================

    def normalizar(x):

        return (
            x - x.min()
        ) / (
            x.max() - x.min()
        )

    pendiente_n = normalizar(pendiente)

    humedad_n = normalizar(humedad)

    velocidad_n = normalizar(velocidad)

    costo_n = normalizar(costo)

    isd_n = normalizar(isd_interp)

    # ======================================================
    # Gráfica integrada
    # ======================================================

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
        pk,
        pendiente_n,
        linewidth=2,
        label="Pendiente"
    )

    ax.plot(
        pk,
        humedad_n,
        linewidth=2,
        label="Humedad"
    )

    ax.plot(
        pk,
        isd_n,
        linewidth=3,
        label="ISD"
    )

    ax.plot(
        pk,
        velocidad_n,
        linewidth=2,
        label="Velocidad"
    )

    ax.plot(
        pk,
        costo_n,
        linewidth=2,
        label="Costo"
    )

    # ======================================================
    # Tramo crítico
    # ======================================================

    criticidad = (
        pendiente_n
        + humedad_n
        + isd_n
        + costo_n
        - velocidad_n
    )

    pk_critico = pk.iloc[
        criticidad.argmax()
    ]

    ax.axvspan(

        pk_critico-1,

        pk_critico+1,

        alpha=0.20,

        label="Zona crítica"

    )

    ax.set_title(
        "Convergencia de variables críticas del corredor"
    )

    ax.set_xlabel(
        "PK (km)"
    )

    ax.set_ylabel(
        "Variables normalizadas"
    )

    ax.grid(True)

    ax.legend()

    st.pyplot(fig)

    # ======================================================
    # Índice de criticidad
    # ======================================================

    st.subheader("🔴 Índice de criticidad del corredor")

    fig2, ax2 = plt.subplots(figsize=(12,2.5))

    ax2.fill_between(

        pk,

        criticidad,

        alpha=0.6

    )

    ax2.set_xlabel("PK")

    ax2.set_ylabel("Índice")

    ax2.grid(True)

    st.pyplot(fig2)

    # ======================================================
    # Hallazgos automáticos
    # ======================================================

    st.subheader("📋 Hallazgos automáticos")

    velocidad_reduccion = (

        (
            logistica["velocidad_promedio"]
            -
            logistica["velocidad_minima"]

        )

        /

        logistica["velocidad_promedio"]

    )*100

    hallazgos = [

        f"El tramo más crítico del corredor se localiza aproximadamente alrededor del PK {pk_critico:.1f}, donde convergen elevadas pendientes, alta humedad, mayor susceptibilidad a deslizamientos y aumento del costo de construcción.",

        f"La velocidad promedio disminuye aproximadamente un {velocidad_reduccion:.1f}% respecto al promedio del corredor, indicando un posible cuello de botella logístico.",

        f"El mayor costo del proyecto se registra cerca del PK {costos['pk_costo_maximo']:.1f}.",

        f"El ISD alcanza la categoría {riesgo_max} en el sector de mayor criticidad.",

    ]

    if humedad.max()>100:

        hallazgos.append(

            "Se identificaron registros de humedad relativa superiores al 100%, lo que sugiere posibles inconsistencias de calibración o captura de datos en algunos sensores."

        )

    for h in hallazgos:

        st.write("✔",h)


    # ======================================================
    # Recomendaciones
    # ======================================================

    st.divider()

    st.header("💡 Recomendaciones del Sistema")

    recomendaciones = generar_recomendaciones(

        reglas=reglas,

        movimiento=movimiento,

        resultados=resultados,

        isd=isd,

        meteorologia=meteorologia,

        sensores=sensores,

        logistica=logistica,

        costos=costos

    )

    # Mostrar recomendaciones en un único bloque

    texto_recomendaciones = "\n\n".join(

        f"**{i}.** {r}"

        for i, r in enumerate(recomendaciones, 1)

    )

    st.info(texto_recomendaciones)