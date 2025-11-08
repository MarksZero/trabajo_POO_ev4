#============================================
# negocio/gestor_matriculas.py
# Gestor de lógica de negocio para Matrículas
#============================================

from sqlalchemy.orm import Session
from datos.matricula_dao import MatriculaDAO
from datos.estudiante_dao import EstudianteDAO
from datos.curso_dao import CursoDAO
from datos.historial_dao import HistorialDAO
from auxiliares.validadores import Validadores
from auxiliares.constantes import Constantes


class GestorMatriculas:
    # Clase que implementa la lógica de negocio para matrículas

    @staticmethod
    def matricular_estudiante(session: Session, estudiante_id: int, curso_id: int):
        # Matricula un estudiante en un curso con todas las validaciones de negocio

        # Validar que el estudiante exista
        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return False, "Estudiante no encontrado"

        if estudiante.estado != 'Activo':
            return False, f"El estudiante no está activo (Estado: {estudiante.estado})"

        # Validar que el curso exista
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return False, "Curso no encontrado"

        if curso.estado != 'Activo':
            return False, f"El curso no está activo (Estado: {curso.estado})"

        # Validar que no esté ya inscrito
        matricula_existente = MatriculaDAO.obtener_matricula(session, estudiante_id, curso_id)
        if matricula_existente:
            return False, f"El estudiante ya está inscrito en este curso (Estado: {matricula_existente.estado})"

        # Validar créditos máximos
        creditos_actuales = MatriculaDAO.calcular_creditos_estudiante(session, estudiante_id)
        creditos_totales = creditos_actuales + curso.creditos

        if creditos_totales > estudiante.creditos_maximos:
            return False, (
                f"Excede el máximo de créditos permitidos. "
                f"Actuales: {creditos_actuales}, "
                f"Curso: {curso.creditos}, "
                f"Total: {creditos_totales}, "
                f"Máximo: {estudiante.creditos_maximos}"
            )

        # Validar capacidad del curso
        estudiantes_inscritos = CursoDAO.contar_estudiantes_inscritos(session, curso_id)
        if estudiantes_inscritos >= curso.capacidad_maxima:
            return False, f"El curso ha alcanzado su capacidad máxima ({estudiantes_inscritos}/{curso.capacidad_maxima})"

        # Crear la matrícula
        matricula, error = MatriculaDAO.crear(session, estudiante_id, curso_id)
        if not matricula:
            return False, error

        return True, f"Matrícula realizada exitosamente. Créditos totales: {creditos_totales}/{estudiante.creditos_maximos}"

    @staticmethod
    def retirar_estudiante(session: Session, estudiante_id: int, curso_id: int):
        # Retira a un estudiante de un curso
        matricula = MatriculaDAO.obtener_matricula(session, estudiante_id, curso_id)
        if not matricula:
            return False, "No existe una matrícula para este estudiante y curso"

        if matricula.estado != 'Inscrito':
            return False, f"La matrícula no está activa (Estado: {matricula.estado})"

        return MatriculaDAO.retirar_curso(session, estudiante_id, curso_id)

    @staticmethod
    def listar_matriculas_estudiante(session: Session, estudiante_id: int, solo_inscritos: bool = True):
        # Lista todas las matrículas de un estudiante
        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return None, "Estudiante no encontrado"

        matriculas = MatriculaDAO.obtener_por_estudiante(session, estudiante_id, solo_inscritos)
        return matriculas, None

    @staticmethod
    def listar_matriculas_curso(session: Session, curso_id: int, solo_inscritos: bool = True):
        # Lista todas las matrículas de un curso
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return None, "Curso no encontrado"

        matriculas = MatriculaDAO.obtener_por_curso(session, curso_id, solo_inscritos)
        return matriculas, None

    @staticmethod
    def registrar_nota(session: Session, estudiante_id: int, curso_id: int,
                      semestre: str, nota: float):
        # Registra una nota en el historial académico y actualiza el estado de la matrícula

        # Validar nota
        valido, mensaje = Validadores.validar_nota(nota)
        if not valido:
            return False, mensaje

        # Validar semestre
        valido, mensaje = Validadores.validar_semestre(semestre)
        if not valido:
            return False, mensaje

        # Validar que exista la matrícula
        matricula = MatriculaDAO.obtener_matricula(session, estudiante_id, curso_id)
        if not matricula:
            return False, "No existe una matrícula para este estudiante y curso"

        # Obtener el curso para los créditos
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return False, "Curso no encontrado"

        # Crear registro en historial
        historial, error = HistorialDAO.crear(
            session, estudiante_id, curso_id, semestre, nota, curso.creditos
        )
        if not historial:
            return False, error

        # Actualizar estado de matrícula
        nuevo_estado = 'Aprobado' if nota >= Constantes.NOTA_APROBACION else 'Reprobado'
        MatriculaDAO.actualizar_estado(session, matricula.matricula_id, nuevo_estado)

        return True, f"Nota registrada exitosamente. Estado: {nuevo_estado}"

    @staticmethod
    def calcular_creditos_estudiante(session: Session, estudiante_id: int):
        # Calcula los créditos actuales de un estudiante
        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return None, "Estudiante no encontrado"

        creditos_actuales = MatriculaDAO.calcular_creditos_estudiante(session, estudiante_id)
        return creditos_actuales, None

    @staticmethod
    def listar_cursos_disponibles(session: Session, estudiante_id: int):
        # Lista los cursos disponibles para un estudiante (con cupos y que no exceda créditos)
        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return None, "Estudiante no encontrado"

        # Obtener todos los cursos activos
        todos_cursos = CursoDAO.obtener_todos(session)

        # Obtener cursos en los que ya está inscrito
        matriculas = MatriculaDAO.obtener_por_estudiante(session, estudiante_id)
        cursos_inscritos = {m.curso_id for m in matriculas}

        # Calcular créditos actuales
        creditos_actuales = MatriculaDAO.calcular_creditos_estudiante(session, estudiante_id)

        cursos_disponibles = []
        for curso in todos_cursos:
            if curso.curso_id in cursos_inscritos:
                continue

            estudiantes_inscritos = CursoDAO.contar_estudiantes_inscritos(session, curso.curso_id)
            tiene_cupos = estudiantes_inscritos < curso.capacidad_maxima
            puede_inscribir_creditos = (creditos_actuales + curso.creditos) <= estudiante.creditos_maximos

            motivo_rechazo = []
            if not tiene_cupos:
                motivo_rechazo.append("Sin cupos disponibles")
            if not puede_inscribir_creditos:
                motivo_rechazo.append(f"Excedería créditos máximos ({creditos_actuales + curso.creditos}/{estudiante.creditos_maximos})")

            cursos_disponibles.append({
                'curso': curso.to_dict(),
                'estudiantes_inscritos': estudiantes_inscritos,
                'cupos_disponibles': curso.capacidad_maxima - estudiantes_inscritos,
                'tiene_cupos': tiene_cupos,
                'puede_inscribir': tiene_cupos and puede_inscribir_creditos,
                'motivo_rechazo': ', '.join(motivo_rechazo) if motivo_rechazo else None
            })

        return cursos_disponibles, None
