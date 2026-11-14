import os

# Codigos ANSI para colorear la consola sin usar librerias (pueden no estar instaladas).
AMARILLO = "\033[33m"
CYAN = "\033[96m"
RESET = "\033[0m"   # vuelve al color por defecto
NEGRITA = "\033[1m"
# Cursor arriba + borrar pantalla + borrar historial de desplazamiento
BORRAR_TODO = "\033[H\033[2J\033[3J"


def limpiar_consola() -> None:
    """cls/clear no borra el historial en VS Code ni Windows Terminal: la secuencia ANSI si."""
    os.system("cls" if os.name == "nt" else "clear")
    print(BORRAR_TODO, end="", flush=True)


def verificar_dependencias() -> bool:
    """Comprueba questionary y rich antes de iniciar el programa."""
    faltantes: list[str] = []
    try:
        import questionary  # noqa: F401
    except ImportError:
        faltantes.append("questionary")
    try:
        import rich  # noqa: F401
    except ImportError:
        faltantes.append("rich")
    if not faltantes:
        return True
    print(f"\n{AMARILLO}{NEGRITA}Faltan dependencias: {', '.join(faltantes)}{RESET}")
    print(f"{CYAN}Ejecute: pip install -r requirements.txt{RESET}")
    input(f"\n{NEGRITA}Presione Enter para continuar...{RESET}")
    return False
