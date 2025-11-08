#============================================
# datos/__init__.py
# Módulo de acceso a datos (Data Access Layer)
#============================================

from .conexion import engine, SessionLocal, Base, get_session, init_db
from .estudiante_dao import EstudianteDAO
from .profesor_dao import ProfesorDAO
from .curso_dao import CursoDAO
from .matricula_dao import MatriculaDAO
from .historial_dao import HistorialDAO

__all__ = [
    'engine', 'SessionLocal', 'Base', 'get_session', 'init_db',
    'EstudianteDAO', 'ProfesorDAO', 'CursoDAO', 'MatriculaDAO', 'HistorialDAO'
]
