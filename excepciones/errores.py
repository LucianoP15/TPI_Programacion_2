class FoodStoreError(Exception):
    """Excepcion base del sistema. La consola captura esta clase para mostrar errores de negocio."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
        self.mensaje: str = mensaje


class EntidadNoEncontradaError(FoodStoreError):
    """Id inexistente o entidad eliminada."""


class DatoInvalidoError(FoodStoreError):
    """Texto vacio, formato incorrecto, numero fuera de rango."""


class PrecioInvalidoError(DatoInvalidoError):
    """Precio negativo."""


class StockInsuficienteError(FoodStoreError):
    """Cantidad pedida mayor al stock disponible."""


class DuplicadoError(FoodStoreError):
    """Mail o nombre de categoria repetido."""


class OperacionNoPermitidaError(FoodStoreError):
    """Transicion de estado invalida, categoria con productos activos, admin que se elimina a si mismo."""


class CredencialesInvalidasError(FoodStoreError):
    """Mail o contrasenia incorrectos, o usuario eliminado. Siempre con el mismo mensaje."""

    def __init__(self, mensaje: str = "Mail o contraseña incorrectos") -> None:
        super().__init__(mensaje)
