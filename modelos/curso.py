# ============================================
# modelos/curso.py
# Modelo de dominio para la entidad Curso
# ============================================

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship
from datos.conexion import Base


class Curso(Base):
    __tablename__ = 'Curso'

    # ============================================
    # Columnas
    # ============================================
    curso_id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(200), nullable=False)
    creditos = Column(Integer, nullable=False)
    profesor_id = Column(Integer, ForeignKey('Profesor.profesor_id', ondelete='SET NULL'))
    capacidad_maxima = Column(Integer, default=40)
    semestre = Column(String(10))
    estado = Column(
        Enum('Activo', 'Inactivo', name='estado_curso'),
        default='Activo'
    )

    # ============================================
    # Relaciones
    # ============================================
    profesor = relationship('Profesor', back_populates='cursos')

    matriculas = relationship(
        'Matricula',
        back_populates='curso',
        cascade='all, delete-orphan'
    )

    historiales = relationship(
        'HistorialAcademico',
        back_populates='curso',
        cascade='all, delete-orphan'
    )

    # ============================================
    # Representación del objeto
    # ============================================
    def __repr__(self):
        return f"<Curso(id={self.curso_id}, codigo='{self.codigo}', nombre='{self.nombre}')>"

    # ============================================
    # Convierte el objeto a diccionario
    # ============================================
    def to_dict(self):
        return {
            'curso_id': self.curso_id,
            'codigo': self.codigo,
            'nombre': self.nombre,
            'creditos': self.creditos,
            'profesor_id': self.profesor_id,
            'capacidad_maxima': self.capacidad_maxima,
            'semestre': self.semestre,
            'estado': self.estado
        }
