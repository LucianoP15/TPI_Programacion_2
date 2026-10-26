"""
Menus por rol resueltos con polimorfismo (auxiliar, ya resuelto).
El rol se pregunta en UN solo lugar: crear_menu(). Despues main solo llama a menu.mostrar().
Las pantallas (lo que hay que desarrollar) estan en consola/pantallas/.
"""

from abc import ABC, abstractmethod
from collections.abc import Callable

import questionary

from consola.entrada import OperacionCancelada, limpiar_consola, pausar
from consola.estilos import (
    ESTILO_MENU,
    mensaje_aviso,
    mensaje_error,
    mensaje_pendiente,
    mostrar_titulo,
)
from consola.pantallas import categorias, pedidos, productos, usuarios
from entidades import Usuario
from enums import Rol
from excepciones import FoodStoreError
from servicios import Servicios

Pantalla = Callable[[Servicios, Usuario], None]

CERRAR_SESION: str = "cerrar"
SALIR: str = "salir"
VOLVER: str = "volver"


class Menu(ABC):
    def __init__(self, usuario: Usuario, servicios: Servicios) -> None:
        self._usuario: Usuario = usuario
        self._servicios: Servicios = servicios

    @abstractmethod
    def mostrar(self) -> bool:
        """True = cerrar sesion, False = salir del programa."""
        ...

    # ------------------------------------------------------------------
    # Auxiliares comunes a todos los menus
    # ------------------------------------------------------------------
    def _ejecutar(self, pantalla: Pantalla) -> None:
        """Ejecuta una pantalla y captura TODO error: el menu nunca se cae."""
        limpiar_consola()
        try:
            pantalla(self._servicios, self._usuario)
        except OperacionCancelada:
            mensaje_aviso("Operacion cancelada.")
        except NotImplementedError as e:
            mensaje_pendiente(str(e))
        except FoodStoreError as e:
            mensaje_error(e.mensaje)
        except ValueError as e:
            mensaje_error(f"Dato invalido: {e}")
        pausar()

    @staticmethod
    def _opciones_numeradas(etiquetas: list[str]) -> list[questionary.Choice]:
        return [
            questionary.Choice(etiqueta, value=etiqueta, shortcut_key=str(i))
            for i, etiqueta in enumerate(etiquetas, start=1)
        ]

    def _menu_principal(self, titulo: str, opciones: dict[str, Callable[[], None]]) -> bool:
        while True:
            limpiar_consola()
            mostrar_titulo(titulo)
            choices = self._opciones_numeradas(list(opciones))
            choices.append(questionary.Separator())
            choices.append(questionary.Choice("🔒 Cerrar sesion", value=CERRAR_SESION, shortcut_key="9"))
            choices.append(questionary.Choice("🚪 Salir", value=SALIR, shortcut_key="0"))

            seleccion = questionary.select(
                "Seleccione una opcion:", choices=choices, style=ESTILO_MENU, use_shortcuts=True
            ).ask()

            if seleccion == CERRAR_SESION:
                return True
            if seleccion in (SALIR, None):
                return False
            opciones[seleccion]()

    def _submenu(self, titulo: str, opciones: dict[str, Pantalla]) -> None:
        while True:
            limpiar_consola()
            mostrar_titulo(titulo)
            choices = self._opciones_numeradas(list(opciones))
            choices.append(questionary.Separator())
            choices.append(questionary.Choice("↩️  Volver", value=VOLVER, shortcut_key="0"))

            seleccion = questionary.select(
                "Seleccione una opcion:", choices=choices, style=ESTILO_MENU, use_shortcuts=True
            ).ask()

            if seleccion in (VOLVER, None):
                return
            self._ejecutar(opciones[seleccion])


class MenuAdministrador(Menu):
    def mostrar(self) -> bool:
        return self._menu_principal(
            f"FOOD STORE - ADMINISTRADOR ({self._usuario.nombre_completo})",
            {
                "📂 Categorias": lambda: self._submenu("--- CATEGORIAS ---", {
                    "📋 Listar":   categorias.listar,
                    "➕ Crear":    categorias.crear,
                    "✍️  Editar":   categorias.editar,
                    "❌ Eliminar": categorias.eliminar,
                }),
                "🍔 Productos": lambda: self._submenu("--- PRODUCTOS ---", {
                    "📋 Listar":   productos.listar,
                    "➕ Crear":    productos.crear,
                    "✍️  Editar":   productos.editar,
                    "❌ Eliminar": productos.eliminar,
                }),
                "👥 Usuarios": lambda: self._submenu("--- USUARIOS ---", {
                    "📋 Listar":   usuarios.listar,
                    "➕ Crear":    usuarios.crear,
                    "✍️  Editar":   usuarios.editar,
                    "❌ Eliminar": usuarios.eliminar,
                }),
                "🧾 Pedidos": lambda: self._submenu("--- PEDIDOS ---", {
                    "📋 Listar":                       pedidos.listar,
                    "🔍 Ver detalle":                  pedidos.ver_detalle,
                    "➕ Crear":                        pedidos.crear,
                    "🚦 Cambiar estado / forma pago":  pedidos.actualizar,
                    "❌ Eliminar":                     pedidos.eliminar,
                }),
            },
        )


class MenuCliente(Menu):
    """Solo consulta: ninguna opcion modifica datos."""

    def mostrar(self) -> bool:
        return self._menu_principal(
            f"FOOD STORE - CLIENTE ({self._usuario.nombre_completo})",
            {
                "📂 Ver categorias":           lambda: self._ejecutar(categorias.listar),
                "🍔 Ver productos disponibles": lambda: self._ejecutar(productos.listar_disponibles),
                "🧾 Mis pedidos":              lambda: self._ejecutar(pedidos.mis_pedidos),
                "👤 Mis datos":                lambda: self._ejecutar(usuarios.mis_datos),
            },
        )


def crear_menu(usuario: Usuario, servicios: Servicios) -> Menu:
    """Unico lugar donde se pregunta por el rol."""
    if usuario.rol == Rol.ADMIN:
        return MenuAdministrador(usuario, servicios)
    return MenuCliente(usuario, servicios)


__all__ = ["Menu", "MenuAdministrador", "MenuCliente", "crear_menu"]
