"""Integrante A - Epica 3: Gestion de usuarios."""

from consola.entrada import confirmar, elegir_enum, pedir_contrasenia, pedir_id, pedir_texto, pedir_validado
from consola.estilos import (
    console,
    mensaje_aviso,
    mensaje_exito,
    mostrar_ficha_usuario,
    mostrar_tabla_usuarios,
    mostrar_titulo,
)
from entidades import Usuario
from enums import Rol
from servicios import Servicios


def listar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-01 (nunca mostrar la contrasenia)."""
    mostrar_titulo("👥 Listado de usuarios")
    _mostrar_activos(servicios)


def crear(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-02. El mail se valida (formato y duplicado) apenas se ingresa."""
    mostrar_titulo("➕ Crear usuario")
    nombre = pedir_texto("Nombre: ")
    apellido = pedir_texto("Apellido: ")
    mail = pedir_validado("Mail: ", servicios.usuarios.validar_mail_disponible)
    celular = pedir_texto("Celular: ")
    contrasenia = pedir_contrasenia()
    rol = elegir_enum("Rol:", Rol)
    usuario = servicios.usuarios.crear(nombre, apellido, mail, celular, contrasenia, rol)
    mensaje_exito(f"Usuario '{usuario.nombre_completo}' creado con id {usuario.id}.")


def editar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-03. El propio rol no se ofrece: un admin no puede quitarse permisos."""
    mostrar_titulo("✍️  Editar usuario")
    if not _mostrar_activos(servicios):
        return
    usuario = servicios.usuarios.buscar_por_id(pedir_id("\nId del usuario: "))
    console.print("[dim]Presione Enter para conservar el valor actual.[/dim]\n")
    nombre = pedir_texto(f"Nombre [{usuario.nombre}]: ", opcional=True)
    apellido = pedir_texto(f"Apellido [{usuario.apellido}]: ", opcional=True)
    mail = pedir_validado(
        f"Mail [{usuario.mail}]: ",
        lambda valor: servicios.usuarios.validar_mail_disponible(valor, usuario.id),
        opcional=True,
    )
    celular = pedir_texto(f"Celular [{usuario.celular}]: ", opcional=True)
    contrasenia = pedir_contrasenia("Nueva contraseña: ") if confirmar("¿Cambiar la contraseña?") else None
    rol = None if usuario == sesion else elegir_enum(f"Rol [{usuario.rol.value}]:", Rol, opcional=True)
    if all(valor is None for valor in (nombre, apellido, mail, celular, contrasenia, rol)):
        mensaje_aviso("No se realizaron cambios.")
        return
    servicios.usuarios.editar(
        usuario.id, nombre, apellido, mail, celular, contrasenia, rol, usuario_sesion=sesion
    )
    mensaje_exito(f"Usuario '{usuario.nombre_completo}' actualizado.")


def eliminar(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-04 (un admin no puede eliminarse a si mismo)."""
    mostrar_titulo("❌ Eliminar usuario")
    if not _mostrar_activos(servicios):
        return
    usuario = servicios.usuarios.buscar_por_id(pedir_id("\nId del usuario: "))
    if not confirmar(f"¿Confirma eliminar al usuario '{usuario.nombre_completo}'?"):
        mensaje_aviso("Operacion cancelada.")
        return
    servicios.usuarios.eliminar(usuario.id, sesion)
    mensaje_exito(f"Usuario '{usuario.nombre_completo}' eliminado.")


def mis_datos(servicios: Servicios, sesion: Usuario) -> None:
    """HU-USR-05 (cliente)."""
    mostrar_titulo("👤 Mis datos")
    mostrar_ficha_usuario(sesion)


def _mostrar_activos(servicios: Servicios) -> bool:
    """Muestra la tabla; devuelve False si no hay usuarios para operar."""
    usuarios = servicios.usuarios.listar_activos()
    if not usuarios:
        mensaje_aviso("No hay usuarios cargados.")
        return False
    mostrar_tabla_usuarios(usuarios)
    return True
