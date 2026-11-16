"""
Pruebas del modelo y los servicios, SIN menu. Ejecutar: python pruebas.py
Cada integrante completa su seccion. Las pruebas de la seccion 0 ya funcionan y sirven de ejemplo.
"""

from collections.abc import Callable

from consola.dependencias import verificar_dependencias


def main() -> None:
    if not verificar_dependencias():
        return

    from consola.estilos import console, mostrar_titulo
    from entidades import Base, Categoria, Pedido, Producto, Usuario  # noqa: F401
    from enums import Estado, FormaPago, Rol  # noqa: F401
    from excepciones import (  # noqa: F401
        CredencialesInvalidasError,
        DatoInvalidoError,
        DuplicadoError,
        EntidadNoEncontradaError,
        OperacionNoPermitidaError,
        PrecioInvalidoError,
        StockInsuficienteError,
    )
    from servicios import Servicios, crear_servicios

    resultados: dict[str, int] = {"ok": 0, "falla": 0, "pendiente": 0}

    # ------------------------------------------------------------------
    # Auxiliar: ejecuta un caso y muestra el resultado
    # ------------------------------------------------------------------
    def probar(
        descripcion: str,
        accion: Callable[[], object],
        excepcion_esperada: type[Exception] | None = None,
    ) -> None:
        try:
            resultado = accion()
        except NotImplementedError as e:
            resultados["pendiente"] += 1
            console.print(f"  [yellow]🚧 PENDIENTE[/yellow] {descripcion} [dim]({e})[/dim]")
            return
        except Exception as e:
            if excepcion_esperada and isinstance(e, excepcion_esperada):
                resultados["ok"] += 1
                console.print(f"  [green]✅ OK[/green]        {descripcion} [dim]-> {type(e).__name__}: {e}[/dim]")
            else:
                resultados["falla"] += 1
                console.print(f"  [red]❌ FALLA[/red]     {descripcion} [dim]-> {type(e).__name__}: {e}[/dim]")
            return
        if excepcion_esperada:
            resultados["falla"] += 1
            console.print(f"  [red]❌ FALLA[/red]     {descripcion} [dim]-> se esperaba {excepcion_esperada.__name__}[/dim]")
        else:
            resultados["ok"] += 1
            extra = f" -> {resultado}" if resultado is not None else ""
            console.print(f"  [green]✅ OK[/green]        {descripcion}[dim]{extra}[/dim]")

    def afirmar(condicion: bool, mensaje: str = "La condicion no se cumple") -> None:
        if not condicion:
            raise AssertionError(mensaje)

    def seccion(titulo: str) -> None:
        console.print(f"\n[bold bright_blue]━━ {titulo} ━━[/bold bright_blue]")

    def nuevo_entorno() -> Servicios:
        """Servicios con 1 admin, 1 cliente, 1 categoria y 1 producto (stock 5)."""
        s = crear_servicios()
        s.usuarios.registrar(Usuario("Ana", "Perez", "admin@foodstore.com", "261", "admin123", Rol.ADMIN))
        s.usuarios.registrar(Usuario("Juan", "Gomez", "juan@foodstore.com", "261", "cliente123", Rol.USUARIO))
        cat = s.categorias.registrar(Categoria("Pizzas", "A la piedra"))
        s.productos.registrar(Producto("Muzza", 1000.0, "-", 5, "-", True, cat))
        return s

    mostrar_titulo("FOOD STORE - PRUEBAS")

    # ==================================================================
    # 0. Auxiliares (ya resueltas, sirven de ejemplo)
    # ==================================================================
    seccion("0. Base y servicio base")
    probar("Base no se puede instanciar", lambda: Base(), TypeError)
    c1, c2 = Categoria("A", "a"), Categoria("B", "b")
    probar("Ids autoincrementales", lambda: afirmar(c2.id == c1.id + 1))
    probar("__eq__ compara por id", lambda: afirmar(c1 == c1 and c1 != c2))
    s0 = nuevo_entorno()
    probar("buscar_por_id inexistente", lambda: s0.categorias.buscar_por_id(999), EntidadNoEncontradaError)

    # ==================================================================
    # 1. Integrante A: categorias y usuarios
    # ==================================================================
    seccion("1. Categorias [A]")
    s = nuevo_entorno()
    pizzas = s.categorias.listar_activos()[0]
    probar("Crear categoria valida", lambda: s.categorias.crear("Empanadas", "Al horno"))
    probar("Nombre repetido (otra capitalizacion)", lambda: s.categorias.crear("  PIZZAS ", "Otra"), DuplicadoError)
    probar("Nombre vacio", lambda: s.categorias.crear("   ", "Sin nombre"), DatoInvalidoError)
    probar("Descripcion vacia", lambda: s.categorias.crear("Postres", ""), DatoInvalidoError)
    probar("Editar id inexistente", lambda: s.categorias.editar(999, "X", None), EntidadNoEncontradaError)
    probar("Editar a su mismo nombre en otra capitalizacion", lambda: afirmar(s.categorias.editar(pizzas.id, "PIZZAS", None).nombre == "PIZZAS"))
    probar("Editar a un nombre ajeno", lambda: s.categorias.editar(pizzas.id, "empanadas", None), DuplicadoError)
    probar("Editar conservando valores (None)", lambda: afirmar(s.categorias.editar(pizzas.id, None, None).descripcion == "A la piedra"))
    probar("Eliminar categoria con productos activos", lambda: s.categorias.eliminar(pizzas.id), OperacionNoPermitidaError)
    empanadas = s.categorias.listar_activos()[1]
    probar("Eliminar categoria sin productos", lambda: s.categorias.eliminar(empanadas.id))
    probar("Nombre de categoria eliminada se puede reusar", lambda: s.categorias.crear("Empanadas", "De carne"))

    seccion("2. Usuarios y login [A]")
    s = nuevo_entorno()
    admin, juan = s.usuarios.listar_activos()
    probar("Login correcto", lambda: s.usuarios.autenticar("admin@foodstore.com", "admin123"))
    probar("Login con mail en mayusculas", lambda: s.usuarios.autenticar("  ADMIN@FoodStore.com ", "admin123"))
    probar("Contraseña incorrecta", lambda: s.usuarios.autenticar("admin@foodstore.com", "otra"), CredencialesInvalidasError)
    probar("Mail inexistente", lambda: s.usuarios.autenticar("nadie@foodstore.com", "admin123"), CredencialesInvalidasError)
    probar(
        "Crear usuario valido",
        lambda: s.usuarios.crear("Maria", "Lopez", "maria@foodstore.com", "261", "clave", Rol.USUARIO),
    )
    probar(
        "Mail duplicado (otra capitalizacion)",
        lambda: s.usuarios.crear("Otro", "Juan", "JUAN@foodstore.com", "261", "clave", Rol.USUARIO),
        DuplicadoError,
    )
    probar(
        "Mail sin @",
        lambda: s.usuarios.crear("Pepe", "Paz", "pepe.foodstore.com", "261", "clave", Rol.USUARIO),
        DatoInvalidoError,
    )
    probar(
        "Mail sin punto en el dominio",
        lambda: s.usuarios.crear("Pepe", "Paz", "pepe@foodstore", "261", "clave", Rol.USUARIO),
        DatoInvalidoError,
    )
    probar(
        "Nombre vacio",
        lambda: s.usuarios.crear("   ", "Paz", "pepe@foodstore.com", "261", "clave", Rol.USUARIO),
        DatoInvalidoError,
    )
    probar(
        "Apellido con numeros",
        lambda: s.usuarios.crear("Pepe", "Paz2", "pepe@foodstore.com", "261", "clave", Rol.USUARIO),
        DatoInvalidoError,
    )
    probar(
        "Contraseña vacia",
        lambda: s.usuarios.crear("Pepe", "Paz", "pepe@foodstore.com", "261", "  ", Rol.USUARIO),
        DatoInvalidoError,
    )
    probar("Editar conservando valores (None)", lambda: afirmar(s.usuarios.editar(juan.id).mail == "juan@foodstore.com"))
    probar("Editar celular", lambda: afirmar(s.usuarios.editar(juan.id, celular="2619999999").celular == "2619999999"))
    probar("Editar a un mail ajeno", lambda: s.usuarios.editar(juan.id, mail="admin@foodstore.com"), DuplicadoError)
    probar("Editar id inexistente", lambda: s.usuarios.editar(999, nombre="X"), EntidadNoEncontradaError)
    probar(
        "Admin se cambia su propio rol",
        lambda: s.usuarios.editar(admin.id, rol=Rol.USUARIO, usuario_sesion=admin),
        OperacionNoPermitidaError,
    )
    probar("Admin se elimina a si mismo", lambda: s.usuarios.eliminar(admin.id, admin), OperacionNoPermitidaError)
    probar("Eliminar otro usuario", lambda: s.usuarios.eliminar(juan.id, admin))
    probar("Login de usuario eliminado", lambda: s.usuarios.autenticar("juan@foodstore.com", "cliente123"), CredencialesInvalidasError)
    probar(
        "Mail de usuario eliminado sigue reservado",
        lambda: s.usuarios.crear("Juan", "Nuevo", "juan@foodstore.com", "261", "clave", Rol.USUARIO),
        DuplicadoError,
    )

    # ==================================================================
    # 2. Integrante B: productos y pedidos
    # ==================================================================
    seccion("3. Productos [B]")
    s = nuevo_entorno()
    cat = s.categorias.listar_activos()[0]
    muzza = s.productos.listar_activos()[0]  # stock 5
    probar("Listar disponibles", lambda: len(s.productos.listar_disponibles()))

    # --- crear ---
    def crear_producto(**cambios: object) -> object:
        datos: dict[str, object] = {
            "nombre": "Napo", "precio": 1200.0, "descripcion": "-", "stock": 3,
            "imagen": "-", "disponible": True, "id_categoria": cat.id,
        }
        datos.update(cambios)
        return s.productos.crear(**datos)  # type: ignore[arg-type]

    probar("Crear producto valido", lambda: crear_producto())
    probar("Crear con precio entero (se guarda como float)", lambda: afirmar(crear_producto(precio=500).precio == 500.0))
    probar("Crear con precio 0 (gratis) se permite", lambda: crear_producto(precio=0))
    probar("Precio negativo", lambda: crear_producto(precio=-1), PrecioInvalidoError)
    probar("Precio NaN", lambda: crear_producto(precio=float("nan")), PrecioInvalidoError)
    probar("Precio infinito", lambda: crear_producto(precio=float("inf")), PrecioInvalidoError)
    probar("Precio como texto", lambda: crear_producto(precio="100"), PrecioInvalidoError)
    probar("Precio booleano", lambda: crear_producto(precio=True), PrecioInvalidoError)
    probar("PrecioInvalidoError es un DatoInvalidoError", lambda: crear_producto(precio=-5), DatoInvalidoError)
    probar("Stock negativo", lambda: crear_producto(stock=-1), DatoInvalidoError)
    probar("Stock decimal", lambda: crear_producto(stock=2.5), DatoInvalidoError)
    probar("Stock booleano", lambda: crear_producto(stock=True), DatoInvalidoError)
    probar("Nombre vacio", lambda: crear_producto(nombre=""), DatoInvalidoError)
    probar("Nombre solo espacios", lambda: crear_producto(nombre="   "), DatoInvalidoError)
    probar("Nombre None", lambda: crear_producto(nombre=None), DatoInvalidoError)
    probar("Nombre se guarda sin espacios", lambda: afirmar(crear_producto(nombre="  Fugazza ").nombre == "Fugazza"))
    probar("Disponible no booleano", lambda: crear_producto(disponible="si"), DatoInvalidoError)
    probar("Categoria inexistente", lambda: crear_producto(id_categoria=999), EntidadNoEncontradaError)
    cat_borrada = s.categorias.registrar(Categoria("Vieja", "-"))
    cat_borrada.eliminar()
    probar("Categoria eliminada", lambda: crear_producto(id_categoria=cat_borrada.id), EntidadNoEncontradaError)
    cantidad_antes = len(s.productos.listar_todos())
    probar("Crear invalido no registra nada", lambda: crear_producto(precio=-1), PrecioInvalidoError)
    probar("...la coleccion no cambio", lambda: afirmar(len(s.productos.listar_todos()) == cantidad_antes))

    # --- listados ---
    s = nuevo_entorno()
    cat = s.categorias.listar_activos()[0]
    muzza = s.productos.listar_activos()[0]
    sin_stock = s.productos.registrar(Producto("Agua", 500.0, "-", 0, "-", True, cat))
    no_disp = s.productos.registrar(Producto("Fanta", 500.0, "-", 10, "-", False, cat))
    borrado = s.productos.registrar(Producto("Sprite", 500.0, "-", 10, "-", True, cat))
    borrado.eliminar()
    probar(
        "Disponibles excluye sin stock, no disponibles y eliminados",
        lambda: afirmar(s.productos.listar_disponibles() == [muzza]),
    )
    probar(
        "Listar activos incluye sin stock y no disponibles",
        lambda: afirmar(set(s.productos.listar_activos()) == {muzza, sin_stock, no_disp}),
    )
    otra_cat = s.categorias.registrar(Categoria("Bebidas", "-"))
    probar("Listar por categoria", lambda: afirmar(len(s.productos.listar_por_categoria(cat.id)) == 3))
    probar("Listar por categoria vacia", lambda: afirmar(s.productos.listar_por_categoria(otra_cat.id) == []))
    probar("Listar por categoria inexistente", lambda: s.productos.listar_por_categoria(999), EntidadNoEncontradaError)

    # --- editar ---
    probar("Editar sin cambios (todo None) conserva", lambda: afirmar(s.productos.editar(muzza.id).nombre == "Muzza"))
    probar("Editar precio", lambda: afirmar(s.productos.editar(muzza.id, precio=1500.0).precio == 1500.0))
    probar("Editar id inexistente", lambda: s.productos.editar(999, nombre="X"), EntidadNoEncontradaError)
    probar("Editar producto eliminado", lambda: s.productos.editar(borrado.id, nombre="X"), EntidadNoEncontradaError)
    probar("Editar con precio negativo", lambda: s.productos.editar(muzza.id, precio=-1), PrecioInvalidoError)
    probar(
        "Editar con nombre valido + stock invalido",
        lambda: s.productos.editar(muzza.id, nombre="Cambiado", stock=-3),
        DatoInvalidoError,
    )
    probar("...el nombre NO quedo a medias (todo o nada)", lambda: afirmar(muzza.nombre == "Muzza", muzza.nombre))
    probar("Editar a categoria inexistente", lambda: s.productos.editar(muzza.id, id_categoria=999), EntidadNoEncontradaError)
    probar("Editar categoria mueve el producto", lambda: s.productos.editar(muzza.id, id_categoria=otra_cat.id))
    probar(
        "...la categoria vieja ya no lo tiene y la nueva si",
        lambda: afirmar(muzza not in cat.productos and muzza in otra_cat.productos),
    )
    probar("Editar a stock 0 lo saca de disponibles", lambda: s.productos.editar(muzza.id, stock=0))
    probar("...ya no figura en disponibles", lambda: afirmar(muzza not in s.productos.listar_disponibles()))

    # --- eliminar ---
    probar("Eliminar producto", lambda: s.productos.eliminar(muzza.id))
    probar("...no aparece en activos", lambda: afirmar(muzza not in s.productos.listar_activos()))
    probar("...sigue en la coleccion (baja logica)", lambda: afirmar(muzza in s.productos.listar_todos()))
    probar("...ya no cuenta como activo en la categoria", lambda: afirmar(otra_cat.cantidad_productos_activos() == 0))
    probar("Eliminar dos veces", lambda: s.productos.eliminar(muzza.id), EntidadNoEncontradaError)
    probar("Eliminar id inexistente", lambda: s.productos.eliminar(999), EntidadNoEncontradaError)

    seccion("4. Pedidos [B]")
    s = nuevo_entorno()
    admin = s.usuarios.listar_activos()[0]
    cliente = s.usuarios.listar_activos()[1]
    cat = s.categorias.listar_activos()[0]
    muzza = s.productos.listar_activos()[0]  # stock 5, $1000
    napo = s.productos.registrar(Producto("Napo", 1500.0, "-", 10, "-", True, cat))
    probar(
        "Pedido con stock insuficiente",
        lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 99)]),
        StockInsuficienteError,
    )
    probar("...no se desconto stock", lambda: afirmar(muzza.stock == 5))
    probar("...no se registro el pedido", lambda: afirmar(len(s.pedidos.listar_todos()) == 0))

    # --- crear: casos de error (ninguno debe tocar stock ni la coleccion) ---
    probar("Pedido sin items", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, []), DatoInvalidoError)
    probar("Usuario inexistente", lambda: s.pedidos.crear(999, FormaPago.EFECTIVO, [(muzza.id, 1)]), EntidadNoEncontradaError)
    probar("Producto inexistente", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(999, 1)]), EntidadNoEncontradaError)
    probar("Cantidad 0", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 0)]), DatoInvalidoError)
    probar("Cantidad negativa", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, -2)]), DatoInvalidoError)
    probar("Cantidad decimal", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 1.5)]), DatoInvalidoError)
    probar("Cantidad booleana", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, True)]), DatoInvalidoError)
    probar("Forma de pago invalida", lambda: s.pedidos.crear(cliente.id, "Bitcoin", [(muzza.id, 1)]), DatoInvalidoError)
    probar(
        "Stock justo en el limite (5 de 5) en dos lineas: 3 + 3",
        lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 3), (muzza.id, 3)]),
        StockInsuficienteError,
    )
    probar(
        "Primer item ok y el segundo falla",
        lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(napo.id, 2), (muzza.id, 99)]),
        StockInsuficienteError,
    )
    probar("...el stock del primero NO se desconto", lambda: afirmar(napo.stock == 10 and muzza.stock == 5))
    probar("...seguimos sin pedidos registrados", lambda: afirmar(len(s.pedidos.listar_todos()) == 0))
    probar("...el usuario no tiene pedidos colgados", lambda: afirmar(len(cliente.pedidos) == 0))

    no_disp = s.productos.registrar(Producto("Fanta", 500.0, "-", 10, "-", False, cat))
    probar("Producto no disponible", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(no_disp.id, 1)]), OperacionNoPermitidaError)
    borrado = s.productos.registrar(Producto("Sprite", 500.0, "-", 10, "-", True, cat))
    borrado.eliminar()
    probar("Producto eliminado", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(borrado.id, 1)]), EntidadNoEncontradaError)
    ex = s.usuarios.registrar(Usuario("Ex", "Cliente", "ex@foodstore.com", "261", "x", Rol.USUARIO))
    ex.eliminar()
    probar("Usuario eliminado", lambda: s.pedidos.crear(ex.id, FormaPago.EFECTIVO, [(muzza.id, 1)]), EntidadNoEncontradaError)
    probar("Pedido() directo con usuario eliminado", lambda: Pedido(ex, FormaPago.EFECTIVO), OperacionNoPermitidaError)
    probar("Pedido() directo sin usuario", lambda: Pedido(None, FormaPago.EFECTIVO), OperacionNoPermitidaError)

    # --- crear: casos validos ---
    p1 = s.pedidos.crear(cliente.id, FormaPago.TARJETA, [(muzza.id, 2), (napo.id, 1)])
    probar("Pedido valido: total correcto (2x1000 + 1x1500)", lambda: afirmar(p1.total == 3500.0, str(p1.total)))
    probar("...stock descontado", lambda: afirmar(muzza.stock == 3 and napo.stock == 9))
    probar("...arranca PENDIENTE", lambda: afirmar(p1.estado == Estado.PENDIENTE))
    probar("...queda en el usuario", lambda: afirmar(p1 in cliente.pedidos))
    probar("...2 detalles", lambda: afirmar(len(p1.detalles) == 2))

    p2 = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(napo.id, 2), (napo.id, 3)])
    probar("Mismo producto dos veces -> un solo detalle", lambda: afirmar(len(p2.detalles) == 1))
    probar("...con la cantidad sumada (5)", lambda: afirmar(p2.detalles[0].cantidad == 5))
    probar("...total 5x1500", lambda: afirmar(p2.total == 7500.0))
    probar("...stock descontado una sola vez (9-5=4)", lambda: afirmar(napo.stock == 4, str(napo.stock)))

    p3 = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 3)])
    probar("Pedir TODO el stock que queda (3 de 3)", lambda: afirmar(muzza.stock == 0))
    probar("...ya no figura en disponibles", lambda: afirmar(muzza not in s.productos.listar_disponibles()))
    probar("...otro pedido de 1 falla", lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 1)]), StockInsuficienteError)

    probar(
        "Cambiar el precio NO altera pedidos ya hechos",
        lambda: (s.productos.editar(napo.id, precio=99999.0), afirmar(p2.total == 7500.0))[1],
    )
    s.productos.editar(napo.id, precio=1500.0)
    probar("Los detalles son una tupla (no se modifican desde afuera)", lambda: afirmar(isinstance(p1.detalles, tuple)))

    # --- entidad Pedido directo ---
    suelto = Pedido(cliente, FormaPago.EFECTIVO)
    probar("agregar_detalle valido", lambda: suelto.agregar_detalle(1, napo))
    probar("...total recalculado", lambda: afirmar(suelto.total == 1500.0))
    probar("buscar_detalle_por_producto existente", lambda: afirmar(suelto.buscar_detalle_por_producto(napo) is not None))
    probar("buscar_detalle_por_producto ausente -> None", lambda: afirmar(suelto.buscar_detalle_por_producto(no_disp) is None))
    probar("eliminar_detalle_por_producto", lambda: suelto.eliminar_detalle_por_producto(napo))
    probar("...total vuelve a 0", lambda: afirmar(suelto.total == 0))
    probar("...ya no lo encuentra", lambda: afirmar(suelto.buscar_detalle_por_producto(napo) is None))
    probar("eliminar detalle inexistente", lambda: suelto.eliminar_detalle_por_producto(napo), OperacionNoPermitidaError)
    probar("agregar_detalle con producto None", lambda: suelto.agregar_detalle(1, None), OperacionNoPermitidaError)
    probar("Estado con texto", lambda: setattr(suelto, "estado", "Terminado"), DatoInvalidoError)

    # --- cambiar estado ---
    probar("PENDIENTE -> PENDIENTE (mismo estado)", lambda: s.pedidos.cambiar_estado(p1.id, Estado.PENDIENTE), OperacionNoPermitidaError)
    probar("PENDIENTE -> TERMINADO (salteando)", lambda: s.pedidos.cambiar_estado(p1.id, Estado.TERMINADO), OperacionNoPermitidaError)
    probar("Estado como texto", lambda: s.pedidos.cambiar_estado(p1.id, "Confirmado"), DatoInvalidoError)
    probar("Estado de pedido inexistente", lambda: s.pedidos.cambiar_estado(999, Estado.CONFIRMADO), EntidadNoEncontradaError)
    probar("PENDIENTE -> CONFIRMADO", lambda: s.pedidos.cambiar_estado(p1.id, Estado.CONFIRMADO))
    probar("...confirmar NO toca stock", lambda: afirmar(muzza.stock == 0 and napo.stock == 4))
    probar("CONFIRMADO -> TERMINADO", lambda: s.pedidos.cambiar_estado(p1.id, Estado.TERMINADO))
    probar("Transicion invalida TERMINADO -> PENDIENTE", lambda: s.pedidos.cambiar_estado(p1.id, Estado.PENDIENTE), OperacionNoPermitidaError)
    probar("TERMINADO -> CANCELADO", lambda: s.pedidos.cambiar_estado(p1.id, Estado.CANCELADO), OperacionNoPermitidaError)
    probar("...el stock no volvio (terminado no devuelve)", lambda: afirmar(muzza.stock == 0 and napo.stock == 4))

    probar("Cancelar desde PENDIENTE", lambda: s.pedidos.cambiar_estado(p3.id, Estado.CANCELADO))
    probar("...cancelar devuelve stock (0+3)", lambda: afirmar(muzza.stock == 3, str(muzza.stock)))
    probar("Cancelar dos veces", lambda: s.pedidos.cambiar_estado(p3.id, Estado.CANCELADO), OperacionNoPermitidaError)
    probar("...no devolvio stock dos veces", lambda: afirmar(muzza.stock == 3, str(muzza.stock)))
    probar("CANCELADO -> CONFIRMADO (resucitar)", lambda: s.pedidos.cambiar_estado(p3.id, Estado.CONFIRMADO), OperacionNoPermitidaError)

    s.pedidos.cambiar_estado(p2.id, Estado.CONFIRMADO)
    probar("Cancelar desde CONFIRMADO", lambda: s.pedidos.cambiar_estado(p2.id, Estado.CANCELADO))
    probar("...devuelve stock (4+5)", lambda: afirmar(napo.stock == 9, str(napo.stock)))

    # --- forma de pago ---
    p4 = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(napo.id, 1)])
    probar("Cambiar forma de pago", lambda: afirmar(s.pedidos.cambiar_forma_pago(p4.id, FormaPago.TRANSFERENCIA).forma_pago == FormaPago.TRANSFERENCIA))
    probar("Forma de pago invalida (texto)", lambda: s.pedidos.cambiar_forma_pago(p4.id, "Tarjeta"), DatoInvalidoError)
    probar("...conserva la anterior", lambda: afirmar(p4.forma_pago == FormaPago.TRANSFERENCIA))
    probar("Forma de pago de pedido terminado", lambda: s.pedidos.cambiar_forma_pago(p1.id, FormaPago.EFECTIVO), OperacionNoPermitidaError)
    probar("Forma de pago de pedido cancelado", lambda: s.pedidos.cambiar_forma_pago(p3.id, FormaPago.EFECTIVO), OperacionNoPermitidaError)

    # --- eliminar ---
    stock_napo = napo.stock
    probar("Eliminar pedido PENDIENTE", lambda: s.pedidos.eliminar(p4.id))
    probar("...devuelve stock", lambda: afirmar(napo.stock == stock_napo + 1))
    probar("...marca detalles como eliminados", lambda: afirmar(len(p4.detalles) == 0))
    probar("...no aparece en activos", lambda: afirmar(p4 not in s.pedidos.listar_activos()))
    probar("Eliminar dos veces", lambda: s.pedidos.eliminar(p4.id), EntidadNoEncontradaError)
    probar("Cambiar estado de pedido eliminado", lambda: s.pedidos.cambiar_estado(p4.id, Estado.CONFIRMADO), EntidadNoEncontradaError)

    stock_muzza = muzza.stock
    probar("Eliminar pedido CANCELADO", lambda: s.pedidos.eliminar(p3.id))
    probar("...NO devuelve stock otra vez", lambda: afirmar(muzza.stock == stock_muzza, str(muzza.stock)))
    stock_napo = napo.stock
    probar("Eliminar pedido TERMINADO", lambda: s.pedidos.eliminar(p1.id))
    probar("...NO devuelve stock", lambda: afirmar(napo.stock == stock_napo))

    p5 = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(napo.id, 2)])
    s.productos.eliminar(napo.id)
    stock_napo = napo.stock
    probar("Eliminar pedido cuyo producto ya se borro", lambda: s.pedidos.eliminar(p5.id))
    probar("...igual devuelve el stock al producto", lambda: afirmar(napo.stock == stock_napo + 2))

    # --- por usuario (HU-PED-05) ---
    s = nuevo_entorno()
    admin = s.usuarios.listar_activos()[0]
    cliente = s.usuarios.listar_activos()[1]
    muzza = s.productos.listar_activos()[0]
    del_cliente = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 1)])
    del_admin = s.pedidos.crear(admin.id, FormaPago.EFECTIVO, [(muzza.id, 1)])
    borrado = s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 1)])
    s.pedidos.eliminar(borrado.id)
    probar("Listar por usuario: solo los suyos y activos", lambda: afirmar(s.pedidos.listar_por_usuario(cliente) == [del_cliente]))
    probar("Usuario sin pedidos -> lista vacia", lambda: afirmar(s.pedidos.listar_por_usuario(
        Usuario("N", "N", "n@n.com", "1", "x", Rol.USUARIO)) == []))
    probar("Buscar pedido propio", lambda: afirmar(s.pedidos.buscar_de_usuario(del_cliente.id, cliente) is del_cliente))
    probar("Buscar pedido de OTRO usuario", lambda: s.pedidos.buscar_de_usuario(del_admin.id, cliente), EntidadNoEncontradaError)
    probar("Buscar pedido propio eliminado", lambda: s.pedidos.buscar_de_usuario(borrado.id, cliente), EntidadNoEncontradaError)
    probar("Buscar con id de un producto (ids compartidos)", lambda: s.pedidos.buscar_de_usuario(muzza.id, cliente), EntidadNoEncontradaError)

    # ------------------------------------------------------------------
    console.print(
        f"\n[bold]Resumen:[/bold] [green]{resultados['ok']} OK[/green] · "
        f"[red]{resultados['falla']} fallas[/red] · "
        f"[yellow]{resultados['pendiente']} pendientes[/yellow]\n"
    )


if __name__ == "__main__":
    main()
