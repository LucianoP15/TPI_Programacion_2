from entidades import Producto
from excepciones import FoodStoreError
from servicios.categoria_servicio import CategoriaServicio
from servicios.servicio_base import ServicioBase


class ProductoServicio(ServicioBase[Producto]):
    """Integrante B."""

    nombre_entidad = "Producto"

    def __init__(self, categorias: CategoriaServicio) -> None:
        super().__init__()
        self._categorias: CategoriaServicio = categorias

    def listar_disponibles(self) -> list[Producto]:
        return [p for p in self.listar_activos() if p.disponible and p.stock > 0]

    def listar_por_categoria(self, id_categoria: int) -> list[Producto]:
        categoria = self._categorias.buscar_por_id(id_categoria)
        return [p for p in self.listar_activos() if p.categoria == categoria]

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
        categoria = self._categorias.buscar_por_id(id_categoria)
        producto = Producto(nombre, precio, descripcion, stock, imagen, disponible, categoria)
        return self.registrar(producto)

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
        producto = self.buscar_por_id(id_producto)
        categoria = self._categorias.buscar_por_id(id_categoria) if id_categoria is not None else None

        # Si un dato falla, se restauran los anteriores: la edicion es todo o nada
        anterior = (
            producto.nombre, producto.precio, producto.descripcion, producto.stock,
            producto.imagen, producto.disponible, producto.categoria,
        )
        try:
            if nombre is not None:
                producto.nombre = nombre
            if precio is not None:
                producto.precio = precio
            if descripcion is not None:
                producto.descripcion = descripcion
            if stock is not None:
                producto.stock = stock
            if imagen is not None:
                producto.imagen = imagen
            if disponible is not None:
                producto.disponible = disponible
            if categoria is not None:
                producto.categoria = categoria
        except FoodStoreError:
            (
                producto.nombre, producto.precio, producto.descripcion, producto.stock,
                producto.imagen, producto.disponible, producto.categoria,
            ) = anterior
            raise
        return producto

    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminar()
