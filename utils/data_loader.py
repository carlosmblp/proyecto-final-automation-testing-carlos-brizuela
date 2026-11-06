import json
from pathlib import Path


RUTA_PROYECTO = Path(__file__).resolve().parents[1]


def cargar_json(nombre_archivo):
    """Lee un archivo JSON de la carpeta data del proyecto."""
    ruta = RUTA_PROYECTO / "data" / nombre_archivo
    return json.loads(ruta.read_text(encoding="utf-8"))
