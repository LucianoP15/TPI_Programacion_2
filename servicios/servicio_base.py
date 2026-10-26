from typing import Generic, TypeVar

from entidades import Base
from excepciones import EntidadNoEncontradaError

T = TypeVar("T", bound=Base)


class ServicioBase(Generic[T]):
    """
    Auxiliar comun a todos los servicios: guarda la coleccion y resuelve
    las operaciones repetidas (registrar, listar activos, buscar por id).
    Cada servicio concreto agrega SUS reglas de negocio.
    """

    nombre_entidad: str = "Entidad"

    def __init__(self) -> None:
        self._items: list[T] = []

    def registrar(self, item: T) -> T:
        """Agrega a la coleccion sin validar reglas de negocio (las valida quien llama)."""
        self._items.append(item)
        return item

    def listar_activos(self) -> list[T]:
        return [item for item in self._items if not item.eliminado]

    def listar_todos(self) -> tuple[T, ...]:
        return tuple(self._items)

    def buscar_por_id(self, id_buscado: int) -> T:
        for item in self._items:
            if item.id == id_buscado and not item.eliminado:
                return item
        raise EntidadNoEncontradaError(f"{self.nombre_entidad} con id {id_buscado} no encontrado/a")
