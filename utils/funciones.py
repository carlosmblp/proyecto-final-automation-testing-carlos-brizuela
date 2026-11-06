def iniciar_sesion(navegador, usuario, contrasena):
    """Compatibilidad para código antiguo; la interacción vive en LoginPage."""
    from pages.login_page import LoginPage

    LoginPage(navegador).abrir().iniciar_sesion(usuario, contrasena)
