from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.checkout_complete_page import CheckoutCompletePage


class CheckoutOverviewPage:
    """Resumen de la compra previo a confirmarla."""

    URL_PATH = "/checkout-step-two.html"
    ITEMS = (By.CLASS_NAME, "cart_item")
    BOTON_FINALIZAR = (By.ID, "finish")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_carga(self):
        self.wait.until(lambda driver: driver.current_url.endswith(self.URL_PATH))
        self.wait.until(EC.element_to_be_clickable(self.BOTON_FINALIZAR))
        return self

    def obtener_nombres_productos(self):
        items = self.driver.find_elements(*self.ITEMS)
        return [
            item.find_element(By.CLASS_NAME, "inventory_item_name").text
            for item in items
        ]

    def finalizar_compra(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BOTON_FINALIZAR)
        ).click()
        return CheckoutCompletePage(self.driver).esperar_carga()
