from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base

if TYPE_CHECKING:
    from entidades.categoria import Categoria


class Producto(Base):
    """N..1 con Categoria."""

    def __init__(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        categoria: Categoria,
    ) -> None:
        super().__init__()
        self.__categoria: Categoria | None = None
        self.nombre = nombre
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible = disponible
        self.categoria = categoria

    # ---------------- properties ----------------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # TODO [B] HU-PROD-02: validar texto no vacio -> DatoInvalidoError
        self.__nombre = valor

    @property
    def precio(self) -> float:
        return self.__precio

    @precio.setter
    def precio(self, valor: float) -> None:
        # TODO [B] HU-PROD-02: validar precio >= 0 -> PrecioInvalidoError
        self.__precio = valor

    @property
    def descripcion(self) -> str:
        return self.__descripcion

    @descripcion.setter
    def descripcion(self, valor: str) -> None:
        self.__descripcion = valor

    @property
    def stock(self) -> int:
        return self.__stock

    @stock.setter
    def stock(self, valor: int) -> None:
        # TODO [B] HU-PROD-02: validar stock >= 0 -> DatoInvalidoError
        self.__stock = valor

    @property
    def imagen(self) -> str:
        return self.__imagen

    @imagen.setter
    def imagen(self, valor: str) -> None:
        self.__imagen = valor

    @property
    def disponible(self) -> bool:
        return self.__disponible

    @disponible.setter
    def disponible(self, valor: bool) -> None:
        self.__disponible = valor

    @property
    def categoria(self) -> Categoria:
        return self.__categoria  # type: ignore[return-value]

    @categoria.setter
    def categoria(self, valor: Categoria) -> None:
        # TODO [B] HU-PROD-02: validar categoria no eliminada -> OperacionNoPermitidaError
        # Mantiene sincronizada la agregacion en ambos sentidos (auxiliar, ya resuelto)
        if self.__categoria is not None:
            self.__categoria.quitar_producto(self)
        self.__categoria = valor
        valor.agregar_producto(self)

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre} - ${self.precio:.2f} (stock: {self.stock}) - {self.categoria.nombre}"
