"""Integrante A - Epica 1: Gestion de categorias."""

from consola.entrada import confirmar, pedir_id, pedir_texto, pedir_validado
from consola.estilos import console, mensaje_aviso, mensaje_exito, mostrar_tabla_categorias, mostrar_titulo
from entidades import Usuario
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-01 (admin y cliente)."""
    mostrar_titulo("📂 Listado de categorias")
    _mostrar_activas(servicios)


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-02."""
    mostrar_titulo("➕ Crear categoria")
    nombre = pedir_validado("Nombre: ", servicios.categorias.validar_nombre_unico)
    descripcion = pedir_texto("Descripcion: ")
    categoria = servicios.categorias.crear(nombre, descripcion)
    mensaje_exito(f"Categoria '{categoria.nombre}' creada con id {categoria.id}.")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-03."""
    mostrar_titulo("✍️  Editar categoria")
    if not _mostrar_activas(servicios):
        return
    categoria = servicios.categorias.buscar_por_id(pedir_id("\nId de la categoria: "))
    console.print("[dim]Presione Enter para conservar el valor actual.[/dim]\n")
    nombre = pedir_validado(
        f"Nombre [{categoria.nombre}]: ",
        lambda valor: servicios.categorias.validar_nombre_unico(valor, categoria.id),
        opcional=True,
    )
    descripcion = pedir_texto(f"Descripcion [{categoria.descripcion}]: ", opcional=True)
    if nombre is None and descripcion is None:
        mensaje_aviso("No se realizaron cambios.")
        return
    servicios.categorias.editar(categoria.id, nombre, descripcion)
    mensaje_exito(f"Categoria '{categoria.nombre}' actualizada.")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-CAT-04."""
    mostrar_titulo("❌ Eliminar categoria")
    if not _mostrar_activas(servicios):
        return
    categoria = servicios.categorias.buscar_por_id(pedir_id("\nId de la categoria: "))
    if not confirmar(f"¿Confirma eliminar la categoria '{categoria.nombre}'?"):
        mensaje_aviso("Operacion cancelada.")
        return
    servicios.categorias.eliminar(categoria.id)
    mensaje_exito(f"Categoria '{categoria.nombre}' eliminada.")


def _mostrar_activas(servicios: Servicios) -> bool:
    """Muestra la tabla; devuelve False si no hay categorias para operar."""
    categorias = servicios.categorias.listar_activos()
    if not categorias:
        mensaje_aviso("No hay categorias cargadas.")
        return False
    mostrar_tabla_categorias(categorias)
    return True
