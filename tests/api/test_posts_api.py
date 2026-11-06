import logging

import requests

from utils.data_loader import cargar_json


logger = logging.getLogger(__name__)
API_BASE_URL = "https://jsonplaceholder.typicode.com"
TIMEOUT_SEGUNDOS = 10
DATOS_API = cargar_json("api_payloads.json")


def test_obtener_post_existente():
    url = f"{API_BASE_URL}/posts/1"
    logger.info("GET %s", url)
    respuesta = requests.get(url, timeout=TIMEOUT_SEGUNDOS)

    assert respuesta.status_code == 200
    post = respuesta.json()
    assert isinstance(post["id"], int)
    assert post["id"] == 1
    assert isinstance(post["userId"], int)
    assert post["title"].strip()
    assert post["body"].strip()


def test_crear_post():
    url = f"{API_BASE_URL}/posts"
    payload = DATOS_API["nuevo_post"]
    logger.info("POST %s", url)
    respuesta = requests.post(
        url,
        json=payload,
        timeout=TIMEOUT_SEGUNDOS,
    )

    assert respuesta.status_code == 201
    post_creado = respuesta.json()
    assert isinstance(post_creado["id"], int)
    assert post_creado["title"] == payload["title"]
    assert post_creado["body"] == payload["body"]
    assert post_creado["userId"] == payload["userId"]


def test_eliminar_post():
    url = f"{API_BASE_URL}/posts/1"
    logger.info("DELETE %s", url)
    respuesta = requests.delete(url, timeout=TIMEOUT_SEGUNDOS)

    assert respuesta.status_code == 200
    assert respuesta.json() == {}


def test_endpoint_de_error_devuelve_404():
    url = "https://httpbin.org/status/404"
    logger.info("GET %s para validar una respuesta de error", url)
    respuesta = requests.get(url, timeout=TIMEOUT_SEGUNDOS)

    assert respuesta.status_code == 404
