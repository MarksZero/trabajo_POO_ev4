#============================================
# datos/curso_dao.py
# Data Access Object para la entidad Curso
#============================================

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from modelos.curso import Curso


class CursoDAO:
    #============================================
    # Clase para operaciones CRUD de Curso
    #============================================

    #============================================
    # Crea un nuevo curso en la base de datos
    #============================================
    @staticmethod
    def crear(session: Session, codigo: str, nombre: str, creditos: int,
              profesor_id: int = None, capacidad_maxima: int = 40, semestre: str = None):
        try:
            curso = Curso(
                codigo=codigo,
                nombre=nombre,
                creditos=creditos,
                profesor_id=profesor_id,
                capacidad_maxima=capacidad_maxima,
                semestre=semestre
            )
            session.add(curso)
            session.commit()
            session.refresh(curso)
            return curso, None
        except IntegrityError as e:
            session.rollback()
            return None, f"Error: Código de curso ya existe"
        except Exception as e:
            session.rollback()
            return None, f"Error al crear curso: {str(e)}"

    #============================================
    # Obtiene un curso por su ID
    #============================================
    @staticmethod
    def obtener_por_id(session: Session, curso_id: int):
        return session.query(Curso).filter(
            Curso.curso_id == curso_id
        ).first()

    #============================================
    # Obtiene un curso por su código
    #============================================
    @staticmethod
    def obtener_por_codigo(session: Session, codigo: str):
        return session.query(Curso).filter(
            Curso.codigo == codigo
        ).first()

    #============================================
    # Obtiene todos los cursos
    #============================================
    @staticmethod
    def obtener_todos(session: Session, solo_activos: bool = True):
        query = session.query(Curso)
        if solo_activos:
            query = query.filter(Curso.estado == 'Activo')
        return query.all()

    #============================================
    # Obtiene cursos por profesor
    #============================================
    @staticmethod
    def obtener_por_profesor(session: Session, profesor_id: int):
        return session.query(Curso).filter(
            Curso.profesor_id == profesor_id,
            Curso.estado == 'Activo'
        ).all()

    #============================================
    # Obtiene cursos por semestre
    #============================================
    @staticmethod
    def obtener_por_semestre(session: Session, semestre: str):
        return session.query(Curso).filter(
            Curso.semestre == semestre,
            Curso.estado == 'Activo'
        ).all()

    #============================================
    # Actualiza los datos de un curso
    #============================================
    @staticmethod
    def actualizar(session: Session, curso_id: int, **kwargs):
        try:
            curso = CursoDAO.obtener_por_id(session, curso_id)
            if not curso:
                return None, "Curso no encontrado"

            for key, value in kwargs.items():
                if hasattr(curso, key):
                    setattr(curso, key, value)

            session.commit()
            session.refresh(curso)
            return curso, None
        except Exception as e:
            session.rollback()
            return None, f"Error al actualizar: {str(e)}"

    #============================================
    # Elimina un curso
    #============================================
    @staticmethod
    def eliminar(session: Session, curso_id: int):
        try:
            curso = CursoDAO.obtener_por_id(session, curso_id)
            if not curso:
                return False, "Curso no encontrado"

            session.delete(curso)
            session.commit()
            return True, "Curso eliminado exitosamente"
        except Exception as e:
            session.rollback()
            return False, f"Error al eliminar: {str(e)}"

    #============================================
    # Asigna un profesor a un curso
    #============================================
    @staticmethod
    def asignar_profesor(session: Session, curso_id: int, profesor_id: int):
        return CursoDAO.actualizar(session, curso_id, profesor_id=profesor_id)

    #============================================
    # Cuenta estudiantes inscritos en un curso
    #============================================
    @staticmethod
    def contar_estudiantes_inscritos(session: Session, curso_id: int):
        from modelos.matricula import Matricula
        return session.query(Matricula).filter(
            Matricula.curso_id == curso_id,
            Matricula.estado == 'Inscrito'
        ).count()

    #============================================
    # Obtiene todos los estudiantes inscritos en un curso
    #============================================
    @staticmethod
    def obtener_estudiantes_curso(session: Session, curso_id: int):
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if curso:
            from modelos.matricula import Matricula
            matriculas = session.query(Matricula).filter(
                Matricula.curso_id == curso_id,
                Matricula.estado == 'Inscrito'
            ).all()
            return [m.estudiante for m in matriculas]
        return []
