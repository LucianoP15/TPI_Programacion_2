from entidades import Usuario
from enums import Rol
from servicios.servicio_base import ServicioBase


class UsuarioServicio(ServicioBase[Usuario]):
    """Integrante A."""

    nombre_entidad = "Usuario"

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        # TODO [A] HU-ACC-01
        #  - buscar el usuario por mail (sin distinguir mayusculas)
        #  - si no existe, esta eliminado o verificar_contrasenia() da False
        #    -> raise CredencialesInvalidasError()  (mismo mensaje en los 3 casos)
        #  - devolver el usuario
        raise NotImplementedError("UsuarioServicio.autenticar")

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        # TODO [A] HU-USR-02: validar mail unico, crear, registrar y devolver
        raise NotImplementedError("UsuarioServicio.crear")

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
    ) -> Usuario:
        # TODO [A] HU-USR-03: None = conservar. Si cambia el mail, validar unicidad excluyendo al propio usuario
        raise NotImplementedError("UsuarioServicio.editar")

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        # TODO [A] HU-USR-04
        #  - si id_usuario == usuario_sesion.id -> OperacionNoPermitidaError
        #  - si no: usuario.eliminar()
        raise NotImplementedError("UsuarioServicio.eliminar")

    def _validar_mail_unico(self, mail: str, excluir_id: int | None = None) -> None:
        # TODO [A] recorrer la coleccion; si el mail ya existe -> DuplicadoError
        raise NotImplementedError("UsuarioServicio._validar_mail_unico")
