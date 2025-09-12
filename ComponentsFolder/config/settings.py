# config/settings.py
 
CONFIG = {
    # URLs de scraping
    "base_url": "https://quotes.toscrape.com",
    "start_page": "/page/1/",
 
    # Configuración de la extracción
    "max_pages": 3,                        # Número máximo de páginas a recorrer
    "max_items": 30,                       # Máximo total de quotes a extraer (si deseas limitarlo)
    "timeout": 10,                         # Tiempo máximo espera explícita Selenium (WebDriverWait)
 
    # Paths de salida
    "out_dir": "data/outputs",             # Directorio resultados CSV
    "screenshot_dir": "data/screenshots",  # Directorio capturas pantalla
    "csv_name": "quotes.csv",              # Archivo CSV de salida
    "screenshot_name": "quotes_last.png",  # Archivo captura final
 
    # Encabezados y metadatos (útil si haces requests directas con requests o scrapy)
    "headers": {
        "User-Agent": "Analyt-IA-WS/1.0 (+contacto@analyt-ia.com)"
    },
 
    # Otras configuraciones (opcionales para lógica adicional)
    "min_quote_len": 15,                    # Ejemplo filtro por longitud mínima (opcional)
    "metrics_dir": "data/outputs"           # Directorio resultados Métricas
}