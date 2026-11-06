from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    """Acciones y elementos de la página de inicio de sesión de SauceDemo."""

    URL = "https://www.saucedemo.com/"
    CAMPO_USUARIO = (By.ID, "user-name")
    CAMPO_CONTRASENA = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def abrir(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.CAMPO_USUARIO))
        return self

    def iniciar_sesion(self, usuario, contrasena):
        campo_usuario = self.wait.until(
            EC.visibility_of_element_located(self.CAMPO_USUARIO)
        )
        campo_usuario.clear()
        campo_usuario.send_keys(usuario)

        campo_contrasena = self.driver.find_element(*self.CAMPO_CONTRASENA)
        campo_contrasena.clear()
        campo_contrasena.send_keys(contrasena)

        self.wait.until(EC.element_to_be_clickable(self.BOTON_LOGIN)).click()
        return self

    def obtener_mensaje_error(self):
        return self.wait.until(
            EC.visibility_of_element_located(self.MENSAJE_ERROR)
        ).text
