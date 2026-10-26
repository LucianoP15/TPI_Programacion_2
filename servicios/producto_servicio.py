from entidades import Producto
from servicios.categoria_servicio import CategoriaServicio
from servicios.servicio_base import ServicioBase


class ProductoServicio(ServicioBase[Producto]):
    """Integrante B."""

    nombre_entidad = "Producto"

    def __init__(self, categorias: CategoriaServicio) -> None:
        super().__init__()
        self._categorias: CategoriaServicio = categorias

    def listar_disponibles(self) -> list[Producto]:
        # TODO [B] HU-PROD-01: activos, disponible == True y stock > 0
        raise NotImplementedError("ProductoServicio.listar_disponibles")

    def listar_por_categoria(self, id_categoria: int) -> list[Producto]:
        # TODO [B] (opcional) HU-PROD-01: filtrar activos por categoria
        raise NotImplementedError("ProductoServicio.listar_por_categoria")

    def crear(
        self,
        nombre: str,
        precio: float,
        descripcion: str,
        stock: int,
        imagen: str,
        disponible: bool,
        id_categoria: int,
    ) -> Producto:
        # TODO [B] HU-PROD-02
        #  - categoria = self._categorias.buscar_por_id(id_categoria)
        #  - crear Producto (los setters validan), registrar y devolver
        raise NotImplementedError("ProductoServicio.crear")

    def editar(
        self,
        id_producto: int,
        nombre: str | None = None,
        precio: float | None = None,
        descripcion: str | None = None,
        stock: int | None = None,
        imagen: str | None = None,
        disponible: bool | None = None,
        id_categoria: int | None = None,
    ) -> Producto:
        # TODO [B] HU-PROD-03: None = conservar; mismas validaciones que al crear
        raise NotImplementedError("ProductoServicio.editar")

    def eliminar(self, id_producto: int) -> None:
        # TODO [B] HU-PROD-04: baja logica (producto.eliminar())
        raise NotImplementedError("ProductoServicio.eliminar")
