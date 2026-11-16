from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base
from excepciones import DatoInvalidoError

if TYPE_CHECKING:
    from entidades.producto import Producto


class DetallePedido(Base):
    """
    Vive dentro de un Pedido (composicion): SOLO Pedido.agregar_detalle() crea instancias.
    El subtotal se calcula con el precio del producto al momento de crearlo.
    """

    def __init__(self, cantidad: int, producto: Producto) -> None:
        super().__init__()
        self.__producto: Producto = producto
        self.__precio_unitario: float = producto.precio
        self.cantidad = cantidad

    @property
    def producto(self) -> Producto:
        return self.__producto

    @property
    def precio_unitario(self) -> float:
        return self.__precio_unitario

    @property
    def cantidad(self) -> int:
        return self.__cantidad

    @cantidad.setter
    def cantidad(self, valor: int) -> None:
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise DatoInvalidoError("La cantidad debe ser un número entero")
        if valor <= 0:
            raise DatoInvalidoError("La cantidad debe ser mayor a 0")
        self.__cantidad = valor
        self.__subtotal = valor * self.__precio_unitario

    @property
    def subtotal(self) -> float:
        return self.__subtotal

    def __str__(self) -> str:
        return f"{self.producto.nombre} x{self.cantidad} = ${self.subtotal:.2f}"
