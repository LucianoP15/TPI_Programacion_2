from __future__ import annotations

from datetime import date
from typing import TYPE_CHECKING

from entidades.base import Base
from entidades.calculable import Calculable
from entidades.detalle_pedido import DetallePedido
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, OperacionNoPermitidaError, StockInsuficienteError

if TYPE_CHECKING:
    from entidades.producto import Producto
    from entidades.usuario import Usuario


class Pedido(Base, Calculable):
    """N..1 con Usuario; composicion 1..N con DetallePedido."""

    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        if usuario is None:
            raise OperacionNoPermitidaError("El pedido debe tener un usuario")
        if usuario.eliminado:
            raise OperacionNoPermitidaError("No se puede crear un pedido para un usuario eliminado")
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
        if producto is None or producto.eliminado:
            raise OperacionNoPermitidaError("El producto no existe o fue eliminado")
        if not producto.disponible:
            raise OperacionNoPermitidaError(f"El producto '{producto.nombre}' no está disponible")
        if isinstance(cantidad, bool) or not isinstance(cantidad, int) or cantidad <= 0:
            raise DatoInvalidoError("La cantidad debe ser un número entero mayor a 0")
        existente = self.buscar_detalle_por_producto(producto)
        cantidad_total = cantidad + (existente.cantidad if existente else 0)
        if cantidad_total > producto.stock:
            raise StockInsuficienteError(
                f"Stock insuficiente para '{producto.nombre}': "
                f"pedido {cantidad_total}, disponible {producto.stock}"
            )
        if existente:
            existente.cantidad = cantidad_total
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()

    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for detalle in self.__detalles:
            if not detalle.eliminado and detalle.producto == producto:
                return detalle
        return None

    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        detalle = self.buscar_detalle_por_producto(producto)
        if detalle is None:
            raise OperacionNoPermitidaError("El pedido no tiene un detalle de ese producto")
        detalle.eliminar()
        self.calcular_total()

    def calcular_total(self) -> None:
        self.__total = sum(d.subtotal for d in self.__detalles if not d.eliminado)

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
