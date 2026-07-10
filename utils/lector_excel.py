# utils/lector_excel.py

import pandas as pd


def cargar_proyecto():
    """
    Carga todas las hojas del archivo datos.xlsx
    y las devuelve en un diccionario.
    """

    ruta = "data/datos.xlsx"

    excel = pd.ExcelFile(ruta)

    proyecto = {}

    for hoja in excel.sheet_names:

        proyecto[hoja] = pd.read_excel(
            ruta,
            sheet_name=hoja
        )

    return proyecto