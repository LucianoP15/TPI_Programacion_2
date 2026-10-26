from abc import ABC
from datetime import datetime


class Base(ABC):
    """
    Superclase abstracta de todas las entidades.
    El id se asigna con un contador de clase COMPARTIDO por todas las entidades
    (decision a justificar en el informe: ids unicos en todo el sistema).
    """

    __contador_id: int = 0

    def __init__(self) -> None:
        if type(self) is Base:
            raise TypeError("Base es abstracta y no se puede instanciar")
        Base.__contador_id += 1
        self.__id: int = Base.__contador_id
        self.__eliminado: bool = False
        self.__creado_en: datetime = datetime.now()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def eliminado(self) -> bool:
        return self.__eliminado

    @property
    def creado_en(self) -> datetime:
        return self.__creado_en

    def eliminar(self) -> None:
        """Baja logica: el objeto sigue en la coleccion."""
        self.__eliminado = True

    def __eq__(self, otro: object) -> bool:
        if not isinstance(otro, Base):
            return NotImplemented
        return type(self) is type(otro) and self.id == otro.id

    def __hash__(self) -> int:
        return hash((type(self).__name__, self.id))
