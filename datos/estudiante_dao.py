# ============================================
# datos/estudiante_dao.py
# Data Access Object (DAO) para la entidad Estudiante
# ============================================

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.estudiante import Estudiante


# --------------------------------------------
# Clase DAO: Acceso y manipulación de datos
# --------------------------------------------
class EstudianteDAO:
    """Operaciones CRUD para la entidad Estudiante"""

    # ----------------------------------------
    # Crear un nuevo estudiante
    # ----------------------------------------
    @staticmethod
    def crear(session: Session, rut: str, nombre: str, apellido: str,
              email: str, carrera: str, creditos_maximos: int = 20):
        """Inserta un nuevo estudiante en la base de datos"""
        try:
            estudiante = Estudiante(
                rut=rut,
                nombre=nombre,
                apellido=apellido,
                email=email,
                carrera=carrera,
                creditos_maximos=creditos_maximos
            )
            session.add(estudiante)
            session.commit()
            session.refresh(estudiante)
            return estudiante, None
        except IntegrityError:
            session.rollback()
            return None, "Error: RUT o email ya existe"
        except Exception as e:
            session.rollback()
            return None, f"Error al crear estudiante: {str(e)}"

    # ----------------------------------------
    # Obtener estudiante por ID
    # ----------------------------------------
    @staticmethod
    def obtener_por_id(session: Session, estudiante_id: int):
        """Retorna un estudiante según su ID"""
        return session.query(Estudiante).filter(
            Estudiante.estudiante_id == estudiante_id
        ).first()

    # ----------------------------------------
    # Obtener estudiante por RUT
    # ----------------------------------------
    @staticmethod
    def obtener_por_rut(session: Session, rut: str):
        """Retorna un estudiante según su RUT"""
        return session.query(Estudiante).filter(
            Estudiante.rut == rut
        ).first()

    # ----------------------------------------
    # Listar todos los estudiantes
    # ----------------------------------------
    @staticmethod
    def obtener_todos(session: Session, solo_activos: bool = True):
        """Obtiene todos los estudiantes (opcionalmente solo activos)"""
        query = session.query(Estudiante)
        if solo_activos:
            query = query.filter(Estudiante.estado == 'Activo')
        return query.all()

    # ----------------------------------------
    # Listar estudiantes por carrera
    # ----------------------------------------
    @staticmethod
    def obtener_por_carrera(session: Session, carrera: str):
        """Retorna estudiantes activos filtrados por carrera"""
        return session.query(Estudiante).filter(
            Estudiante.carrera == carrera,
            Estudiante.estado == 'Activo'
        ).all()

    # ----------------------------------------
    # Actualizar información del estudiante
    # ----------------------------------------
    @staticmethod
    def actualizar(session: Session, estudiante_id: int, **kwargs):
        """Actualiza los datos de un estudiante existente"""
        try:
            estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
            if not estudiante:
                return None, "Estudiante no encontrado"

            for key, value in kwargs.items():
                if hasattr(estudiante, key):
                    setattr(estudiante, key, value)

            session.commit()
            session.refresh(estudiante)
            return estudiante, None
        except Exception as e:
            session.rollback()
            return None, f"Error al actualizar: {str(e)}"

    # ----------------------------------------
    # Eliminar estudiante
    # ----------------------------------------
    @staticmethod
    def eliminar(session: Session, estudiante_id: int):
        """Elimina un estudiante de la base de datos"""
        try:
            estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
            if not estudiante:
                return False, "Estudiante no encontrado"

            session.delete(estudiante)
            session.commit()
            return True, "Estudiante eliminado exitosamente"
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"

    # ----------------------------------------
    # Cambiar estado del estudiante
    # ----------------------------------------
    @staticmethod
    def cambiar_estado(session: Session, estudiante_id: int, nuevo_estado: str):
        """Cambia el estado (Activo, Inactivo, Egresado) de un estudiante"""
        return EstudianteDAO.actualizar(
            session, estudiante_id, estado=nuevo_estado
        )

    # ----------------------------------------
    # Contar estudiantes por carrera
    # ----------------------------------------
    @staticmethod
    def contar_por_carrera(session: Session):
        """Devuelve la cantidad de estudiantes activos agrupados por carrera"""
        from sqlalchemy import func
        return session.query(
            Estudiante.carrera,
            func.count(Estudiante.estudiante_id).label('cantidad')
        ).filter(
            Estudiante.estado == 'Activo'
        ).group_by(Estudiante.carrera).all()
