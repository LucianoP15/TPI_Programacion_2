from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from enums import Estado, FormaPago

if TYPE_CHECKING:
    from entidades.producto import Producto
    from entidades.usuario import Usuario


class Pedido(Base, Calculable):
    """N..1 con Usuario; composicion 1..N con DetallePedido."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        # TODO [B] HU-PED-02: validar usuario existente y no eliminado -> OperacionNoPermitidaError
        self.__usuario: Usuario = usuario
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0.0
        self.forma_pago = forma_pago
        self.__detalles: list[DetallePedido] = []

    # ---------------- properties ----------------
    @property
    def usuario(self) -> Usuario:
        return self.__usuario

    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado

    @estado.setter
    def estado(self, valor: Estado) -> None:
        # Las transiciones validas las controla PedidoServicio.cambiar_estado()
        self.__estado = valor

    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago

    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        self.__forma_pago = valor

    @property
    def total(self) -> float:
        return self.__total

    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        """Copia inmutable: la lista real no se modifica desde afuera."""
        return tuple(d for d in self.__detalles if not d.eliminado)

    # ---------------- metodos obligatorios (consigna) ----------------
    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        # TODO [B] HU-PED-02
        #  - producto no eliminado y disponible
        #  - cantidad > 0 y (cantidad total del producto en el pedido) <= producto.stock -> StockInsuficienteError
        #  - si ya hay un detalle de ese producto: sumar la cantidad al existente
        #  - si no: crear DetallePedido(cantidad, producto) y agregarlo a self.__detalles
        #  - NO descuenta stock (eso lo hace PedidoServicio cuando el pedido se confirma en la coleccion)
        raise NotImplementedError("Pedido.agregar_detalle")

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        # TODO [B] devolver el detalle activo de ese producto o None
        raise NotImplementedError("Pedido.buscar_detalle_por_producto")

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        # TODO [B] baja logica del detalle (detalle.eliminar()) y recalcular total
        raise NotImplementedError("Pedido.eliminar_detalle_por_producto")

    def calcular_total(self) -> None:
        # TODO [B] HU-PED-02: self.__total = suma de subtotales de los detalles activos
        raise NotImplementedError("Pedido.calcular_total")

    # ---------------- auxiliares ----------------
    def eliminar(self) -> None:
        """Baja logica del pedido y de sus detalles (composicion)."""
        super().eliminar()
        for detalle in self.__detalles:
            detalle.eliminar()

    def __str__(self) -> str:
        return (
            f"[{self.id}] {self.fecha:%d/%m/%Y} - {self.usuario.nombre_completo} - "
            f"{self.estado.value} - {self.forma_pago.value} - ${self.total:.2f}"
        )
