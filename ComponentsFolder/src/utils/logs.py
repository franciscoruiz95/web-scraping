# src/utils/logs.py
import os
import sys
from datetime import datetime
 
def build_log_path(prefix="logsCitas", folder="logs", with_time=False):
    """
    Devuelve la ruta del archivo de log.
    - with_time=False -> logsCitas_YYYYMMDD.log (un archivo por día)
    - with_time=True  -> logsCitas_YYYYMMDD_HHMMSS.log (uno por ejecución)
    """
    os.makedirs(folder, exist_ok=True)
    fmt = "%Y%m%d_%H%M%S" if with_time else "%Y%m%d"
    stamp = datetime.now().strftime(fmt)
    return os.path.join(folder, f"{prefix}_{stamp}.log")
 
class TeeToFile:
    """
    Redirige stdout y stderr a consola y archivo simultáneamente.
    Útil para capturar prints sin modificar el código existente.
    """
    def __init__(self, filepath, mode="a", encoding="utf-8"):
        self.filepath = filepath
        self.file = open(filepath, mode, encoding=encoding)
        self._stdout = sys.stdout
        self._stderr = sys.stderr
 
    def write(self, data):
        self._stdout.write(data)
        self.file.write(data)
 
    def flush(self):
        self._stdout.flush()
        self.file.flush()
 
    def __enter__(self):
        sys.stdout = self
        sys.stderr = self
        return self
 
    def __exit__(self, exc_type, exc, tb):
        sys.stdout = self._stdout
        sys.stderr = self._stderr
        self.file.close()