import pytest

from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.data_loader import cargar_json


DATOS_USUARIOS = cargar_json("usuarios.json")
USUARIO_VALIDO = DATOS_USUARIOS["usuario_valido"]
CASOS_LOGIN_INVALIDOS = DATOS_USUARIOS["casos_login_invalidos"]
DATOS_CHECKOUT = DATOS_USUARIOS["datos_checkout"]


def iniciar_sesion_estandar(navegador):
    LoginPage(navegador).abrir().iniciar_sesion(
        USUARIO_VALIDO["usuario"], USUARIO_VALIDO["contrasena"]
    )
    return InventoryPage(navegador).esperar_carga()


def test_login_exitoso(navegador):
    LoginPage(navegador).abrir().iniciar_sesion(
        USUARIO_VALIDO["usuario"], USUARIO_VALIDO["contrasena"]
    )
    pagina_inventario = InventoryPage(navegador)
    pagina_inventario.esperar_carga()
    assert pagina_inventario.esta_activa(), (
        "El login no redirigió a la página de inventario"
    )

    titulo = pagina_inventario.obtener_titulo()
    assert titulo == "Products", (
        f"Se esperaba 'Products', pero apareció '{titulo}'"
    )

    marca = pagina_inventario.obtener_marca()
    assert marca == "Swag Labs", (
        f"Se esperaba 'Swag Labs', pero apareció '{marca}'"
    )


@pytest.mark.parametrize(
    "caso",
    CASOS_LOGIN_INVALIDOS,
    ids=[caso["id"] for caso in CASOS_LOGIN_INVALIDOS],
)
def test_login_rechaza_credenciales_invalidas(navegador, caso):
    pagina_login = LoginPage(navegador).abrir().iniciar_sesion(
        caso["usuario"], caso["contrasena"]
    )

    assert pagina_login.obtener_mensaje_error() == caso["mensaje_esperado"]


def test_catalogo_productos(navegador):
    pagina_inventario = iniciar_sesion_estandar(navegador)

    # Verificar el título visible de la página de inventario.
    titulo = pagina_inventario.obtener_titulo()
    assert titulo == "Products", (
        f"Se esperaba 'Products', pero apareció '{titulo}'"
    )

    cantidad_productos = pagina_inventario.contar_productos()

    assert cantidad_productos > 0, "No hay productos visibles en el catálogo"

    datos_producto = pagina_inventario.obtener_datos_primer_producto()
    assert datos_producto["nombre"], "El producto no tiene nombre"
    assert datos_producto["precio"], "El producto no tiene precio"
    assert pagina_inventario.menu_esta_visible(), (
        "El botón del menú no está visible"
    )
    assert pagina_inventario.filtro_esta_visible(), (
        "El filtro no está visible"
    )
    assert pagina_inventario.enlace_carrito_esta_visible(), (
        "El enlace al carrito no está visible"
    )


def test_agregar_producto_al_carrito(navegador):
    pagina_inventario = iniciar_sesion_estandar(navegador)
    contador_inicial = pagina_inventario.obtener_cantidad_en_carrito()

    assert contador_inicial == 0, (
        "El carrito debe estar vacío al comenzar el test"
    )

    # Agregar un producto y conservar sus datos para compararlos en el carrito.
    datos_producto = pagina_inventario.agregar_primer_producto_al_carrito()
    contador_esperado = contador_inicial + 1
    contador_actual = pagina_inventario.obtener_cantidad_en_carrito()

    assert contador_actual == contador_esperado, (
        "El contador del carrito no aumentó correctamente"
    )

    pagina_carrito = pagina_inventario.abrir_carrito()
    assert pagina_carrito.esta_activa(), (
        "No se abrió la página del carrito"
    )

    productos_carrito = pagina_carrito.esperar_productos()
    assert len(productos_carrito) == 1, (
        f"Se esperaba un producto, pero hay {len(productos_carrito)}"
    )
    producto_carrito = productos_carrito[0]

    assert producto_carrito["nombre"] == datos_producto["nombre"], (
        "El producto del carrito no coincide con el agregado"
    )
    assert producto_carrito["precio"] == datos_producto["precio"], (
        "El precio del carrito no coincide con el del catálogo"
    )
    assert producto_carrito["cantidad"] == "1", (
        "La cantidad del producto debe ser uno"
    )

    print(
        f"\nProducto verificado en carrito: {producto_carrito['nombre']}"
        f" | Precio: {producto_carrito['precio']}"
        f" | Cantidad: {producto_carrito['cantidad']}"
    )


def test_compra_completa_checkout(navegador):
    pagina_inventario = iniciar_sesion_estandar(navegador)
    datos_producto = pagina_inventario.agregar_primer_producto_al_carrito()
    pagina_carrito = pagina_inventario.abrir_carrito()

    productos_carrito = pagina_carrito.esperar_productos()
    assert len(productos_carrito) == 1, (
        f"Se esperaba un producto antes del checkout, pero hay "
        f"{len(productos_carrito)}"
    )

    pagina_datos = pagina_carrito.iniciar_checkout()
    pagina_resumen = (
        pagina_datos
        .completar_datos(
            DATOS_CHECKOUT["nombre"],
            DATOS_CHECKOUT["apellido"],
            DATOS_CHECKOUT["codigo_postal"],
        )
        .continuar()
    )

    nombres_resumen = pagina_resumen.obtener_nombres_productos()
    assert datos_producto["nombre"] in nombres_resumen, (
        "El producto del catálogo no aparece en el resumen del checkout"
    )

    pagina_confirmacion = pagina_resumen.finalizar_compra()
    assert pagina_confirmacion.obtener_titulo_confirmacion() == (
        "Thank you for your order!"
    )

