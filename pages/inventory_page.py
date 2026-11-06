from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.cart_page import CartPage


class InventoryPage:
    """Acciones y consultas de la página del catálogo de SauceDemo."""

    URL_PATH = "/inventory.html"
    TITULO = (By.CLASS_NAME, "title")
    MARCA = (By.CLASS_NAME, "app_logo")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    BOTON_MENU = (By.ID, "react-burger-menu-btn")
    FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")
    ENLACE_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    INDICADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_carga(self):
        self.wait.until(
            lambda driver: driver.current_url.endswith(self.URL_PATH)
        )
        self.wait.until(EC.visibility_of_element_located(self.TITULO))
        return self

    def esta_activa(self):
        return self.driver.current_url.endswith(self.URL_PATH)

    def obtener_titulo(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TITULO)
        ).text

    def obtener_marca(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MARCA)
        ).text

    def obtener_productos(self):
        return self.wait.until(
            EC.visibility_of_any_elements_located(self.PRODUCTOS)
        )

    def contar_productos(self):
        return len(self.obtener_productos())

    def obtener_datos_primer_producto(self):
        producto = self.obtener_productos()[0]
        nombre = producto.find_element(
            By.CLASS_NAME, "inventory_item_name"
        ).text
        precio = producto.find_element(
            By.CLASS_NAME, "inventory_item_price"
        ).text
        return {"nombre": nombre, "precio": precio}

    def menu_esta_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.BOTON_MENU)
        ).is_displayed()

    def filtro_esta_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.FILTRO_ORDEN)
        ).is_displayed()

    def enlace_carrito_esta_visible(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.ENLACE_CARRITO)
        ).is_displayed()

    def agregar_primer_producto_al_carrito(self):
        producto = self.obtener_productos()[0]
        datos = self.obtener_datos_primer_producto()
        boton_agregar = producto.find_element(By.TAG_NAME, "button")
        self.wait.until(lambda _driver: boton_agregar.is_enabled())
        boton_agregar.click()
        self.wait.until(
            EC.text_to_be_present_in_element(self.INDICADOR_CARRITO, "1")
        )
        return datos

    def obtener_cantidad_en_carrito(self):
        indicadores = self.driver.find_elements(*self.INDICADOR_CARRITO)
        return int(indicadores[0].text) if indicadores else 0

    def abrir_carrito(self):
        self.wait.until(
            EC.element_to_be_clickable(self.ENLACE_CARRITO)
        ).click()
        return CartPage(self.driver).esperar_carga()
