#============================================
# datos/historial_dao.py
# Data Access Object para la entidad HistorialAcademico
#============================================

from sqlalchemy.orm import Session
from modelos.historial import HistorialAcademico
from decimal import Decimal


class HistorialDAO:
    #============================================
    # Clase para operaciones CRUD de HistorialAcademico
    #============================================

    #============================================
    # Crea un nuevo registro en el historial académico
    #============================================
    @staticmethod
    def crear(session: Session, estudiante_id: int, curso_id: int,
              semestre: str, nota: float, creditos: int):
        try:
            historial = HistorialAcademico(
                estudiante_id=estudiante_id,
                curso_id=curso_id,
                semestre=semestre,
                nota=Decimal(str(nota)),
                creditos=creditos
            )
            session.add(historial)
            session.commit()
            session.refresh(historial)
            return historial, None
        except Exception as e:
            session.rollback()
            return None, f"Error al crear historial: {str(e)}"

    #============================================
    # Obtiene un registro del historial por su ID
    #============================================
    @staticmethod
    def obtener_por_id(session: Session, historial_id: int):
        return session.query(HistorialAcademico).filter(
            HistorialAcademico.historial_id == historial_id
        ).first()

    #============================================
    # Obtiene todo el historial académico de un estudiante
    #============================================
    @staticmethod
    def obtener_por_estudiante(session: Session, estudiante_id: int):
        return session.query(HistorialAcademico).filter(
            HistorialAcademico.estudiante_id == estudiante_id
        ).order_by(HistorialAcademico.semestre).all()

    #============================================
    # Obtiene el historial de un curso (todos los estudiantes)
    #============================================
    @staticmethod
    def obtener_por_curso(session: Session, curso_id: int):
        return session.query(HistorialAcademico).filter(
            HistorialAcademico.curso_id == curso_id
        ).all()

    #============================================
    # Obtiene el historial de un estudiante en un semestre específico
    #============================================
    @staticmethod
    def obtener_por_semestre(session: Session, estudiante_id: int, semestre: str):
        return session.query(HistorialAcademico).filter(
            HistorialAcademico.estudiante_id == estudiante_id,
            HistorialAcademico.semestre == semestre
        ).all()

    #============================================
    # Actualiza la nota de un registro del historial
    #============================================
    @staticmethod
    def actualizar_nota(session: Session, historial_id: int, nueva_nota: float):
        try:
            historial = HistorialDAO.obtener_por_id(session, historial_id)
            if not historial:
                return None, "Registro no encontrado"

            historial.nota = Decimal(str(nueva_nota))
            session.commit()
            session.refresh(historial)
            return historial, None
        except Exception as e:
            session.rollback()
            return None, f"Error al actualizar: {str(e)}"

    #============================================
    # Elimina un registro del historial
    #============================================
    @staticmethod
    def eliminar(session: Session, historial_id: int):
        try:
            historial = HistorialDAO.obtener_por_id(session, historial_id)
            if not historial:
                return False, "Registro no encontrado"

            session.delete(historial)
            session.commit()
            return True, "Registro eliminado exitosamente"
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"

    #============================================
    # Calcula el promedio ponderado de un estudiante
    #============================================
    @staticmethod
    def calcular_promedio(session: Session, estudiante_id: int):
        from sqlalchemy import func

        result = session.query(
            func.sum(HistorialAcademico.nota * HistorialAcademico.creditos).label('suma_ponderada'),
            func.sum(HistorialAcademico.creditos).label('total_creditos')
        ).filter(
            HistorialAcademico.estudiante_id == estudiante_id
        ).first()

        if result.total_creditos and result.total_creditos > 0:
            promedio = float(result.suma_ponderada) / float(result.total_creditos)
            return round(promedio, 2)
        return 0.0

    #============================================
    # Calcula el promedio de un estudiante en un semestre específico
    #============================================
    @staticmethod
    def calcular_promedio_semestre(session: Session, estudiante_id: int, semestre: str):
        from sqlalchemy import func

        result = session.query(
            func.sum(HistorialAcademico.nota * HistorialAcademico.creditos).label('suma_ponderada'),
            func.sum(HistorialAcademico.creditos).label('total_creditos')
        ).filter(
            HistorialAcademico.estudiante_id == estudiante_id,
            HistorialAcademico.semestre == semestre
        ).first()

        if result.total_creditos and result.total_creditos > 0:
            promedio = float(result.suma_ponderada) / float(result.total_creditos)
            return round(promedio, 2)
        return 0.0

    #============================================
    # Cuenta los créditos aprobados de un estudiante (nota >= 4.0)
    #============================================
    @staticmethod
    def contar_creditos_aprobados(session: Session, estudiante_id: int):
        from sqlalchemy import func

        result = session.query(
            func.sum(HistorialAcademico.creditos)
        ).filter(
            HistorialAcademico.estudiante_id == estudiante_id,
            HistorialAcademico.nota >= 4.0
        ).scalar()

        return result if result else 0
