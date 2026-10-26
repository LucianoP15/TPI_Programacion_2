"""Integrante A - Epica 3: Gestion de usuarios."""

from consola.entrada import confirmar, elegir_enum, pedir_contrasenia, pedir_id, pedir_texto  # noqa: F401
from consola.estilos import (  # noqa: F401
    mensaje_aviso,
    mensaje_exito,
    mostrar_ficha_usuario,
    mostrar_tabla_usuarios,
    mostrar_titulo,
)
from entidades import Usuario
from enums import Rol  # noqa: F401
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-01 (nunca mostrar la contrasenia)."""
    mostrar_titulo("👥 Listado de usuarios")
    # TODO [A] listar_activos -> mostrar_tabla_usuarios / mensaje_aviso si no hay
    raise NotImplementedError("HU-USR-01 · Listar usuarios [A]")


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-02."""
    mostrar_titulo("➕ Crear usuario")
    # TODO [A]
    #  - nombre, apellido, mail, celular (pedir_texto), contrasenia (pedir_contrasenia)
    #  - rol = elegir_enum("Rol:", Rol)
    #  - servicios.usuarios.crear(...) y mensaje_exito con el id
    #  - si el mail ya existe (DuplicadoError) -> volver a pedir el mail (criterio de aceptacion)
    raise NotImplementedError("HU-USR-02 · Crear usuario [A]")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-03."""
    mostrar_titulo("✍️  Editar usuario")
    # TODO [A] listar, pedir_id, campos opcionales (Enter conserva), elegir_enum(..., opcional=True)
    raise NotImplementedError("HU-USR-03 · Editar usuario [A]")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-04 (un admin no puede eliminarse a si mismo: pasar `sesion` al servicio)."""
    mostrar_titulo("❌ Eliminar usuario")
    # TODO [A] listar, pedir_id, confirmar, servicios.usuarios.eliminar(id, sesion)
    raise NotImplementedError("HU-USR-04 · Eliminar usuario [A]")


def mis_datos(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-05 (cliente)."""
    mostrar_titulo("👤 Mis datos")
    # TODO [A] mostrar_ficha_usuario(sesion)
    raise NotImplementedError("HU-USR-05 · Ver mis datos [A]")
