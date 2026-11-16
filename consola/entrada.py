"""Lectura validada desde teclado (auxiliar). Ninguna funcion devuelve datos invalidos."""

import getpass
from collections.abc import Callable
from enum import Enum
from typing import TypeVar

import questionary

from consola.dependencias import limpiar_consola
from consola.estilos import ESTILO_MENU, console, formatear_numero
from excepciones import FoodStoreError

E = TypeVar("E", bound=Enum)

MAX_INTENTOS: int = 3
OPCION_NO_MODIFICAR: str = "(No modificar)"


class OperacionCancelada(Exception):
    """El usuario abandono la carga. El menu la captura y vuelve sin mostrar error."""


# ======================= PANTALLA =======================
def pausar() -> None:
    input("\nPresione Enter para continuar...")


def _error(texto: str) -> None:
    console.print(f"[bold red]{texto}[/bold red]")


def _manejar_max_intentos(intentos: int) -> int:
    """Suma un intento; al llegar al maximo pregunta si volver al menu."""
    intentos += 1
    if intentos < MAX_INTENTOS:
        return intentos
    if confirmar("Demasiados intentos. ¿Desea volver al menu?"):
        raise OperacionCancelada()
    return 0


def _ask(pregunta: questionary.Question) -> object:
    """Ctrl+C en questionary devuelve None: lo convertimos en cancelacion."""
    respuesta = pregunta.ask()
    if respuesta is None:
        raise OperacionCancelada()
    return respuesta


# ======================= TEXTO =======================
def pedir_texto(mensaje: str, opcional: bool = False) -> str | None:
    """No vacio. Con opcional=True, Enter devuelve None (= conservar valor)."""
    intentos = 0
    while True:
        valor = input(mensaje).strip()
        if valor:
            return valor
        if opcional:
            return None
        _error("El campo no puede estar vacio.")
        intentos = _manejar_max_intentos(intentos)


def pedir_validado(mensaje: str, validar: Callable[[str], object], opcional: bool = False) -> str | None:
    """Repite la pregunta mientras validar() lance FoodStoreError. Con opcional=True, Enter devuelve None."""
    intentos = 0
    while True:
        valor = pedir_texto(mensaje, opcional)
        if valor is None:
            return None
        try:
            validar(valor)
            return valor
        except FoodStoreError as e:
            _error(e.mensaje)
        intentos = _manejar_max_intentos(intentos)


def pedir_contrasenia(mensaje: str = "Contraseña: ") -> str:
    """Oculta lo que se escribe (getpass)."""
    intentos = 0
    while True:
        valor = getpass.getpass(mensaje).strip()
        if valor:
            return valor
        _error("La contraseña no puede estar vacia.")
        intentos = _manejar_max_intentos(intentos)


# ======================= NUMEROS =======================
def pedir_entero(mensaje: str, minimo: int = 0, opcional: bool = False) -> int | None:
    intentos = 0
    while True:
        dato = input(mensaje).strip()
        if not dato:
            if opcional:
                return None
            _error("El campo no puede estar vacio.")
        elif not dato.lstrip("-").isdigit():
            _error("Debe ingresar un numero entero.")
        elif int(dato) < minimo:
            _error(f"Debe ingresar un numero entero mayor o igual a {minimo}.")
        else:
            return int(dato)
        intentos = _manejar_max_intentos(intentos)


def pedir_decimal(mensaje: str, minimo: float = 0.0, opcional: bool = False) -> float | None:
    """Acepta coma o punto decimal (1500,50 o 1500.50)."""
    intentos = 0
    while True:
        dato = input(mensaje).strip().replace(",", ".")
        if not dato:
            if opcional:
                return None
            _error("El campo no puede estar vacio.")
        else:
            try:
                numero = float(dato)
            except ValueError:
                _error("Debe ingresar un numero valido.")
            else:
                if numero >= minimo:
                    return numero
                _error(f"Debe ingresar un numero mayor o igual a {formatear_numero(minimo)}.")
        intentos = _manejar_max_intentos(intentos)


def pedir_id(mensaje: str = "Ingrese el id: ") -> int:
    resultado = pedir_entero(mensaje, minimo=1)
    assert resultado is not None
    return resultado


# ======================= SELECCIONES =======================
def confirmar(mensaje: str) -> bool:
    respuesta = _ask(questionary.select(
        mensaje,
        choices=["✅ Si", "❌ No"],
        style=ESTILO_MENU,
    ))
    return respuesta == "✅ Si"


def pedir_si_no(mensaje: str, opcional: bool = False) -> bool | None:
    """Para campos booleanos (ej: disponible). Con opcional=True ofrece '(No modificar)' -> None."""
    opciones = ["✅ Si", "❌ No"]
    if opcional:
        opciones.insert(0, OPCION_NO_MODIFICAR)
    respuesta = _ask(questionary.select(mensaje, choices=opciones, style=ESTILO_MENU))
    if respuesta == OPCION_NO_MODIFICAR:
        return None
    return respuesta == "✅ Si"


def elegir_enum(mensaje: str, tipo: type[E], opcional: bool = False) -> E | None:
    """
    Opciones numeradas (1) Tarjeta, 2) ...). Se puede elegir con flechas o tocando el numero.
    Con opcional=True agrega '(No modificar)' -> None.
    """
    choices: list[questionary.Choice] = []
    if opcional:
        choices.append(questionary.Choice(OPCION_NO_MODIFICAR, value=OPCION_NO_MODIFICAR, shortcut_key="0"))
    for i, miembro in enumerate(tipo, start=1):
        choices.append(questionary.Choice(miembro.value, value=miembro, shortcut_key=str(i)))
    respuesta = _ask(questionary.select(mensaje, choices=choices, style=ESTILO_MENU, use_shortcuts=True))
    if respuesta == OPCION_NO_MODIFICAR:
        return None
    return respuesta  # type: ignore[return-value]
