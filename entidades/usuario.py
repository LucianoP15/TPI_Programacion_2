from __future__ import annotations

from typing import TYPE_CHECKING

from entidades.base import Base
from enums import Rol
from excepciones import DatoInvalidoError

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
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El nombre no puede estar vacío")
        if any(c.isdigit() for c in valor):
            raise DatoInvalidoError("El nombre no puede contener números")
        self.__nombre = valor.strip()

    @property
    def apellido(self) -> str:
        return self.__apellido

    @apellido.setter
    def apellido(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El apellido no puede estar vacío")
        if any(c.isdigit() for c in valor):
            raise DatoInvalidoError("El apellido no puede contener números")
        self.__apellido = valor.strip()

    @property
    def mail(self) -> str:
        return self.__mail

    @mail.setter
    def mail(self, valor: str) -> None:
        """La unicidad la valida UsuarioServicio."""
        self.__mail = Usuario.validar_formato_mail(valor)

    @staticmethod
    def validar_formato_mail(valor: str) -> str:
        """Formato nombre@dominio.ext; devuelve el mail en minusculas."""
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("El mail no puede estar vacío")
        mail = valor.strip().lower()
        local, arroba, dominio = mail.partition("@")
        nombre_dominio, punto, extension = dominio.rpartition(".")
        if not (local and arroba and nombre_dominio and punto and extension) or "@" in dominio or " " in mail:
            raise DatoInvalidoError(f"El mail '{valor.strip()}' no es válido (ejemplo: nombre@dominio.com)")
        return mail

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, valor: str) -> None:
        self.__celular = valor

    # Sin property de lectura a proposito: solo setter.
    def _set_contrasenia(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise DatoInvalidoError("La contraseña no puede estar vacía")
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
