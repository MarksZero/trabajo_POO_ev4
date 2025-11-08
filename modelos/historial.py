# ============================================
# modelos/historial.py
# Modelo de dominio para la entidad HistorialAcademico
# ============================================

from sqlalchemy import Column, Integer, String, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datos.conexion import Base


class HistorialAcademico(Base):
    __tablename__ = 'HistorialAcademico'

    # ============================================
    # Columnas
    # ============================================
    historial_id = Column(Integer, primary_key=True, autoincrement=True)
    estudiante_id = Column(
        Integer,
        ForeignKey('Estudiante.estudiante_id', ondelete='CASCADE'),
        nullable=False
    )
    curso_id = Column(
        Integer,
        ForeignKey('Curso.curso_id', ondelete='CASCADE'),
        nullable=False
    )
    semestre = Column(String(10), nullable=False)
    nota = Column(DECIMAL(3, 2))
    creditos = Column(Integer, nullable=False)

    # ============================================
    # Relaciones
    # ============================================
    estudiante = relationship('Estudiante', back_populates='historiales')
    curso = relationship('Curso', back_populates='historiales')

    # ============================================
    # Representación del objeto
    # ============================================
    def __repr__(self):
        return (f"<HistorialAcademico(id={self.historial_id}, "
                f"estudiante_id={self.estudiante_id}, "
                f"curso_id={self.curso_id}, "
                f"nota={self.nota})>")

    # ============================================
    # Convierte el objeto a diccionario
    # ============================================
    def to_dict(self):
        return {
            'historial_id': self.historial_id,
            'estudiante_id': self.estudiante_id,
            'curso_id': self.curso_id,
            'semestre': self.semestre,
            'nota': float(self.nota) if self.nota else None,
            'creditos': self.creditos
        }
