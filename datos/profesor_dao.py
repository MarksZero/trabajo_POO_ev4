#============================================
# datos/profesor_dao.py
# Data Access Object para la entidad Profesor
#============================================

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.profesor import Profesor


class ProfesorDAO:
    #============================================
    # Clase para operaciones CRUD de Profesor
    #============================================

    #============================================
    # Crea un nuevo profesor en la base de datos
    #============================================
    @staticmethod
    def crear(session: Session, rut: str, nombre: str, apellido: str, email: str):
        try:
            profesor = Profesor(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                email=email
            )
            session.add(profesor)
            session.commit()
            session.refresh(profesor)
            return profesor, None
        except IntegrityError as e:
            session.rollback()
            return None, f"Error: RUT o email ya existe"
        except Exception as e:
            session.rollback()
            return None, f"Error al crear profesor: {str(e)}"

    #============================================
    # Obtiene un profesor por su ID
    #============================================
    @staticmethod
    def obtener_por_id(session: Session, profesor_id: int):
        return session.query(Profesor).filter(
            Profesor.profesor_id == profesor_id
        ).first()

    #============================================
    # Obtiene un profesor por su RUT
    #============================================
    @staticmethod
    def obtener_por_rut(session: Session, rut: str):
        return session.query(Profesor).filter(
            Profesor.rut == rut
        ).first()

    #============================================
    # Obtiene todos los profesores
    #============================================
    @staticmethod
    def obtener_todos(session: Session, solo_activos: bool = True):
        query = session.query(Profesor)
        if solo_activos:
            query = query.filter(Profesor.estado == 'Activo')
        return query.all()

    #============================================
    # Actualiza los datos de un profesor
    #============================================
    @staticmethod
    def actualizar(session: Session, profesor_id: int, **kwargs):
        try:
            profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
            if not profesor:
                return None, "Profesor no encontrado"

            for key, value in kwargs.items():
                if hasattr(profesor, key):
                    setattr(profesor, key, value)

            session.commit()
            session.refresh(profesor)
            return profesor, None
        except Exception as e:
            session.rollback()
            return None, f"Error al actualizar: {str(e)}"

    #============================================
    # Elimina un profesor
    #============================================
    @staticmethod
    def eliminar(session: Session, profesor_id: int):
        try:
            profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
            if not profesor:
                return False, "Profesor no encontrado"

            session.delete(profesor)
            session.commit()
            return True, "Profesor eliminado exitosamente"
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"

    #============================================
    # Obtiene todos los cursos de un profesor
    #============================================
    @staticmethod
    def obtener_cursos_profesor(session: Session, profesor_id: int):
        profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
        if profesor:
            return profesor.cursos
        return []

    #============================================
    # Cuenta la cantidad de cursos activos de un profesor
    #============================================
    @staticmethod
    def contar_cursos(session: Session, profesor_id: int):
        from modelos.curso import Curso
        return session.query(Curso).filter(
            Curso.profesor_id == profesor_id,
            Curso.estado == 'Activo'
        ).count()
