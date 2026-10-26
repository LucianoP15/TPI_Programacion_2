from dataclasses import dataclass

from servicios.categoria_servicio import CategoriaServicio
from servicios.producto_servicio import ProductoServicio
from servicios.usuario_servicio import UsuarioServicio
from servicios.pedido_servicio import PedidoServicio


@dataclass
class Servicios:
    """Agrupa los servicios para pasarlos juntos a los menus (sin variables globales)."""

    categorias: CategoriaServicio
    productos: ProductoServicio
    usuarios: UsuarioServicio
    pedidos: PedidoServicio


def crear_servicios() -> Servicios:
    categorias = CategoriaServicio()
    productos = ProductoServicio(categorias)
    usuarios = UsuarioServicio()
    pedidos = PedidoServicio(usuarios, productos)
    return Servicios(categorias, productos, usuarios, pedidos)


__all__ = [
    "Servicios",
    "crear_servicios",
    "CategoriaServicio",
    "ProductoServicio",
    "UsuarioServicio",
    "PedidoServicio",
]
