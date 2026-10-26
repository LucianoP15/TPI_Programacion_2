from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base
from enums import Rol

if TYPE_CHECKING:
    from entidades.pedido import Pedido


class Usuario(Base):
    """Asociacion 1..N con Pedido. La contrasenia nunca sale del objeto."""

    def __init__(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> None:
        super().__init__()
        self.nombre = nombre
        self.apellido = apellido
        self.mail = mail
        self.celular = celular
        self.contrasenia = contrasenia
        self.rol = rol
        self.__pedidos: list[Pedido] = []

    # ---------------- properties ----------------
    @property
    def nombre(self) -> str:
        return self.__nombre

    @nombre.setter
    def nombre(self, valor: str) -> None:
        # TODO [A] HU-USR-02: validar texto no vacio -> DatoInvalidoError
        self.__nombre = valor

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        # TODO [A] HU-USR-02: validar texto no vacio -> DatoInvalidoError
        self.__apellido = valor

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        # TODO [A] HU-USR-02: validar no vacio y formato basico ("@" y ".") -> DatoInvalidoError
        #          (la unicidad del mail se valida en UsuarioServicio, no aca)
        self.__mail = valor

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = valor

    # Sin property de lectura a proposito: solo setter.
    def _set_contrasenia(self, valor: str) -> None:
        # TODO [A] HU-USR-02: validar no vacia -> DatoInvalidoError
        self.__contrasenia = valor

    contrasenia = property(fset=_set_contrasenia)

    @property
    def rol(self) -> Rol:
        return self.__rol

    @rol.setter
    def rol(self, valor: Rol) -> None:
        self.__rol = valor

    @property
    def pedidos(self) -> tuple[Pedido, ...]:
        return tuple(self.__pedidos)

    @property
    def nombre_completo(self) -> str:
        return f"{self.nombre} {self.apellido}"

    # ---------------- auxiliares ----------------
    def verificar_contrasenia(self, contrasenia: str) -> bool:
        return self.__contrasenia == contrasenia

    def agregar_pedido(self, pedido: Pedido) -> None:
        if pedido not in self.__pedidos:
            self.__pedidos.append(pedido)

    def es_admin(self) -> bool:
        return self.rol == Rol.ADMIN

    def __str__(self) -> str:
        return f"[{self.id}] {self.nombre_completo} <{self.mail}> ({self.rol.value})"
