# src/utils/metrics.py
 
import os
import csv
from datetime import datetime
from config.settings import CONFIG
 
def guardar_metricas_csv(metricas_por_pagina):
    """
    Guarda las métricas obtenidas por página en un archivo CSV dentro del directorio de datos.
    """
    fecha_hora = datetime.now().strftime("%Y%m%d_%H%M%S")
    ruta_metricas = CONFIG.get("metrics_dir", "data/outputs")
    os.makedirs(ruta_metricas, exist_ok=True)
 
    archivo_csv = os.path.join(ruta_metricas, f"metricas_{fecha_hora}.csv")
 
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["pagina", "quotes_extraidas", "quotes_nuevas"])
        writer.writeheader()
        writer.writerows(metricas_por_pagina)
 
    print(f"📈 Métricas guardadas en {archivo_csv}")