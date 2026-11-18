"""Pantalla de inicio de sesion. La verificacion la hace UsuarioServicio.autenticar()."""

import getpass

from consola.entrada import limpiar_consola
from consola.estilos import console, mensaje_error, mostrar_titulo
from entidades import Usuario
from excepciones import CredencialesInvalidasError, DatoInvalidoError
from servicios import UsuarioServicio

MAX_INTENTOS_LOGIN: int = 3


def iniciar_sesion(usuarios: UsuarioServicio) -> Usuario | None:
    """Devuelve el usuario logueado o None si se agotaron los intentos."""
    limpiar_consola()
    mostrar_titulo("FOOD STORE - INICIO DE SESION")

    # Cualquier error (mail vacio, mal formado o credenciales) consume uno de los 3 intentos
    for intento in range(1, MAX_INTENTOS_LOGIN + 1):
        try:
            mail = input("📧 Mail: ").strip()
            Usuario.validar_formato_mail(mail)
            contrasenia = getpass.getpass("🔑 Contraseña: ").strip()
            usuario = usuarios.autenticar(mail, contrasenia)
        except (DatoInvalidoError, CredencialesInvalidasError) as e:
            restantes = MAX_INTENTOS_LOGIN - intento
            mensaje_error(f"{e.mensaje}. Intentos restantes: {restantes}")
            continue

        console.print(
            f"\n[bold green]Bienvenido/a, {usuario.nombre_completo} "
            f"[{usuario.rol.name}][/bold green]"
        )
        input("\nPresione Enter para continuar...")
        return usuario

    mensaje_error("Se agotaron los intentos. El programa se cerrara.")
    return None

