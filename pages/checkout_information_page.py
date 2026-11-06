from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.checkout_overview_page import CheckoutOverviewPage


class CheckoutInformationPage:
    """Formulario con los datos del comprador durante el checkout."""

    URL_PATH = "/checkout-step-one.html"
    CAMPO_NOMBRE = (By.ID, "first-name")
    CAMPO_APELLIDO = (By.ID, "last-name")
    CAMPO_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def esperar_carga(self):
        self.wait.until(lambda driver: driver.current_url.endswith(self.URL_PATH))
        self.wait.until(EC.visibility_of_element_located(self.CAMPO_NOMBRE))
        return self

    def completar_datos(self, nombre, apellido, codigo_postal):
        valores = (
            (self.CAMPO_NOMBRE, nombre),
            (self.CAMPO_APELLIDO, apellido),
            (self.CAMPO_CODIGO_POSTAL, codigo_postal),
        )
        for localizador, valor in valores:
            campo = self.wait.until(
                EC.visibility_of_element_located(localizador)
            )
            campo.clear()
            campo.send_keys(valor)
        return self

    def continuar(self):
        self.wait.until(
            EC.element_to_be_clickable(self.BOTON_CONTINUAR)
        ).click()
        return CheckoutOverviewPage(self.driver).esperar_carga()
