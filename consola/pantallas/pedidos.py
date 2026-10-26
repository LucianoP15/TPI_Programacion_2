"""Integrante B - Epica 4: Gestion de pedidos y detalles."""

from consola.entrada import confirmar, elegir_enum, pedir_entero, pedir_id  # noqa: F401
from consola.estilos import (  # noqa: F401
    mensaje_aviso,
    mensaje_exito,
    mostrar_tabla_detalles,
    mostrar_tabla_pedidos,
    mostrar_tabla_productos,
    mostrar_tabla_usuarios,
    mostrar_titulo,
)
from entidades import Usuario
from enums import Estado, FormaPago  # noqa: F401
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-01."""
    mostrar_titulo("🧾 Listado de pedidos")
    # TODO [B] listar_activos -> mostrar_tabla_pedidos / mensaje_aviso si no hay
    raise NotImplementedError("HU-PED-01 · Listar pedidos [B]")


def ver_detalle(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-01 (opcional): detalle de un pedido."""
    mostrar_titulo("🔍 Detalle de pedido")
    # TODO [B] pedir_id -> buscar_por_id -> mostrar_tabla_detalles(pedido)
    raise NotImplementedError("HU-PED-01 · Ver detalle de pedido [B]")


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-02."""
    mostrar_titulo("➕ Crear pedido")
    # TODO [B]
    #  - mostrar_tabla_usuarios + pedir_id del usuario
    #  - forma_pago = elegir_enum("Forma de pago:", FormaPago)
    #  - bucle: mostrar_tabla_productos, pedir_id producto, pedir_entero cantidad (minimo=1),
    #           acumular (id_producto, cantidad) en una lista; confirmar("¿Agregar otro producto?")
    #  - pedido = servicios.pedidos.crear(id_usuario, forma_pago, items)
    #  - mostrar_tabla_detalles(pedido) y mensaje_exito con id y total
    raise NotImplementedError("HU-PED-02 · Crear pedido [B]")


def actualizar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-03."""
    mostrar_titulo("🚦 Cambiar estado / forma de pago")
    # TODO [B]
    #  - listar, pedir_id
    #  - elegir_enum("Nuevo estado:", Estado, opcional=True) -> si no es None: cambiar_estado
    #  - elegir_enum("Nueva forma de pago:", FormaPago, opcional=True) -> si no es None: cambiar_forma_pago
    raise NotImplementedError("HU-PED-03 · Cambiar estado / forma de pago [B]")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-04."""
    mostrar_titulo("❌ Eliminar pedido")
    # TODO [B] listar, pedir_id, confirmar, servicios.pedidos.eliminar(id)
    raise NotImplementedError("HU-PED-04 · Eliminar pedido [B]")


def mis_pedidos(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-05 (cliente)."""
    mostrar_titulo("🧾 Mis pedidos")
    # TODO [B]
    #  - servicios.pedidos.listar_por_usuario(sesion) -> mostrar_tabla_pedidos
    #  - si confirmar("¿Ver el detalle de alguno?"): pedir_id -> buscar_de_usuario(id, sesion)
    #    -> mostrar_tabla_detalles
    raise NotImplementedError("HU-PED-05 · Mis pedidos [B]")
