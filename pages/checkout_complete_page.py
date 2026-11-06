from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutCompletePage:
    """Confirmación que aparece al completar una compra."""

    URL_PATH = "/checkout-complete.html"
    TITULO_CONFIRMACION = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_carga(self):
        self.wait.until(lambda driver: driver.current_url.endswith(self.URL_PATH))
        self.wait.until(
            EC.visibility_of_element_located(self.TITULO_CONFIRMACION)
        )
        return self

    def obtener_titulo_confirmacion(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.TITULO_CONFIRMACION)
        ).text
