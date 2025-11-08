#============================================
# negocio/gestor_profesores.py
# Gestor de lógica de negocio para Profesores
#============================================

from sqlalchemy.orm import Session
from datos.profesor_dao import ProfesorDAO
from auxiliares.validadores import Validadores
from auxiliares.formateadores import Formateadores
from auxiliares.constantes import Constantes


class GestorProfesores:
    # Clase que implementa la lógica de negocio para profesores

    @staticmethod
    def crear_profesor(session: Session, rut: str, nombre: str, apellido: str, email: str):
        # Crea un profesor con validaciones de negocio

        # Validar RUT
        valido, mensaje = Validadores.validar_rut(rut)
        if not valido:
            return None, mensaje

        # Validar email
        valido, mensaje = Validadores.validar_email(email)
        if not valido:
            return None, mensaje

        # Validar nombre
        valido, mensaje = Validadores.validar_texto_no_vacio(nombre, "Nombre")
        if not valido:
            return None, mensaje

        # Validar apellido
        valido, mensaje = Validadores.validar_texto_no_vacio(apellido, "Apellido")
        if not valido:
            return None, mensaje

        # Formatear datos
        nombre = Formateadores.capitalizar_nombre(nombre)
        apellido = Formateadores.capitalizar_nombre(apellido)

        # Crear en la base de datos
        return ProfesorDAO.crear(session, rut, nombre, apellido, email)

    @staticmethod
    def obtener_profesor(session: Session, profesor_id: int):
        # Obtiene un profesor por ID
        profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
        if not profesor:
            return None, "Profesor no encontrado"
        return profesor, None

    @staticmethod
    def listar_profesores(session: Session, solo_activos: bool = True):
        # Lista todos los profesores
        return ProfesorDAO.obtener_todos(session, solo_activos)

    @staticmethod
    def actualizar_profesor(session: Session, profesor_id: int, **kwargs):
        # Actualiza un profesor con validaciones

        # Validar email si se proporciona
        if 'email' in kwargs:
            valido, mensaje = Validadores.validar_email(kwargs['email'])
            if not valido:
                return None, mensaje

        # Formatear nombre y apellido si se proporcionan
        if 'nombre' in kwargs:
            kwargs['nombre'] = Formateadores.capitalizar_nombre(kwargs['nombre'])
        if 'apellido' in kwargs:
            kwargs['apellido'] = Formateadores.capitalizar_nombre(kwargs['apellido'])

        return ProfesorDAO.actualizar(session, profesor_id, **kwargs)

    @staticmethod
    def eliminar_profesor(session: Session, profesor_id: int):
        # Elimina un profesor

        # Verificar que no tenga cursos asignados
        cantidad_cursos = ProfesorDAO.contar_cursos(session, profesor_id)
        if cantidad_cursos > 0:
            return False, f"El profesor tiene {cantidad_cursos} curso(s) asignado(s). No se puede eliminar."

        return ProfesorDAO.eliminar(session, profesor_id)

    @staticmethod
    def obtener_cursos_profesor(session: Session, profesor_id: int):
        # Obtiene todos los cursos de un profesor
        profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
        if not profesor:
            return None, "Profesor no encontrado"

        return ProfesorDAO.obtener_cursos_profesor(session, profesor_id), None

    @staticmethod
    def validar_carga_academica(session: Session, profesor_id: int):
        # Valida que el profesor no exceda el máximo de cursos permitidos
        cantidad_cursos = ProfesorDAO.contar_cursos(session, profesor_id)

        if cantidad_cursos >= Constantes.MAX_CURSOS_PROFESOR:
            return False, f"El profesor ya tiene {cantidad_cursos} curso(s). Máximo permitido: {Constantes.MAX_CURSOS_PROFESOR}"

        return True, f"El profesor puede aceptar más cursos ({cantidad_cursos}/{Constantes.MAX_CURSOS_PROFESOR})"
