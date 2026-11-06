# Proyecto Final de Automatización QA

**Autor:** Carlos Mario Brizuela

## Propósito

A partir de la pre-entrega, este proyecto reúne pruebas de interfaz con
Selenium WebDriver y pruebas de API con Requests, organizadas con Pytest.
La interfaz cubre login, catálogo, carrito y checkout de SauceDemo.

Sitio utilizado: https://www.saucedemo.com/

## Tecnologías utilizadas

- Python.
- Selenium WebDriver.
- Pytest.
- pytest-html.
- Requests.
- Google Chrome.
- Git y GitHub para control de versiones.

## Estructura del proyecto

- `pages/login_page.py`: elementos y acciones de la página de login.
- `pages/inventory_page.py`: elementos y acciones del catálogo.
- `pages/cart_page.py`: consultas de los productos del carrito.
- `pages/checkout_information_page.py`: formulario de datos del comprador.
- `pages/checkout_overview_page.py`: resumen de compra y confirmación.
- `pages/checkout_complete_page.py`: confirmación final del checkout.
- `tests/ui/test_saucedemo.py`: pruebas POM de login, catálogo, carrito y checkout.
- `tests/api/test_posts_api.py`: pruebas GET, POST y DELETE para JSONPlaceholder
  y una respuesta 404 controlada de HTTPBin.
- `tests/conftest.py`: fixture del navegador, logs y capturas ante fallos.
- `tests/test_evidencias.py`: prueba con fallo intencional para verificar capturas.
- `utils/funciones.py`: función de compatibilidad que delega el login a `LoginPage`.
- `utils/data_loader.py`: lectura de datos JSON desde `data/`.
- `data/usuarios.json`: credenciales, escenarios negativos y datos de checkout.
- `data/api_payloads.json`: payload para crear un post mediante la API.
- `utils/__init__.py`: identifica el paquete de funciones auxiliares.
- `reports/reporte_evidencias.html`: reporte de la prueba de captura intencional.
- `reports/reporte_13_casos_antes_de_consolidar.html`: reporte histórico de la
  ejecución anterior a retirar tres pruebas duplicadas.
- `reports/ejecucion.log`: log de la última ejecución.
- `reports/capturas/`: capturas automáticas ante fallos.
- `requirements.txt`: dependencias del proyecto.
- `pytest.ini`: configuración de las pruebas y los logs.
- `.gitignore`: archivos excluidos del control de versiones.

## Pruebas implementadas

### Login exitoso

- Abre la página de login.
- Ingresa el usuario `standard_user` y la contraseña `secret_sauce`.
- Utiliza esperas explícitas.
- Verifica la redirección a `/inventory.html`.
- Valida los textos visibles `Products` y `Swag Labs`.

### Login con credenciales inválidas

- Lee dos conjuntos de datos desde `data/usuarios.json`.
- Ejecuta el escenario con `pytest.mark.parametrize`.
- Comprueba el mensaje esperado para usuario bloqueado y credenciales incorrectas.

### Verificación del catálogo

- Inicia sesión.
- Valida el título `Products`.
- Comprueba que exista al menos un producto visible.
- Obtiene y muestra en la terminal el nombre y precio del primero.
- Verifica la presencia del menú, el filtro de ordenamiento y el enlace al carrito.

### Agregado de un producto al carrito

- Inicia sesión y verifica que el carrito esté vacío.
- Guarda el nombre y precio del primer producto visible.
- Agrega ese producto al carrito.
- Verifica que el contador aumente de cero a uno.
- Navega a `/cart.html`.
- Comprueba que haya un único producto visible.
- Valida su nombre, precio y cantidad.

### Compra completa

- Agrega un producto y avanza desde el carrito hasta el checkout.
- Completa los datos del comprador con valores del archivo JSON.
- Verifica el producto en el resumen y el mensaje de compra completada.

### Pruebas de API

- `GET /posts/1`: valida el estado HTTP y los campos principales del post.
- `POST /posts`: envía un payload de `data/api_payloads.json` y valida la respuesta.
- `DELETE /posts/1`: valida el estado HTTP y el cuerpo JSON devuelto.
- `GET /status/404` en HTTPBin: comprueba el manejo de una respuesta de error.

JSONPlaceholder simula las operaciones de escritura: la respuesta permite
validar el flujo, pero los datos creados o eliminados no se guardan de forma
permanente en el servidor.

Cada prueba de UI utiliza una sesión nueva de Chrome y realiza su propio login.
Los tests de API no dependen del navegador ni de otros tests.

Las pruebas de interfaz utilizan Page Object Model: las acciones y los
localizadores de cada página están en `pages/`; los tests contienen los
escenarios y sus validaciones. El login inválido se parametriza con dos
conjuntos de datos externos. Hay cinco funciones de prueba de UI; la
parametrización produce seis ejecuciones de UI, más cuatro pruebas de API:
10 ejecuciones en la suite principal.

## Requisitos previos

- Python instalado y disponible mediante el comando `py` en Windows.
- Google Chrome instalado.
- Acceso a Internet para instalar dependencias, acceder a SauceDemo
  y permitir la gestión del controlador de Chrome por Selenium.

Los comandos siguientes se ejecutan desde la raíz del proyecto,
donde se encuentran `requirements.txt` y `pytest.ini`.

## Instalación en Windows

Crear el entorno virtual:

```powershell
py -m venv .venv
```

Instalar las dependencias:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Se utiliza directamente el Python del entorno virtual, por lo que
no es necesario activarlo.

## Ejecutar las pruebas

Ejecutar las pruebas y generar un reporte HTML:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s --html=reports/reporte.html --self-contained-html
```

- `-v`: muestra los nombres y resultados de las pruebas.
- `-s`: permite ver en la terminal los datos mostrados con `print()`.
- `--html`: indica dónde guardar el reporte.
- `--self-contained-html`: genera un reporte HTML con sus recursos incorporados.

Abrir `reports/reporte.html` en el navegador para consultar los resultados.

### Ejecutar una prueba individual

Login:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_saucedemo.py::test_login_exitoso -v
```

Catálogo:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_saucedemo.py::test_catalogo_productos -v -s
```

Carrito:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_saucedemo.py::test_agregar_producto_al_carrito -v -s
```

Compra completa:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/ui/test_saucedemo.py::test_compra_completa_checkout -v
```

Solo pruebas de API:

```powershell
.\.venv\Scripts\python.exe -m pytest tests/api -v
```

## Logs de ejecución

Los logs aparecen en la terminal y se guardan en `reports/ejecucion.log`.

Incluyen:

- Inicio de cada prueba.
- Apertura y cierre de Chrome.
- Resultado de la prueba.
- Detalle de los fallos.
- Ubicación de las capturas generadas o errores al capturarlas.

Cuando falla una prueba de UI, la captura se guarda como PNG en
`reports/capturas/` y se agrega al reporte HTML.

El archivo de log se reemplaza en cada ejecución.
Los mensajes mostrados con `print()` no se agregan automáticamente al log.

## Capturas automáticas ante fallos

Cuando una prueba falla durante su preparación o ejecución y Chrome
sigue disponible, se guarda una captura PNG en `reports/capturas/`.

El nombre incluye la prueba, la etapa, la fecha y la hora. La captura también
queda incluida en el reporte HTML como imagen incrustada.

Si Chrome no llega a abrirse, no es posible obtener una captura.
Si todas las pruebas pasan, no se generan capturas nuevas.

### Comprobar el funcionamiento de las capturas

El archivo `tests/test_evidencias.py` contiene una prueba que abre SauceDemo
y provoca un fallo intencional con `assert False`.

Esta prueba está excluida de las ejecuciones habituales mediante
la siguiente configuración en `pytest.ini`:

```ini
addopts = --ignore=tests/test_evidencias.py
```

Para ejecutarla, anular esa opción solamente para esta ejecución:

```powershell
.\.venv\Scripts\python.exe -m pytest -o addopts="" tests/test_evidencias.py -v
```

El resultado esperado es `1 failed`, porque el fallo es intencional.

Verificar que:

1. Se haya creado un PNG en `reports/capturas/`.
2. El log registre el fallo y el mensaje `Captura guardada`.
3. La imagen muestre la página abierta al momento del fallo.

Después, ejecutar nuevamente las pruebas normales para dejar
actualizados el log y el reporte HTML:

```powershell
.\.venv\Scripts\python.exe -m pytest -v -s --html=reports/reporte.html --self-contained-html
```

## Resultados de ejecución

El 6 de noviembre de 2026, la suite informó `13 passed in 43.22s` en Windows.
Ese total incluía tres pruebas de la pre-entrega que repetían login, catálogo
y carrito sin utilizar Page Object Model. Se retiró ese archivo duplicado para
que la suite final use los Page Objects y evite ejecutar los mismos flujos dos
veces. La suite actual tiene 10 ejecuciones: seis de UI y cuatro de API.

La prueba de captura se ejecuta por separado y termina con `1 failed` a
propósito. `reports/reporte_evidencias.html` registra ese fallo y muestra la
captura incrustada. Volvé a ejecutar la suite principal para generar el nuevo
`reports/reporte.html` con los 10 casos de la estructura consolidada.
