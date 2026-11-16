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
    from entidades import Base, Categoria, Producto, Usuario  # noqa: F401
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
    probar("Listar disponibles", lambda: len(s.productos.listar_disponibles()))
    # TODO [B] agregar casos:
    #  - precio negativo                    -> PrecioInvalidoError
    #  - stock negativo                     -> DatoInvalidoError
    #  - categoria inexistente              -> EntidadNoEncontradaError

    seccion("4. Pedidos [B]")
    s = nuevo_entorno()
    cliente = s.usuarios.listar_activos()[1]
    muzza = s.productos.listar_activos()[0]  # stock 5
    probar(
        "Pedido con stock insuficiente",
        lambda: s.pedidos.crear(cliente.id, FormaPago.EFECTIVO, [(muzza.id, 99)]),
        StockInsuficienteError,
    )
    # TODO [B] agregar casos:
    #  - pedido valido: total correcto y stock descontado
    #  - mismo producto dos veces -> un solo detalle con la cantidad sumada
    #  - transicion invalida (TERMINADO -> PENDIENTE)  -> OperacionNoPermitidaError
    #  - cancelar devuelve stock
    #  - eliminar pedido marca detalles como eliminados

    # ------------------------------------------------------------------
    console.print(
        f"\n[bold]Resumen:[/bold] [green]{resultados['ok']} OK[/green] · "
        f"[red]{resultados['falla']} fallas[/red] · "
        f"[yellow]{resultados['pendiente']} pendientes[/yellow]\n"
    )


if __name__ == "__main__":
    main()
