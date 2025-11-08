# ============================================
# modelos/matricula.py
# Modelo de dominio para la entidad Matricula
# ============================================

from sqlalchemy import Column, Integer, Enum, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from datos.conexion import Base


class Matricula(Base):
    __tablename__ = 'Matricula'

    # ============================================
    # Columnas
    # ============================================
    matricula_id = Column(Integer, primary_key=True, autoincrement=True)
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
    estado = Column(
        Enum('Inscrito', 'Retirado', 'Aprobado', 'Reprobado', name='estado_matricula'),
        default='Inscrito'
    )

    # ============================================
    # Constraint de unicidad
    # ============================================
    __table_args__ = (
        UniqueConstraint('estudiante_id', 'curso_id', name='unique_matricula'),
    )

    # ============================================
    # Relaciones
    # ============================================
    estudiante = relationship('Estudiante', back_populates='matriculas')
    curso = relationship('Curso', back_populates='matriculas')

    # ============================================
    # Representación del objeto
    # ============================================
    def __repr__(self):
        return (f"<Matricula(id={self.matricula_id}, "
                f"estudiante_id={self.estudiante_id}, "
                f"curso_id={self.curso_id}, "
                f"estado='{self.estado}')>")

    # ============================================
    # Convierte el objeto a diccionario
    # ============================================
    def to_dict(self):
        return {
            'matricula_id': self.matricula_id,
            'estudiante_id': self.estudiante_id,
            'curso_id': self.curso_id,
            'estado': self.estado
        }
