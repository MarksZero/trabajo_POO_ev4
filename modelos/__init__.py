#============================================
# modelos/__init__.py
# Módulo de modelos de dominio (entidades ORM)
#============================================

from .estudiante import Estudiante
from .profesor import Profesor
from .curso import Curso
from .matricula import Matricula
from .historial import HistorialAcademico

__all__ = ['Estudiante', 'Profesor', 'Curso', 'Matricula', 'HistorialAcademico']
