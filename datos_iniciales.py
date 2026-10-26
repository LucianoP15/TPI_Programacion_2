"""
Carga el administrador inicial y datos de ejemplo (auxiliar).
Usa registrar() directamente para no depender de los crear() que todavia estan vacios.
Cuando esten implementados, pueden cambiarse por servicios.X.crear(...).
"""

from entidades import Categoria, Producto, Usuario
from enums import Rol
from servicios import Servicios


def cargar_datos_iniciales(servicios: Servicios) -> None:
    # ---------- usuarios ----------
    servicios.usuarios.registrar(
        Usuario("Ana", "Pérez", "admin@foodstore.com", "2614000000", "admin123", Rol.ADMIN)
    )
    servicios.usuarios.registrar(
        Usuario("Juan", "Gómez", "juan@foodstore.com", "2615111111", "cliente123", Rol.USUARIO)
    )

    # ---------- categorias ----------
    pizzas = servicios.categorias.registrar(Categoria("Pizzas", "Pizzas a la piedra"))
    hamburguesas = servicios.categorias.registrar(Categoria("Hamburguesas", "Con papas incluidas"))
    bebidas = servicios.categorias.registrar(Categoria("Bebidas", "Gaseosas, aguas y cervezas"))

    # ---------- productos ----------
    productos: list[Producto] = [
        Producto("Muzzarella", 9500.0, "Salsa, muzza y aceitunas", 20, "muzza.png", True, pizzas),
        Producto("Napolitana", 11000.0, "Muzza, tomate y ajo", 15, "napo.png", True, pizzas),
        Producto("Clasica", 8500.0, "Carne, queso, lechuga y tomate", 25, "clasica.png", True, hamburguesas),
        Producto("Doble bacon", 12500.0, "Doble carne, cheddar y bacon", 2, "bacon.png", True, hamburguesas),
        Producto("Coca-Cola 1.5L", 3500.0, "Botella 1.5 litros", 40, "coca.png", True, bebidas),
        Producto("Agua 500ml", 1500.0, "Sin gas", 0, "agua.png", True, bebidas),
    ]
    for producto in productos:
        servicios.productos.registrar(producto)
