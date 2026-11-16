from consola.dependencias import limpiar_consola, verificar_dependencias


def main() -> None:
    limpiar_consola()
    if not verificar_dependencias():
        return

    # Se importan despues de verificar que rich y questionary esten instalados
    from consola.estilos import console
    from consola.login import iniciar_sesion
    from consola.menu import crear_menu
    from datos_iniciales import cargar_datos_iniciales
    from servicios import crear_servicios

    servicios = crear_servicios()
    cargar_datos_iniciales(servicios)

    while True:
        sesion = iniciar_sesion(servicios.usuarios)
        if sesion is None:
            break
        menu = crear_menu(sesion, servicios)
        if not menu.mostrar():  # True = cerrar sesion, False = salir
            break

    console.print("\n[blue bold]PROGRAMA FINALIZADO.[/blue bold]\n")


if __name__ == "__main__":
    main()
