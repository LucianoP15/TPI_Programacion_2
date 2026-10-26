# Reparto de tareas – TPI Programación II (Food Store)

En el código, cada parte pendiente está marcada con **`TODO [A]`** o **`TODO [B]`** y lanza
`NotImplementedError`. Mientras algo no esté hecho, el programa igual corre: el menú muestra
"🚧 Funcionalidad pendiente" y vuelve. Para ver lo que falta:

```bash
grep -rn "TODO \[A\]" --include=*.py .     # Integrante A
grep -rn "TODO \[B\]" --include=*.py .     # Integrante B
```

## Criterio de la división

- **A = catálogo + acceso** (categorías, usuarios, login).
- **B = venta** (productos, pedidos, stock).
- Cada uno es dueño de **archivos distintos**, así no se pisan en Git.
- B tiene la lógica más pesada (pedidos/stock); A compensa con más historias de usuario, más validaciones de entidades y la mayor parte del informe.

## Integrante A — Categorías, Usuarios y Acceso (10 HU)

| Capa | Archivo | Qué completar |
|---|---|---|
| Entidades | `entidades/categoria.py` | Validaciones en setters de `nombre`, `descripcion` |
| Entidades | `entidades/usuario.py` | Validaciones de `nombre`, `apellido`, `mail` (formato), `contrasenia` |
| Servicios | `servicios/categoria_servicio.py` | `crear`, `editar`, `eliminar`, `_validar_nombre_unico` |
| Servicios | `servicios/usuario_servicio.py` | `autenticar`, `crear`, `editar`, `eliminar`, `_validar_mail_unico` |
| Consola | `consola/pantallas/categorias.py` | `listar`, `crear`, `editar`, `eliminar` |
| Consola | `consola/pantallas/usuarios.py` | `listar`, `crear`, `editar`, `eliminar`, `mis_datos` |
| Consola | `consola/login.py` | Borrar el bloque "modo desarrollo" cuando `autenticar()` funcione |
| Pruebas | `pruebas.py` secciones 1 y 2 | Casos válidos y de error |

**HU:** ACC-01, ACC-03 (verificar), CAT-01 a CAT-04, USR-01 a USR-05.
**Informe:** marco teórico completo + decisiones técnicas y arquitectura.

## Integrante B — Productos y Pedidos (9 HU, las más pesadas)

| Capa | Archivo | Qué completar |
|---|---|---|
| Entidades | `entidades/producto.py` | Validaciones de `nombre`, `precio`, `stock`, `categoria` |
| Entidades | `entidades/detalle_pedido.py` | Validación de `cantidad` |
| Entidades | `entidades/pedido.py` | `agregar_detalle`, `buscar_detalle_por_producto`, `eliminar_detalle_por_producto`, `calcular_total`, validación de usuario |
| Servicios | `servicios/producto_servicio.py` | `listar_disponibles`, `listar_por_categoria`, `crear`, `editar`, `eliminar` |
| Servicios | `servicios/pedido_servicio.py` | `crear`, `cambiar_estado`, `cambiar_forma_pago`, `eliminar`, `listar_por_usuario`, `buscar_de_usuario`, stock |
| Consola | `consola/pantallas/productos.py` | `listar`, `listar_disponibles`, `crear`, `editar`, `eliminar` |
| Consola | `consola/pantallas/pedidos.py` | `listar`, `ver_detalle`, `crear`, `actualizar`, `eliminar`, `mis_pedidos` |
| Pruebas | `pruebas.py` secciones 3 y 4 | Casos válidos y de error |

**HU:** PROD-01 a PROD-04, PED-01 a PED-05.
**Informe:** README final, capturas de pantalla y guion del video.

## Entre los dos

- Sección "Dificultades y soluciones" del informe (cada uno escribe la suya).
- Video de 10 a 15 min: A muestra el login con ambos roles + categorías/usuarios; B muestra productos, pedidos y **el pedido cancelado por falta de stock**. Los dos muestran al menos un error de validación.
- Revisar el código del otro antes de mergear (pull request).

## Ya resuelto en el esqueleto (no hace falta tocarlo)

| Archivo | Contenido |
|---|---|
| `main.py` | Arranque, verificación de dependencias, ciclo login → menú → cerrar sesión/salir |
| `datos_iniciales.py` | Admin `admin@foodstore.com / admin123`, cliente `juan@foodstore.com / cliente123`, categorías y productos de ejemplo |
| `entidades/base.py` | `Base` abstracta: id autoincremental, `eliminado`, `creado_en`, `eliminar()`, `__eq__`, `__hash__` |
| `entidades/calculable.py` | Interfaz `Calculable` |
| Entidades (resto) | Constructores, properties, `__str__`, relaciones sincronizadas (categoría ↔ productos, usuario ↔ pedidos) |
| `enums/`, `excepciones/` | `Rol`, `Estado`, `FormaPago` y todas las excepciones propias |
| `servicios/servicio_base.py` | `registrar`, `listar_activos`, `listar_todos`, `buscar_por_id` (lanza `EntidadNoEncontradaError`) |
| `servicios/pedido_servicio.py` | Diccionario `TRANSICIONES_VALIDAS` |
| `consola/menu.py` | `Menu` abstracta, `MenuAdministrador`, `MenuCliente`, `crear_menu()` (polimorfismo) y captura de errores |
| `consola/login.py` | Pantalla de login con 3 intentos |
| `consola/entrada.py` | `pedir_texto`, `pedir_entero`, `pedir_decimal`, `pedir_id`, `pedir_contrasenia`, `pedir_si_no`, `confirmar`, `elegir_enum` |
| `consola/estilos.py` | Títulos, mensajes y tablas `rich` para cada entidad |

## Patrón de una pantalla (ejemplo para seguir)

```python
def editar(servicios: Servicios, sesion: Usuario) -> None:
    mostrar_titulo("✍️  Editar categoria")
    mostrar_tabla_categorias(servicios.categorias.listar_activos())
    id_cat = pedir_id("Id de la categoria: ")
    categoria = servicios.categorias.buscar_por_id(id_cat)   # si no existe, lanza y el menu lo informa
    nombre = pedir_texto(f"Nombre [{categoria.nombre}]: ", opcional=True)        # Enter = conservar
    descripcion = pedir_texto(f"Descripcion [{categoria.descripcion}]: ", opcional=True)
    servicios.categorias.editar(id_cat, nombre, descripcion)
    mensaje_exito("Categoria actualizada.")
```

No hace falta `try/except` en las pantallas: `Menu._ejecutar()` ya captura `FoodStoreError`,
`ValueError` y la cancelación, muestra el mensaje y vuelve al menú.

## Flujo de Git sugerido

1. `main` siempre ejecutable.
2. Ramas por épica: `feat/categorias`, `feat/usuarios`, `feat/productos`, `feat/pedidos`.
3. Orden recomendado: **A** arranca por `autenticar()` (destraba el login real); **B** arranca por `Pedido.agregar_detalle()` y `calcular_total()` (es lo más evaluado).
