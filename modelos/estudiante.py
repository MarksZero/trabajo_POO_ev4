# ============================================
# modelos/estudiante.py
# Modelo de dominio para la entidad Estudiante
# ============================================

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from datos.conexion import Base


class Estudiante(Base):
    __tablename__ = 'Estudiante'

    # ============================================
    # Columnas
    # ============================================
    estudiante_id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(10), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    carrera = Column(String(150), nullable=False)
    creditos_maximos = Column(Integer, default=20)
    estado = Column(
        Enum('Activo', 'Inactivo', 'Egresado', name='estado_estudiante'),
        default='Activo'
    )

    # ============================================
    # Relaciones
    # ============================================
    matriculas = relationship(
        'Matricula',
        back_populates='estudiante',
        cascade='all, delete-orphan'
    )

    historiales = relationship(
        'HistorialAcademico',
        back_populates='estudiante',
        cascade='all, delete-orphan'
    )

    # ============================================
    # Representación del objeto
    # ============================================
    def __repr__(self):
        return f"<Estudiante(id={self.estudiante_id}, rut='{self.rut}', nombre='{self.nombre} {self.apellido}')>"

    # ============================================
    # Convierte el objeto a diccionario
    # ============================================
    def to_dict(self):
        return {
            'estudiante_id': self.estudiante_id,
            'rut': self.rut,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'carrera': self.carrera,
            'creditos_maximos': self.creditos_maximos,
            'estado': self.estado
        }

    # ============================================
    # Retorna el nombre completo
    # ============================================
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
