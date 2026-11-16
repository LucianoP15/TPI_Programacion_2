from entidades import Pedido, Usuario
from enums import Estado, FormaPago
from excepciones import DatoInvalidoError, EntidadNoEncontradaError, OperacionNoPermitidaError
from servicios.producto_servicio import ProductoServicio
from servicios.servicio_base import ServicioBase
from servicios.usuario_servicio import UsuarioServicio

# Regla de negocio ya definida por la consigna (auxiliar): estado actual -> estados permitidos
TRANSICIONES_VALIDAS: dict[Estado, set[Estado]] = {
    Estado.PENDIENTE: {Estado.CONFIRMADO, Estado.CANCELADO},
    Estado.CONFIRMADO: {Estado.TERMINADO, Estado.CANCELADO},
    Estado.TERMINADO: set(),
    Estado.CANCELADO: set(),
}

# Estados en los que el stock ya no esta "tomado" por el pedido
ESTADOS_FINALES: set[Estado] = {Estado.TERMINADO, Estado.CANCELADO}


class PedidoServicio(ServicioBase[Pedido]):
    """Integrante B."""

    nombre_entidad = "Pedido"

    def __init__(self, usuarios: UsuarioServicio, productos: ProductoServicio) -> None:
        super().__init__()
        self._usuarios: UsuarioServicio = usuarios
        self._productos: ProductoServicio = productos

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        return [p for p in self.listar_activos() if p.usuario == usuario]

    def buscar_de_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.usuario != usuario:
            # Mismo mensaje que si no existiera: no se revela que el pedido es de otro
            raise EntidadNoEncontradaError(f"{self.nombre_entidad} con id {id_pedido} no encontrado/a")
        return pedido

    def crear(
        self,
        id_usuario: int,
        forma_pago: FormaPago,
        items: list[tuple[int, int]],
    ) -> Pedido:
        """items = [(id_producto, cantidad), ...]"""
        if not items:
            raise DatoInvalidoError("El pedido debe tener al menos un producto")
        usuario = self._usuarios.buscar_por_id(id_usuario)
        pedido = Pedido(usuario, forma_pago)
        for id_producto, cantidad in items:
            producto = self._productos.buscar_por_id(id_producto)
            pedido.agregar_detalle(cantidad, producto)
        pedido.calcular_total()

        # Recien aca se toca la coleccion y el stock: si algo fallo antes, no quedo nada a medias
        self._descontar_stock(pedido)
        self.registrar(pedido)
        usuario.agregar_pedido(pedido)
        return pedido

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if not isinstance(nuevo_estado, Estado):
            raise DatoInvalidoError("Estado inválido")
        if nuevo_estado not in TRANSICIONES_VALIDAS[pedido.estado]:
            raise OperacionNoPermitidaError(
                f"No se puede pasar de {pedido.estado.value} a {nuevo_estado.value}"
            )
        if nuevo_estado == Estado.CANCELADO:
            self._devolver_stock(pedido)
        pedido.estado = nuevo_estado
        return pedido

    def cambiar_forma_pago(self, id_pedido: int, forma_pago: FormaPago) -> Pedido:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado in ESTADOS_FINALES:
            raise OperacionNoPermitidaError(
                f"No se puede cambiar la forma de pago de un pedido {pedido.estado.value.lower()}"
            )
        pedido.forma_pago = forma_pago
        return pedido

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        if pedido.estado not in ESTADOS_FINALES:
            self._devolver_stock(pedido)
        pedido.eliminar()

    def _descontar_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock -= detalle.cantidad

    def _devolver_stock(self, pedido: Pedido) -> None:
        for detalle in pedido.detalles:
            detalle.producto.stock += detalle.cantidad
