"""Integrante A - Epica 1: Gestion de categorias."""

from consola.entrada import confirmar, pedir_id, pedir_texto  # noqa: F401
from consola.estilos import mensaje_aviso, mensaje_exito, mostrar_tabla_categorias, mostrar_titulo  # noqa: F401
from entidades import Usuario
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-01 (admin y cliente)."""
    mostrar_titulo("📂 Listado de categorias")
    # TODO [A]
    #  - servicios.categorias.listar_activos()
    #  - si esta vacia: mensaje_aviso("No hay categorias cargadas") y return
    #  - mostrar_tabla_categorias(...)
    raise NotImplementedError("HU-CAT-01 · Listar categorias [A]")


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-02."""
    mostrar_titulo("➕ Crear categoria")
    # TODO [A]
    #  - pedir_texto nombre y descripcion
    #  - servicios.categorias.crear(...)
    #  - mensaje_exito con el id generado
    raise NotImplementedError("HU-CAT-02 · Crear categoria [A]")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-03."""
    mostrar_titulo("✍️  Editar categoria")
    # TODO [A]
    #  - listar antes de pedir el id
    #  - pedir_id; mostrar la categoria actual
    #  - pedir_texto(..., opcional=True) -> None conserva el valor (Enter)
    #  - servicios.categorias.editar(...) y mensaje_exito
    raise NotImplementedError("HU-CAT-03 · Editar categoria [A]")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-04."""
    mostrar_titulo("❌ Eliminar categoria")
    # TODO [A]
    #  - listar, pedir_id, confirmar("¿Seguro?")
    #  - servicios.categorias.eliminar(id) y mensaje_exito
    raise NotImplementedError("HU-CAT-04 · Eliminar categoria [A]")
