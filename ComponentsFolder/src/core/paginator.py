# src/core/paginator.py
 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
 
 
from src.utils.metrics import guardar_metricas_csv  # ← Importa desde utils
from config.settings import CONFIG
from .scraper import iniciar_driver, cerrar_driver
from .server import guardar_quotes

def cargar_pagina(driver, wait, url):
    """Carga una URL específica y espera a que aparezcan las citas."""
    driver.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".quote")))
    print(f"🌐 Cargando página: {url}")

def extraer_quotes(driver):
    """Extrae todas las citas visibles en la página actual."""
    cards = driver.find_elements(By.CSS_SELECTOR, ".quote")
    print(f"💬 Quotes encontradas: {len(cards)}")
    quotes = [
        {
            "text": q.find_element(By.CSS_SELECTOR, "span.text").text,
            "author": q.find_element(By.CSS_SELECTOR, "small.author").text
        }
        for q in cards
    ]
 
    # (Opcional, diapositiva 28) Filtrar citas cortas por longitud mínima.
    min_len = CONFIG.get("min_quote_len", 0)
    # Filtra y conserva únicamente las citas cuyo texto tiene una longitud mayor o igual a 'min_len'.
    quotes = [q for q in quotes if len(q["text"]) >= min_len]
 
    return quotes

def siguiente_pagina(driver, wait):
    """Avanza a la siguiente página usando el botón 'Next', espera el cambio de URL (diapositiva 26)."""
    boton_next = driver.find_elements(By.CSS_SELECTOR, "li.next > a")
    if boton_next:
        old_url = driver.current_url
        boton_next[0].click()
        wait.until(EC.url_changes(old_url))
        return True
    return False

def ejecutar_pipeline_paginacion():
    """Función principal que automatiza la navegación paginada y extrae datos (diapositiva 24)."""
    driver, wait = iniciar_driver()
    wait._timeout = CONFIG["timeout"]
 
    quotes_totales = []
    urls_visitadas = set() # Buena práctica para evitar bucles infinitos (diapositiva 27)
    metricas_por_pagina = [] # Métricas detalladas por página (diapositiva 28)
   
    try:
        url_inicial = f"{CONFIG['base_url']}{CONFIG['start_page']}"
        cargar_pagina(driver, wait, url_inicial)
 
        for pagina in range(CONFIG["max_pages"]):
            url_actual = driver.current_url
            print(f"📖 Página actual ({pagina + 1}): {url_actual}")
 
            # Evita bucle infinito si la URL se repite (diapositiva 27)
            if url_actual in urls_visitadas:
                print("🔁 URL repetida detectada, cortando el bucle.")
                break
            urls_visitadas.add(url_actual)
 
            quotes_pagina = extraer_quotes(driver)
 
            # Deduplicación de citas, elimina resultados repetidos (diapositiva 28)
            citas_previas = set(q["text"] for q in quotes_totales)
 
            nuevas_quotes = [q for q in quotes_pagina if q["text"] not in citas_previas]
 
            quotes_totales.extend(nuevas_quotes)
 
            # Registro de métricas para análisis posterior (diapositiva 28)
            metricas_por_pagina.append({
                "pagina": pagina + 1,
                "quotes_extraidas": len(quotes_pagina),
                "quotes_nuevas": len(nuevas_quotes)
            })
 
            # Límite máximo de citas a extraer
            if len(quotes_totales) >= CONFIG["max_items"]:
                print("⚠️ Límite máximo de citas alcanzado.")
                quotes_totales = quotes_totales[:CONFIG["max_items"]]
                break
 
            # Manejo de errores al avanzar página y captura de evidencia mínima (diapositiva 29)
            try:
                if not siguiente_pagina(driver, wait):
                    print("⛔ No existe botón 'Next', terminando.")
                    break
            except TimeoutException:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                screenshot_fallo = os.path.join(CONFIG["screenshot_dir"], f"error_pagina_{pagina+1}_{timestamp}.png")
                os.makedirs(CONFIG["screenshot_dir"], exist_ok=True)
                driver.save_screenshot(screenshot_fallo)
                print(f"❌ Error navegando, screenshot guardado: {screenshot_fallo}")
                break
 
        guardar_quotes(quotes_totales, driver)
 
        # Reporte final de métricas
        print("📊 Métricas por página:")
        for metrica in metricas_por_pagina:
            print(f"Página {metrica['pagina']}: {metrica['quotes_extraidas']} extraídas, {metrica['quotes_nuevas']} nuevas.")
 
        # Guardar métricas en CSV usando función reutilizable de utils/metrics.py
        guardar_metricas_csv(metricas_por_pagina)
 
    finally:
        cerrar_driver(driver)