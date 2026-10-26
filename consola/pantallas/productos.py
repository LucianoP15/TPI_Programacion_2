"""Integrante B - Epica 2: Gestion de productos."""

from consola.entrada import confirmar, pedir_decimal, pedir_entero, pedir_id, pedir_si_no, pedir_texto  # noqa: F401
from consola.estilos import (  # noqa: F401
    mensaje_aviso,
    mensaje_exito,
    mostrar_tabla_categorias,
    mostrar_tabla_productos,
    mostrar_titulo,
)
from entidades import Usuario
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-01 (admin): todos los no eliminados."""
    mostrar_titulo("🍔 Listado de productos")
    # TODO [B] listar_activos -> mostrar_tabla_productos / mensaje_aviso si no hay
    #          (opcional: filtrar por categoria con listar_por_categoria)
    raise NotImplementedError("HU-PROD-01 · Listar productos [B]")


def listar_disponibles(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-01 (cliente): solo disponibles y con stock > 0."""
    mostrar_titulo("🍔 Productos disponibles")
    # TODO [B] servicios.productos.listar_disponibles() -> mostrar_tabla_productos
    raise NotImplementedError("HU-PROD-01 · Listar productos disponibles [B]")


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-02."""
    mostrar_titulo("➕ Crear producto")
    # TODO [B]
    #  - nombre, descripcion, imagen (pedir_texto) / precio (pedir_decimal) / stock (pedir_entero)
    #  - disponible = pedir_si_no("¿Disponible?")
    #  - mostrar_tabla_categorias(...) y pedir_id de la categoria
    #  - servicios.productos.crear(...) y mensaje_exito con el id
    raise NotImplementedError("HU-PROD-02 · Crear producto [B]")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-03."""
    mostrar_titulo("✍️  Editar producto")
    # TODO [B] listar, pedir_id, todos los campos con opcional=True (Enter conserva)
    raise NotImplementedError("HU-PROD-03 · Editar producto [B]")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-04."""
    mostrar_titulo("❌ Eliminar producto")
    # TODO [B] listar, pedir_id, confirmar, servicios.productos.eliminar(id)
    raise NotImplementedError("HU-PROD-04 · Eliminar producto [B]")
