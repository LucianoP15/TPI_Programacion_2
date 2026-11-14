from entidades import Categoria
from excepciones import DuplicadoError, OperacionNoPermitidaError
from servicios.servicio_base import ServicioBase


class CategoriaServicio(ServicioBase[Categoria]):
    """Integrante A."""

    nombre_entidad = "Categoria"

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        self.validar_nombre_unico(nombre)
        return self.registrar(Categoria(nombre, descripcion))

    def editar(self, id_categoria: int, nombre: str | None, descripcion: str | None) -> Categoria:
        """None = conservar el valor actual."""
        categoria = self.buscar_por_id(id_categoria)
        if nombre is not None:
            self.validar_nombre_unico(nombre, excluir_id=categoria.id)
            categoria.nombre = nombre
        if descripcion is not None:
            categoria.descripcion = descripcion
        return categoria

    def eliminar(self, id_categoria: int) -> None:
        categoria = self.buscar_por_id(id_categoria)
        activos = [producto.nombre for producto in categoria.productos if not producto.eliminado]
        if activos:
            raise OperacionNoPermitidaError(
                f"La categoria '{categoria.nombre}' tiene {len(activos)} producto/s activo/s "
                f"({', '.join(activos)}). Elimine o reasigne esos productos primero"
            )
        categoria.eliminar()

    def validar_nombre_unico(self, nombre: str, excluir_id: int | None = None) -> None:
        buscado = nombre.strip().lower()
        for categoria in self.listar_activos():
            if categoria.nombre.lower() == buscado and categoria.id != excluir_id:
                raise DuplicadoError(f"Ya existe una categoria con el nombre '{categoria.nombre}'")
