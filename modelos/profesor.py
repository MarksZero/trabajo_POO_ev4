# ============================================
# modelos/profesor.py
# Modelo de dominio para la entidad Profesor
# ============================================

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from datos.conexion import Base


class Profesor(Base):
    __tablename__ = 'Profesor'

    # ============================================
    # Columnas
    # ============================================
    profesor_id = Column(Integer, primary_key=True, autoincrement=True)
    rut = Column(String(12), unique=True, nullable=False)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    estado = Column(
        Enum('Activo', 'Inactivo', name='estado_profesor'),
        default='Activo'
    )

    # ============================================
    # Relaciones
    # ============================================
    cursos = relationship(
        'Curso',
        back_populates='profesor'
    )

    # ============================================
    # Representación del objeto
    # ============================================
    def __repr__(self):
        return f"<Profesor(id={self.profesor_id}, rut='{self.rut}', nombre='{self.nombre} {self.apellido}')>"

    # ============================================
    # Convierte el objeto a diccionario
    # ============================================
    def to_dict(self):
        return {
            'profesor_id': self.profesor_id,
            'rut': self.rut,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'email': self.email,
            'estado': self.estado
        }

    # ============================================
    # Retorna el nombre completo
    # ============================================
    def nombre_completo(self):
        return f"{self.nombre} {self.apellido}"
