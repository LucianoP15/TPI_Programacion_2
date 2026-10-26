"""Pantalla de inicio de sesion (auxiliar, ya resuelta). La verificacion real es UsuarioServicio.autenticar() [A]."""

import questionary

from consola.entrada import OperacionCancelada, limpiar_consola, pedir_contrasenia, pedir_texto
from consola.estilos import ESTILO_MENU, console, mensaje_aviso, mensaje_error, mostrar_titulo
from entidades import Usuario
from excepciones import CredencialesInvalidasError
from servicios import UsuarioServicio

MAX_INTENTOS_LOGIN: int = 3


def iniciar_sesion(usuarios: UsuarioServicio) -> Usuario | None:
    """Devuelve el usuario logueado o None si se agotaron los intentos / se cancelo."""
    limpiar_consola()
    mostrar_titulo("FOOD STORE - INICIO DE SESION")

    for intento in range(1, MAX_INTENTOS_LOGIN + 1):
        try:
            mail = pedir_texto("📧 Mail: ")
            contrasenia = pedir_contrasenia("🔑 Contraseña: ")
            usuario = usuarios.autenticar(mail or "", contrasenia)
        except CredencialesInvalidasError as e:
            restantes = MAX_INTENTOS_LOGIN - intento
            mensaje_error(f"{e.mensaje}. Intentos restantes: {restantes}")
            continue
        except OperacionCancelada:
            return None
        except NotImplementedError:
            # TODO [A] BORRAR este except cuando autenticar() este implementado
            return _ingreso_modo_desarrollo(usuarios)

        console.print(
            f"\n[bold green]Bienvenido/a, {usuario.nombre_completo} "
            f"[{usuario.rol.name}][/bold green]"
        )
        input("\nPresione Enter para continuar...")
        return usuario

    mensaje_error("Se agotaron los intentos. El programa se cerrara.")
    return None


def _ingreso_modo_desarrollo(usuarios: UsuarioServicio) -> Usuario | None:
    """Solo para poder navegar los menus mientras autenticar() no existe."""
    mensaje_aviso("UsuarioServicio.autenticar() todavia no esta implementado.")
    console.print("[dim]Modo desarrollo: elegi con que usuario entrar.[/dim]\n")
    activos = usuarios.listar_activos()
    if not activos:
        mensaje_error("No hay usuarios cargados.")
        return None
    return questionary.select(
        "Entrar como:",
        choices=[questionary.Choice(f"{u.nombre_completo} [{u.rol.name}]", value=u) for u in activos],
        style=ESTILO_MENU,
    ).ask()
