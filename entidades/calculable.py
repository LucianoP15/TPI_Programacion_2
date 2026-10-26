from abc import ABC, abstractmethod


class Calculable(ABC):
    """Interfaz: quien la implementa sabe recalcular su propio total."""

    @abstractmethod
    def calcular_total(self) -> None:
        ...
