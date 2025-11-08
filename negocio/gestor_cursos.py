#============================================
# negocio/gestor_cursos.py
# Gestor de lógica de negocio para Cursos
#============================================

from sqlalchemy.orm import Session
from datos.curso_dao import CursoDAO
from datos.profesor_dao import ProfesorDAO
from auxiliares.validadores import Validadores
from auxiliares.formateadores import Formateadores
from auxiliares.constantes import Constantes


class GestorCursos:
    # Clase que implementa la lógica de negocio para cursos

    @staticmethod
    def crear_curso(session: Session, codigo: str, nombre: str, creditos: int,
                   profesor_id: int = None, capacidad_maxima: int = None, semestre: str = None):
        # Crea un curso con validaciones de negocio

        # Validar código
        valido, mensaje = Validadores.validar_texto_no_vacio(codigo, "Código")
        if not valido:
            return None, mensaje

        # Validar nombre
        valido, mensaje = Validadores.validar_texto_no_vacio(nombre, "Nombre")
        if not valido:
            return None, mensaje

        # Validar créditos
        valido, mensaje = Validadores.validar_creditos(creditos)
        if not valido:
            return None, mensaje

        # Validar semestre si se proporciona
        if semestre:
            valido, mensaje = Validadores.validar_semestre(semestre)
            if not valido:
                return None, mensaje

        # Establecer capacidad por defecto
        if capacidad_maxima is None:
            capacidad_maxima = Constantes.CAPACIDAD_CURSO_DEFAULT
        else:
            valido, mensaje = Validadores.validar_numero_positivo(capacidad_maxima, "Capacidad máxima")
            if not valido:
                return None, mensaje

        # Validar profesor si se proporciona
        if profesor_id:
            profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
            if not profesor:
                return None, "Profesor no encontrado"

            # Verificar carga académica del profesor
            cantidad_cursos = ProfesorDAO.contar_cursos(session, profesor_id)
            if cantidad_cursos >= Constantes.MAX_CURSOS_PROFESOR:
                return None, f"El profesor ya tiene {Constantes.MAX_CURSOS_PROFESOR} cursos asignados"

        # Formatear código en mayúsculas
        codigo = codigo.upper()

        # Crear en la base de datos
        return CursoDAO.crear(
            session, codigo, nombre, creditos, profesor_id, capacidad_maxima, semestre
        )

    @staticmethod
    def obtener_curso(session: Session, curso_id: int):
        # Obtiene un curso por ID
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return None, "Curso no encontrado"
        return curso, None

    @staticmethod
    def listar_cursos(session: Session, solo_activos: bool = True):
        # Lista todos los cursos
        return CursoDAO.obtener_todos(session, solo_activos)

    @staticmethod
    def listar_por_profesor(session: Session, profesor_id: int):
        # Lista cursos por profesor
        return CursoDAO.obtener_por_profesor(session, profesor_id)

    @staticmethod
    def listar_por_semestre(session: Session, semestre: str):
        # Lista cursos por semestre
        valido, mensaje = Validadores.validar_semestre(semestre)
        if not valido:
            return None, mensaje

        return CursoDAO.obtener_por_semestre(session, semestre), None

    @staticmethod
    def asignar_profesor(session: Session, curso_id: int, profesor_id: int):
        # Asigna un profesor a un curso con validaciones

        # Validar que el curso exista
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return None, "Curso no encontrado"

        # Validar que el profesor exista
        profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
        if not profesor:
            return None, "Profesor no encontrado"

        # Verificar carga académica del profesor
        cantidad_cursos = ProfesorDAO.contar_cursos(session, profesor_id)
        if cantidad_cursos >= Constantes.MAX_CURSOS_PROFESOR:
            return None, f"El profesor ya tiene {Constantes.MAX_CURSOS_PROFESOR} cursos asignados"

        return CursoDAO.asignar_profesor(session, curso_id, profesor_id)

    @staticmethod
    def actualizar_curso(session: Session, curso_id: int, **kwargs):
        # Actualiza un curso con validaciones

        # Validar créditos si se proporcionan
        if 'creditos' in kwargs:
            valido, mensaje = Validadores.validar_creditos(kwargs['creditos'])
            if not valido:
                return None, mensaje

        # Validar semestre si se proporciona
        if 'semestre' in kwargs and kwargs['semestre']:
            valido, mensaje = Validadores.validar_semestre(kwargs['semestre'])
            if not valido:
                return None, mensaje

        # Formatear código en mayúsculas si se proporciona
        if 'codigo' in kwargs:
            kwargs['codigo'] = kwargs['codigo'].upper()

        return CursoDAO.actualizar(session, curso_id, **kwargs)

    @staticmethod
    def eliminar_curso(session: Session, curso_id: int):
        # Elimina un curso

        # Verificar que no tenga estudiantes inscritos
        cantidad_estudiantes = CursoDAO.contar_estudiantes_inscritos(session, curso_id)
        if cantidad_estudiantes > 0:
            return False, f"El curso tiene {cantidad_estudiantes} estudiante(s) inscrito(s). No se puede eliminar."

        return CursoDAO.eliminar(session, curso_id)

    @staticmethod
    def obtener_estudiantes_curso(session: Session, curso_id: int):
        # Obtiene todos los estudiantes inscritos en un curso
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return None, "Curso no encontrado"

        return CursoDAO.obtener_estudiantes_curso(session, curso_id), None

    @staticmethod
    def verificar_disponibilidad(session: Session, curso_id: int):
        # Verifica si el curso tiene cupos disponibles
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return False, "Curso no encontrado"

        inscritos = CursoDAO.contar_estudiantes_inscritos(session, curso_id)
        disponibles = curso.capacidad_maxima - inscritos

        if disponibles <= 0:
            return False, "El curso no tiene cupos disponibles"

        return True, f"Cupos disponibles: {disponibles}/{curso.capacidad_maxima}"
