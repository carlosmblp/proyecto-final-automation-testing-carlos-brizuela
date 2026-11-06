from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.checkout_information_page import CheckoutInformationPage


class CartPage:
    """Consultas de los productos agregados al carrito."""

    URL_PATH = "/cart.html"
    ITEMS = (By.CLASS_NAME, "cart_item")
    BOTON_CHECKOUT = (By.ID, "checkout")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_carga(self):
        self.wait.until(lambda driver: driver.current_url.endswith(self.URL_PATH))
        return self

    def esta_activa(self):
        return self.driver.current_url.endswith(self.URL_PATH)

    def obtener_productos(self):
        items = self.driver.find_elements(*self.ITEMS)
        return [
            {
                "nombre": item.find_element(
                    By.CLASS_NAME, "inventory_item_name"
                ).text,
                "precio": item.find_element(
                    By.CLASS_NAME, "inventory_item_price"
                ).text,
                "cantidad": item.find_element(
                    By.CLASS_NAME, "cart_quantity"
                ).text,
            }
            for item in items
        ]

    def esperar_productos(self):
        self.wait.until(EC.visibility_of_any_elements_located(self.ITEMS))
        return self.obtener_productos()

    def iniciar_checkout(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BOTON_CHECKOUT)
        ).click()
        return CheckoutInformationPage(self.driver).esperar_carga()
