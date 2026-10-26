from entidades import Pedido, Usuario
from enums import Estado, FormaPago
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


class PedidoServicio(ServicioBase[Pedido]):
    """Integrante B."""

    nombre_entidad = "Pedido"

    def __init__(self, usuarios: UsuarioServicio, productos: ProductoServicio) -> None:
        super().__init__()
        self._usuarios: UsuarioServicio = usuarios
        self._productos: ProductoServicio = productos

    def listar_por_usuario(self, usuario: Usuario) -> list[Pedido]:
        # TODO [B] HU-PED-05: pedidos activos de ese usuario
        raise NotImplementedError("PedidoServicio.listar_por_usuario")

    def buscar_de_usuario(self, id_pedido: int, usuario: Usuario) -> Pedido:
        # TODO [B] HU-PED-05: si el pedido es de otro usuario -> EntidadNoEncontradaError
        raise NotImplementedError("PedidoServicio.buscar_de_usuario")

    def crear(
        self,
        id_usuario: int,
        forma_pago: FormaPago,
        items: list[tuple[int, int]],
    ) -> Pedido:
        """items = [(id_producto, cantidad), ...]"""
        # TODO [B] HU-PED-02
        #  - usuario = self._usuarios.buscar_por_id(id_usuario)
        #  - pedido = Pedido(usuario, forma_pago)
        #  - por cada item: pedido.agregar_detalle(cantidad, producto)   (OBLIGATORIO)
        #  - pedido.calcular_total()                                     (OBLIGATORIO)
        #  - si algo falla, la excepcion sube y NO se registra nada ni se toca stock
        #  - si todo ok: descontar stock, registrar, usuario.agregar_pedido(pedido), devolver
        raise NotImplementedError("PedidoServicio.crear")

    def cambiar_estado(self, id_pedido: int, nuevo_estado: Estado) -> Pedido:
        # TODO [B] HU-PED-03
        #  - si nuevo_estado no esta en TRANSICIONES_VALIDAS[pedido.estado] -> OperacionNoPermitidaError
        #  - si pasa a CANCELADO -> self._devolver_stock(pedido)
        raise NotImplementedError("PedidoServicio.cambiar_estado")

    def cambiar_forma_pago(self, id_pedido: int, forma_pago: FormaPago) -> Pedido:
        # TODO [B] HU-PED-03
        raise NotImplementedError("PedidoServicio.cambiar_forma_pago")

    def eliminar(self, id_pedido: int) -> None:
        # TODO [B] HU-PED-04
        #  - si no esta TERMINADO ni CANCELADO -> devolver stock
        #  - pedido.eliminar()  (ya marca tambien los detalles)
        raise NotImplementedError("PedidoServicio.eliminar")

    def _descontar_stock(self, pedido: Pedido) -> None:
        # TODO [B]
        raise NotImplementedError("PedidoServicio._descontar_stock")

    def _devolver_stock(self, pedido: Pedido) -> None:
        # TODO [B]
        raise NotImplementedError("PedidoServicio._devolver_stock")
