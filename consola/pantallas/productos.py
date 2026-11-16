"""Integrante B - Epica 2: Gestion de productos."""

from consola.entrada import confirmar, pedir_decimal, pedir_entero, pedir_id, pedir_si_no, pedir_texto
from consola.estilos import (
    mensaje_aviso,
    mensaje_exito,
    mostrar_tabla_categorias,
    mostrar_tabla_productos,
    mostrar_titulo,
)
from entidades import Usuario
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-01 (admin): todos los no eliminados."""
    mostrar_titulo("🍔 Listado de productos")
    productos = servicios.productos.listar_activos()
    if not productos:
        mensaje_aviso("No hay productos cargados")
        return
    if confirmar("¿Filtrar por categoría?"):
        mostrar_tabla_categorias(servicios.categorias.listar_activos())
        id_cat = pedir_id("Id de la categoría: ")
        productos = servicios.productos.listar_por_categoria(id_cat)
        if not productos:
            mensaje_aviso("La categoría no tiene productos")
            return
    mostrar_tabla_productos(productos)


def listar_disponibles(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-01 (cliente): solo disponibles y con stock > 0."""
    mostrar_titulo("🍔 Productos disponibles")
    productos = servicios.productos.listar_disponibles()
    if not productos:
        mensaje_aviso("No hay productos disponibles en este momento")
        return
    mostrar_tabla_productos(productos)


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-02."""
    mostrar_titulo("➕ Crear producto")
    categorias = servicios.categorias.listar_activos()
    if not categorias:
        mensaje_aviso("Primero hay que cargar al menos una categoría")
        return
    nombre = pedir_texto("Nombre: ")
    descripcion = pedir_texto("Descripción: ")
    precio = pedir_decimal("Precio: ")
    stock = pedir_entero("Stock: ")
    imagen = pedir_texto("Imagen: ")
    disponible = pedir_si_no("¿Disponible?")
    mostrar_tabla_categorias(categorias)
    id_cat = pedir_id("Id de la categoría: ")
    producto = servicios.productos.crear(nombre, precio, descripcion, stock, imagen, disponible, id_cat)
    mensaje_exito(f"Producto creado con id {producto.id}.")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-03."""
    mostrar_titulo("✍️  Editar producto")
    productos = servicios.productos.listar_activos()
    if not productos:
        mensaje_aviso("No hay productos cargados")
        return
    mostrar_tabla_productos(productos)
    id_prod = pedir_id("Id del producto: ")
    producto = servicios.productos.buscar_por_id(id_prod)

    nombre = pedir_texto(f"Nombre [{producto.nombre}]: ", opcional=True)
    descripcion = pedir_texto(f"Descripción [{producto.descripcion}]: ", opcional=True)
    precio = pedir_decimal(f"Precio [{producto.precio}]: ", opcional=True)
    stock = pedir_entero(f"Stock [{producto.stock}]: ", opcional=True)
    imagen = pedir_texto(f"Imagen [{producto.imagen}]: ", opcional=True)
    disponible = pedir_si_no(f"¿Disponible? [{'Sí' if producto.disponible else 'No'}]", opcional=True)
    id_cat = None
    if confirmar(f"¿Cambiar la categoría? [{producto.categoria.nombre}]"):
        mostrar_tabla_categorias(servicios.categorias.listar_activos())
        id_cat = pedir_id("Id de la nueva categoría: ")

    servicios.productos.editar(id_prod, nombre, precio, descripcion, stock, imagen, disponible, id_cat)
    mensaje_exito("Producto actualizado.")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-PROD-04."""
    mostrar_titulo("❌ Eliminar producto")
    productos = servicios.productos.listar_activos()
    if not productos:
        mensaje_aviso("No hay productos cargados")
        return
    mostrar_tabla_productos(productos)
    id_prod = pedir_id("Id del producto: ")
    producto = servicios.productos.buscar_por_id(id_prod)
    if not confirmar(f"¿Seguro que querés eliminar '{producto.nombre}'?"):
        mensaje_aviso("No se eliminó el producto.")
        return
    servicios.productos.eliminar(id_prod)
    mensaje_exito("Producto eliminado.")
