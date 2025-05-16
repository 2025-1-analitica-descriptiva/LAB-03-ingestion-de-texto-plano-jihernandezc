"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import pandas as pd
import re


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.


    """
    with open("files/input/clusters_report.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Encontrar la línea de las columnas y limpiar los nombres
    header_idx = 0
    for i, line in enumerate(lines):
        if "Cluster" in line and "Palabras clave" in line:
            header_idx = i
            break
    header_line = lines[header_idx]
    header_line2 = lines[header_idx + 1]

    # Unir las dos líneas del encabezado y limpiar
    header = (header_line.rstrip() + " " + header_line2.rstrip()).lower()
    header = re.sub(r"\s+", " ", header)
    columns = [
        "cluster",
        "cantidad_de_palabras_clave",
        "porcentaje_de_palabras_clave",
        "principales_palabras_clave",
    ]

    # Procesar las filas de datos
    data = []
    current_row = []
    for line in lines[header_idx + 2 :]:
        if re.match(r"\s*$", line):
            continue  # Saltar líneas vacías
        # Si la línea comienza con un número, es una nueva fila
        if re.match(r"\s*\d+", line):
            if current_row:
                data.append(current_row)
            current_row = [line.rstrip()]
        else:
            # Es una continuación de la fila anterior
            if current_row:
                current_row.append(line.rstrip())
    if current_row:
        data.append(current_row)

    # Procesar cada fila para extraer los campos
    rows = []
    for row in data:
        full_row = " ".join(row)
        # Extraer los campos usando regex
        match = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+)\s+%\s+(.+)", full_row)
        if match:
            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = float(match.group(3).replace(",", "."))
            palabras = match.group(4)
            # Limpiar palabras clave: quitar espacios extra y separar por coma y espacio
            palabras = re.sub(r"\s+", " ", palabras)
            palabras = palabras.replace(".", "")
            palabras = ", ".join([p.strip() for p in palabras.split(",")])
            rows.append([cluster, cantidad, porcentaje, palabras])

    df = pd.DataFrame(rows, columns=columns)
    return df