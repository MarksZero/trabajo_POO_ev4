#============================================
# datos/matricula_dao.py
# Data Access Object para la entidad Matricula
#============================================

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.matricula import Matricula


class MatriculaDAO:
    #============================================
    # Clase para operaciones CRUD de Matricula
    #============================================

    #============================================
    # Crea una nueva matrícula en la base de datos
    #============================================
    @staticmethod
    def crear(session: Session, estudiante_id: int, curso_id: int):
        try:
            matricula = Matricula(
                estudiante_id=estudiante_id,
                curso_id=curso_id,
                estado='Inscrito'
            )
            session.add(matricula)
            session.commit()
            session.refresh(matricula)
            return matricula, None
        except IntegrityError:
            session.rollback()
            return None, "El estudiante ya está inscrito en este curso"
        except Exception as e:
            session.rollback()
            return None, f"Error al crear matrícula: {str(e)}"

    #============================================
    # Obtiene una matrícula por su ID
    #============================================
    @staticmethod
    def obtener_por_id(session: Session, matricula_id: int):
        return session.query(Matricula).filter(
            Matricula.matricula_id == matricula_id
        ).first()

    #============================================
    # Obtiene una matrícula específica de estudiante y curso
    #============================================
    @staticmethod
    def obtener_matricula(session: Session, estudiante_id: int, curso_id: int):
        return session.query(Matricula).filter(
            Matricula.estudiante_id == estudiante_id,
            Matricula.curso_id == curso_id
        ).first()

    #============================================
    # Obtiene todas las matrículas de un estudiante
    #============================================
    @staticmethod
    def obtener_por_estudiante(session: Session, estudiante_id: int, solo_inscritos: bool = True):
        query = session.query(Matricula).filter(
            Matricula.estudiante_id == estudiante_id
        )
        if solo_inscritos:
            query = query.filter(Matricula.estado == 'Inscrito')
        return query.all()

    #============================================
    # Obtiene todas las matrículas de un curso
    #============================================
    @staticmethod
    def obtener_por_curso(session: Session, curso_id: int, solo_inscritos: bool = True):
        query = session.query(Matricula).filter(
            Matricula.curso_id == curso_id
        )
        if solo_inscritos:
            query = query.filter(Matricula.estado == 'Inscrito')
        return query.all()

    #============================================
    # Actualiza el estado de una matrícula
    #============================================
    @staticmethod
    def actualizar_estado(session: Session, matricula_id: int, nuevo_estado: str):
        try:
            matricula = MatriculaDAO.obtener_por_id(session, matricula_id)
            if not matricula:
                return None, "Matrícula no encontrada"

            matricula.estado = nuevo_estado
            session.commit()
            session.refresh(matricula)
            return matricula, None
        except Exception as e:
            session.rollback()
            return None, f"Error al actualizar: {str(e)}"

    #============================================
    # Elimina una matrícula
    #============================================
    @staticmethod
    def eliminar(session: Session, matricula_id: int):
        try:
            matricula = MatriculaDAO.obtener_por_id(session, matricula_id)
            if not matricula:
                return False, "Matrícula no encontrada"

            session.delete(matricula)
            session.commit()
            return True, "Matrícula eliminada exitosamente"
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"

    #============================================
    # Retira a un estudiante de un curso
    #============================================
    @staticmethod
    def retirar_curso(session: Session, estudiante_id: int, curso_id: int):
        matricula = MatriculaDAO.obtener_matricula(session, estudiante_id, curso_id)
        if matricula:
            return MatriculaDAO.actualizar_estado(
                session, matricula.matricula_id, 'Retirado'
            )
        return None, "Matrícula no encontrada"

    #============================================
    # Calcula los créditos totales inscritos de un estudiante
    #============================================
    @staticmethod
    def calcular_creditos_estudiante(session: Session, estudiante_id: int):
        from modelos.curso import Curso
        from sqlalchemy import func

        result = session.query(
            func.sum(Curso.creditos)
        ).join(
            Matricula, Curso.curso_id == Matricula.curso_id
        ).filter(
            Matricula.estudiante_id == estudiante_id,
            Matricula.estado == 'Inscrito'
        ).scalar()

        return result if result else 0
