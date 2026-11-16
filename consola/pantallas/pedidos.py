"""Integrante B - Epica 4: Gestion de pedidos y detalles."""

from consola.entrada import confirmar, elegir_enum, pedir_entero, pedir_id
from consola.estilos import (
    formatear_precio,
    mensaje_aviso,
    mensaje_exito,
    mostrar_tabla_detalles,
    mostrar_tabla_pedidos,
    mostrar_tabla_productos,
    mostrar_tabla_usuarios,
    mostrar_titulo,
)
from entidades import Usuario
from enums import Estado, FormaPago
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-01."""
    mostrar_titulo("🧾 Listado de pedidos")
    pedidos = servicios.pedidos.listar_activos()
    if not pedidos:
        mensaje_aviso("No hay pedidos cargados")
        return
    mostrar_tabla_pedidos(pedidos)


def ver_detalle(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-01 (opcional): detalle de un pedido."""
    mostrar_titulo("🔍 Detalle de pedido")
    pedidos = servicios.pedidos.listar_activos()
    if not pedidos:
        mensaje_aviso("No hay pedidos cargados")
        return
    mostrar_tabla_pedidos(pedidos)
    pedido = servicios.pedidos.buscar_por_id(pedir_id("Id del pedido: "))
    mostrar_tabla_detalles(pedido)


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-02."""
    mostrar_titulo("➕ Crear pedido")
    disponibles = servicios.productos.listar_disponibles()
    if not disponibles:
        mensaje_aviso("No hay productos disponibles para pedir")
        return
    mostrar_tabla_usuarios(servicios.usuarios.listar_activos())
    usuario = servicios.usuarios.buscar_por_id(pedir_id("Id del usuario: "))
    forma_pago = elegir_enum("Forma de pago:", FormaPago)

    items: list[tuple[int, int]] = []
    while True:
        mostrar_tabla_productos(disponibles)
        producto = servicios.productos.buscar_por_id(pedir_id("Id del producto: "))
        cantidad = pedir_entero(f"Cantidad de '{producto.nombre}': ", minimo=1)
        items.append((producto.id, cantidad))
        if not confirmar("¿Agregar otro producto?"):
            break

    pedido = servicios.pedidos.crear(usuario.id, forma_pago, items)
    mostrar_tabla_detalles(pedido)
    mensaje_exito(f"Pedido #{pedido.id} creado. Total: {formatear_precio(pedido.total)}")


def actualizar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-03."""
    mostrar_titulo("🚦 Cambiar estado / forma de pago")
    pedidos = servicios.pedidos.listar_activos()
    if not pedidos:
        mensaje_aviso("No hay pedidos cargados")
        return
    mostrar_tabla_pedidos(pedidos)
    pedido = servicios.pedidos.buscar_por_id(pedir_id("Id del pedido: "))

    estado = elegir_enum(f"Nuevo estado [{pedido.estado.value}]:", Estado, opcional=True)
    if estado is not None:
        servicios.pedidos.cambiar_estado(pedido.id, estado)
        mensaje_exito(f"Estado actualizado a {estado.value}.")

    forma_pago = elegir_enum(f"Nueva forma de pago [{pedido.forma_pago.value}]:", FormaPago, opcional=True)
    if forma_pago is not None:
        servicios.pedidos.cambiar_forma_pago(pedido.id, forma_pago)
        mensaje_exito(f"Forma de pago actualizada a {forma_pago.value}.")

    if estado is None and forma_pago is None:
        mensaje_aviso("No se modificó nada.")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-04."""
    mostrar_titulo("❌ Eliminar pedido")
    pedidos = servicios.pedidos.listar_activos()
    if not pedidos:
        mensaje_aviso("No hay pedidos cargados")
        return
    mostrar_tabla_pedidos(pedidos)
    pedido = servicios.pedidos.buscar_por_id(pedir_id("Id del pedido: "))
    if not confirmar(f"¿Seguro que querés eliminar el pedido #{pedido.id}?"):
        mensaje_aviso("No se eliminó el pedido.")
        return
    servicios.pedidos.eliminar(pedido.id)
    mensaje_exito("Pedido eliminado.")


def mis_pedidos(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PED-05 (cliente)."""
    mostrar_titulo("🧾 Mis pedidos")
    pedidos = servicios.pedidos.listar_por_usuario(sesion)
    if not pedidos:
        mensaje_aviso("Todavía no tenés pedidos")
        return
    mostrar_tabla_pedidos(pedidos)
    if confirmar("¿Ver el detalle de alguno?"):
        pedido = servicios.pedidos.buscar_de_usuario(pedir_id("Id del pedido: "), sesion)
        mostrar_tabla_detalles(pedido)
