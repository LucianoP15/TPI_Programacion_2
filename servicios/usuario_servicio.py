from entidades import Usuario
from enums import Rol
from excepciones import CredencialesInvalidasError, DuplicadoError, OperacionNoPermitidaError
from servicios.servicio_base import ServicioBase


class UsuarioServicio(ServicioBase[Usuario]):
    """Integrante A."""

    nombre_entidad = "Usuario"

    def autenticar(self, mail: str, contrasenia: str) -> Usuario:
        """Mismo error si el mail no existe, el usuario esta eliminado o la contrasenia no coincide."""
        usuario = self._buscar_por_mail(mail)
        if usuario is None or usuario.eliminado or not usuario.verificar_contrasenia(contrasenia):
            raise CredencialesInvalidasError()
        return usuario

    def crear(
        self,
        nombre: str,
        apellido: str,
        mail: str,
        celular: str,
        contrasenia: str,
        rol: Rol,
    ) -> Usuario:
        self.validar_mail_disponible(mail)
        return self.registrar(Usuario(nombre, apellido, mail, celular, contrasenia, rol))

    def editar(
        self,
        id_usuario: int,
        nombre: str | None = None,
        apellido: str | None = None,
        mail: str | None = None,
        celular: str | None = None,
        contrasenia: str | None = None,
        rol: Rol | None = None,
        usuario_sesion: Usuario | None = None,
    ) -> Usuario:
        """None = conservar el valor actual."""
        usuario = self.buscar_por_id(id_usuario)
        if rol is not None and rol != usuario.rol and usuario == usuario_sesion:
            raise OperacionNoPermitidaError("No puede cambiar su propio rol")
        if mail is not None:
            self.validar_mail_disponible(mail, excluir_id=usuario.id)

        # Si un dato falla, se restauran los anteriores: la edicion es todo o nada
        anterior = (usuario.mail, usuario.nombre, usuario.apellido, usuario.celular, usuario.rol)
        try:
            if mail is not None:
                usuario.mail = mail
            if nombre is not None:
                usuario.nombre = nombre
            if apellido is not None:
                usuario.apellido = apellido
            if celular is not None:
                usuario.celular = celular
            if rol is not None:
                usuario.rol = rol
            # La contrasenia no se puede leer para restaurarla: va al final, cuando el resto ya es valido
            if contrasenia is not None:
                usuario.contrasenia = contrasenia
        except Exception:
            usuario.mail, usuario.nombre, usuario.apellido, usuario.celular, usuario.rol = anterior
            raise
        return usuario

    def eliminar(self, id_usuario: int, usuario_sesion: Usuario) -> None:
        if id_usuario == usuario_sesion.id:
            raise OperacionNoPermitidaError("No puede eliminar su propio usuario")
        self.buscar_por_id(id_usuario).eliminar()

    def _buscar_por_mail(self, mail: str) -> Usuario | None:
        """Incluye eliminados: el mail queda reservado aunque el usuario se haya dado de baja."""
        buscado = mail.strip().lower()
        for usuario in self._items:
            if usuario.mail == buscado:
                return usuario
        return None

    def validar_mail_disponible(self, mail: str, excluir_id: int | None = None) -> None:
        """Formato valido y sin otro usuario (incluidos eliminados) que ya lo use."""
        Usuario.validar_formato_mail(mail)
        existente = self._buscar_por_mail(mail)
        if existente is not None and existente.id != excluir_id:
            raise DuplicadoError(f"Ya existe un usuario con el mail '{existente.mail}'")
