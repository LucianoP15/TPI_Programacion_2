from collections.abc import Sequence

import questionary
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from entidades import Categoria, DetallePedido, Pedido, Producto, Usuario
from enums import Estado

ESTILO_MENU = questionary.Style([
    ("qmark",       "fg:#00bfff bold"),
    ("question",    "fg:#ffffff bold"),
    ("pointer",     "fg:#00bfff bold"),
    ("highlighted", "fg:#00bfff bold"),
    ("selected",    "fg:#aaffaa"),
    ("separator",   "fg:#555555"),
    ("instruction", "fg:#555555 italic"),
])

console = Console()

COLOR_ESTADO: dict[Estado, str] = {
    Estado.PENDIENTE: "yellow",
    Estado.CONFIRMADO: "bright_blue",
    Estado.TERMINADO: "green",
    Estado.CANCELADO: "red",
}


# ======================= TITULOS Y MENSAJES =======================
def mostrar_titulo(titulo: str) -> None:
    contenido = Text(titulo, justify="center")
    contenido.stylize("bold white")
    console.print(
        Panel(
            contenido,
            style="bold blue",
            border_style="bright_blue",
            padding=(1, 4),
        )
    )
    console.print()


def mensaje_exito(texto: str) -> None:
    console.print(f"\n[bold green]✅ {texto}[/bold green]")


def mensaje_error(texto: str) -> None:
    console.print(f"\n[bold red]❌ ERROR: {texto}[/bold red]")


def mensaje_aviso(texto: str) -> None:
    console.print(f"\n[bold yellow]⚠️  {texto}[/bold yellow]")


def mensaje_pendiente(nombre: str) -> None:
    console.print(
        Panel(
            Text(f"🚧 Funcionalidad pendiente de implementar\n{nombre}", justify="center"),
            border_style="yellow",
            style="yellow",
            padding=(1, 4),
        )
    )


# ======================= FORMATO =======================
def formatear_numero(numero: float, decimales: int | None = None) -> str:
    if decimales is None:
        return f"{numero:,}".replace(",", ".")
    texto = f"{numero:,.{decimales}f}"
    entero, decimal = texto.rsplit(".", 1)
    return f"{entero.replace(',', '.')},{decimal}"


def formatear_precio(valor: float) -> str:
    return f"$ {formatear_numero(valor, 2)}"


def formatear_estado(estado: Estado) -> str:
    color = COLOR_ESTADO[estado]
    return f"[bold {color}]{estado.value}[/bold {color}]"


# ======================= TABLAS =======================
def _crear_tabla() -> Table:
    return Table(
        box=box.ROUNDED,
        border_style="bright_blue",
        header_style="bold white",
        show_lines=False,
        expand=False,
    )


def _pie(cantidad: int, entidad: str) -> None:
    console.print(f"\n[dim]Total: {cantidad} {entidad}.[/dim]")


def mostrar_tabla_categorias(categorias: Sequence[Categoria]) -> None:
    tabla = _crear_tabla()
    tabla.add_column("🆔  Id",           style="dim",       justify="right")
    tabla.add_column("🏷️   Nombre",       style="bold cyan", min_width=18, no_wrap=True)
    tabla.add_column("📝  Descripcion",  style="white",     min_width=30)
    tabla.add_column("🍔  Productos",    style="white",     justify="right")
    for c in categorias:
        tabla.add_row(str(c.id), c.nombre, c.descripcion, str(c.cantidad_productos_activos()))
    console.print(tabla)
    _pie(len(categorias), "categoria/s")


def mostrar_tabla_productos(productos: Sequence[Producto]) -> None:
    tabla = _crear_tabla()
    tabla.add_column("🆔  Id",         style="dim",               justify="right")
    tabla.add_column("🍕  Nombre",     style="bold cyan",         min_width=18, no_wrap=True)
    tabla.add_column("💲  Precio",     style="white",             min_width=12, justify="right")
    tabla.add_column("📦  Stock",      style="white",             justify="right")
    tabla.add_column("🏷️   Categoria",  style="bold bright_white", min_width=14)
    tabla.add_column("✅  Disponible", justify="center")
    for p in productos:
        tabla.add_row(
            str(p.id),
            p.nombre,
            formatear_precio(p.precio),
            formatear_numero(p.stock),
            p.categoria.nombre,
            "[green]Si[/green]" if p.disponible else "[red]No[/red]",
        )
    console.print(tabla)
    _pie(len(productos), "producto/s")


def mostrar_tabla_usuarios(usuarios: Sequence[Usuario]) -> None:
    tabla = _crear_tabla()
    tabla.add_column("🆔  Id",       style="dim",               justify="right")
    tabla.add_column("👤  Nombre",   style="bold cyan",         min_width=20, no_wrap=True)
    tabla.add_column("📧  Mail",     style="white",             min_width=24)
    tabla.add_column("📱  Celular",  style="white")
    tabla.add_column("🔑  Rol",      style="bold bright_white")
    for u in usuarios:
        tabla.add_row(str(u.id), u.nombre_completo, u.mail, u.celular, u.rol.value)
    console.print(tabla)
    _pie(len(usuarios), "usuario/s")


def mostrar_tabla_pedidos(pedidos: Sequence[Pedido]) -> None:
    tabla = _crear_tabla()
    tabla.add_column("🆔  Id",          style="dim",       justify="right")
    tabla.add_column("📅  Fecha",       style="white")
    tabla.add_column("👤  Usuario",     style="bold cyan", min_width=18, no_wrap=True)
    tabla.add_column("🚦  Estado")
    tabla.add_column("💳  Forma pago",  style="white")
    tabla.add_column("💰  Total",       style="bold white", min_width=12, justify="right")
    for p in pedidos:
        tabla.add_row(
            str(p.id),
            f"{p.fecha:%d/%m/%Y}",
            p.usuario.nombre_completo,
            formatear_estado(p.estado),
            p.forma_pago.value,
            formatear_precio(p.total),
        )
    console.print(tabla)
    _pie(len(pedidos), "pedido/s")


def mostrar_tabla_detalles(pedido: Pedido) -> None:
    tabla = _crear_tabla()
    tabla.title = f"Pedido #{pedido.id} - {formatear_estado(pedido.estado)}"
    tabla.add_column("🍕  Producto",     style="bold cyan", min_width=18, no_wrap=True)
    tabla.add_column("🔢  Cantidad",     style="white",     justify="right")
    tabla.add_column("💲  P. unitario",  style="white",     justify="right")
    tabla.add_column("🧾  Subtotal",     style="white",     min_width=12, justify="right")
    detalles: tuple[DetallePedido, ...] = pedido.detalles
    for d in detalles:
        tabla.add_row(
            d.producto.nombre,
            str(d.cantidad),
            formatear_precio(d.precio_unitario),
            formatear_precio(d.subtotal),
        )
    tabla.add_section()
    tabla.add_row("[bold]TOTAL[/bold]", "", "", f"[bold bright_blue]{formatear_precio(pedido.total)}[/bold bright_blue]")
    console.print(tabla)


def mostrar_ficha_usuario(usuario: Usuario) -> None:
    contenido = (
        f"[dim]Nombre:[/dim]   [bold cyan]{usuario.nombre}[/bold cyan]\n"
        f"[dim]Apellido:[/dim] [bold cyan]{usuario.apellido}[/bold cyan]\n"
        f"[dim]Mail:[/dim]     {usuario.mail}\n"
        f"[dim]Celular:[/dim]  {usuario.celular}\n"
        f"[dim]Rol:[/dim]      [bold]{usuario.rol.value}[/bold]"
    )
    console.print(Panel(contenido, title="👤 Mis datos", border_style="bright_blue", padding=(1, 4), expand=False))
