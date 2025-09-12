# src/core/server.py
 
import os
import csv
from config.settings import CONFIG
 
def guardar_quotes(quotes, driver):
    output_path = CONFIG["out_dir"]
    screenshot_path = CONFIG["screenshot_dir"]
 
    os.makedirs(output_path, exist_ok=True)
    os.makedirs(screenshot_path, exist_ok=True)
 
    archivo_csv = os.path.join(output_path, CONFIG["csv_name"])
    archivo_img = os.path.join(screenshot_path, CONFIG["screenshot_name"])
 
    with open(archivo_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["text", "author"])
        writer.writeheader()
        writer.writerows(quotes)
 
    driver.save_screenshot(archivo_img)
    print(f"📦 Guardadas {len(quotes)} frases en {archivo_csv}.")