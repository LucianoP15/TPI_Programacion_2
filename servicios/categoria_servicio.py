from entidades import Categoria
from servicios.servicio_base import ServicioBase


class CategoriaServicio(ServicioBase[Categoria]):
    """Integrante A."""

    nombre_entidad = "Categoria"

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        # TODO [A] HU-CAT-02
        #  - validar nombre unico sin distinguir mayusculas (_validar_nombre_unico)
        #  - crear Categoria, registrarla con self.registrar(...) y devolverla
        raise NotImplementedError("CategoriaServicio.crear")

    def editar(self, id_categoria: int, nombre: str | None, descripcion: str | None) -> Categoria:
        # TODO [A] HU-CAT-03
        #  - buscar_por_id (lanza EntidadNoEncontradaError)
        #  - None = conservar valor. Si cambia el nombre, validar unicidad excluyendo a si misma
        raise NotImplementedError("CategoriaServicio.editar")

    def eliminar(self, id_categoria: int) -> None:
        # TODO [A] HU-CAT-04
        #  - si categoria.cantidad_productos_activos() > 0 -> OperacionNoPermitidaError (informar cuantos)
        #  - si no: categoria.eliminar()
        raise NotImplementedError("CategoriaServicio.eliminar")

    def _validar_nombre_unico(self, nombre: str, excluir_id: int | None = None) -> None:
        # TODO [A] recorrer listar_activos(); si coincide (lower/strip) -> DuplicadoError
        raise NotImplementedError("CategoriaServicio._validar_nombre_unico")
