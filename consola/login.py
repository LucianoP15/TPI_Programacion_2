"""Pantalla de inicio de sesion. La verificacion la hace UsuarioServicio.autenticar()."""

from consola.entrada import OperacionCancelada, limpiar_consola, pedir_contrasenia, pedir_validado
from consola.estilos import console, mensaje_error, mostrar_titulo
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
            mail = pedir_validado("📧 Mail: ", Usuario.validar_formato_mail)
            contrasenia = pedir_contrasenia("🔑 Contraseña: ")
            usuario = usuarios.autenticar(mail or "", contrasenia)
        except CredencialesInvalidasError as e:
            restantes = MAX_INTENTOS_LOGIN - intento
            mensaje_error(f"{e.mensaje}. Intentos restantes: {restantes}")
            continue
        except OperacionCancelada:
            return None

        console.print(
            f"\n[bold green]Bienvenido/a, {usuario.nombre_completo} "
            f"[{usuario.rol.name}][/bold green]"
        )
        input("\nPresione Enter para continuar...")
        return usuario

    mensaje_error("Se agotaron los intentos. El programa se cerrara.")
    return None

