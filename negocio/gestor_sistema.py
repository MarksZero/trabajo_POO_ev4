#============================================
# negocio/gestor_sistema.py
# Gestor principal del sistema - Orquesta las operaciones generales
#============================================

from sqlalchemy.orm import Session
from datos.estudiante_dao import EstudianteDAO
from datos.profesor_dao import ProfesorDAO
from datos.curso_dao import CursoDAO
from datos.historial_dao import HistorialDAO
from auxiliares.formateadores import Formateadores


class GestorSistema:
    # Clase que orquesta las operaciones generales del sistema

    @staticmethod
    def generar_reporte_estudiante(session: Session, estudiante_id: int):
        # Genera un reporte completo de un estudiante
        from datos.matricula_dao import MatriculaDAO

        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return None, "Estudiante no encontrado"

        # Obtener matrículas actuales
        matriculas = MatriculaDAO.obtener_por_estudiante(session, estudiante_id)

        # Calcular créditos actuales
        creditos_actuales = MatriculaDAO.calcular_creditos_estudiante(session, estudiante_id)

        # Obtener historial
        historial = HistorialDAO.obtener_por_estudiante(session, estudiante_id)

        # Calcular promedio
        promedio = HistorialDAO.calcular_promedio(session, estudiante_id)

        # Contar créditos aprobados
        creditos_aprobados = HistorialDAO.contar_creditos_aprobados(session, estudiante_id)

        reporte = {
            'estudiante': estudiante.to_dict(),
            'creditos_actuales': creditos_actuales,
            'cantidad_cursos_actuales': len(matriculas),
            'promedio_general': promedio,
            'creditos_aprobados': creditos_aprobados,
            'cursos_actuales': [
                {
                    'curso': m.curso.to_dict(),
                    'estado': m.estado
                }
                for m in matriculas
            ],
            'historial': [h.to_dict() for h in historial]
        }

        return reporte, None

    @staticmethod
    def generar_reporte_curso(session: Session, curso_id: int):
        # Genera un reporte completo de un curso
        curso = CursoDAO.obtener_por_id(session, curso_id)
        if not curso:
            return None, "Curso no encontrado"

        # Obtener estudiantes inscritos
        estudiantes = CursoDAO.obtener_estudiantes_curso(session, curso_id)

        # Obtener profesor
        profesor = None
        if curso.profesor_id:
            profesor = ProfesorDAO.obtener_por_id(session, curso.profesor_id)

        reporte = {
            'curso': curso.to_dict(),
            'profesor': profesor.to_dict() if profesor else None,
            'cantidad_estudiantes': len(estudiantes),
            'estudiantes_inscritos': [e.to_dict() for e in estudiantes]
        }

        return reporte, None

    @staticmethod
    def generar_reporte_profesor(session: Session, profesor_id: int):
        # Genera un reporte completo de un profesor
        profesor = ProfesorDAO.obtener_por_id(session, profesor_id)
        if not profesor:
            return None, "Profesor no encontrado"

        # Obtener cursos
        cursos = ProfesorDAO.obtener_cursos_profesor(session, profesor_id)

        # Calcular estadísticas de los cursos
        total_estudiantes = 0
        cursos_info = []

        for curso in cursos:
            cantidad_estudiantes = CursoDAO.contar_estudiantes_inscritos(session, curso.curso_id)
            total_estudiantes += cantidad_estudiantes

            cursos_info.append({
                'curso': curso.to_dict(),
                'cantidad_estudiantes': cantidad_estudiantes
            })

        reporte = {
            'profesor': profesor.to_dict(),
            'cantidad_cursos': len(cursos),
            'total_estudiantes': total_estudiantes,
            'cursos': cursos_info
        }

        return reporte, None

    @staticmethod
    def obtener_estadisticas_generales(session: Session):
        # Obtiene estadísticas generales del sistema
        total_estudiantes = len(EstudianteDAO.obtener_todos(session))
        total_profesores = len(ProfesorDAO.obtener_todos(session))
        total_cursos = len(CursoDAO.obtener_todos(session))

        # Estudiantes por carrera
        estudiantes_carrera = EstudianteDAO.contar_por_carrera(session)

        estadisticas = {
            'total_estudiantes': total_estudiantes,
            'total_profesores': total_profesores,
            'total_cursos': total_cursos,
            'estudiantes_por_carrera': [
                {'carrera': carr, 'cantidad': cant}
                for carr, cant in estudiantes_carrera
            ]
        }

        return estadisticas

    @staticmethod
    def formatear_reporte_estudiante(reporte: dict) -> str:
        # Formatea el reporte de estudiante para visualización
        est = reporte['estudiante']

        texto = Formateadores.formatear_titulo("REPORTE DE ESTUDIANTE")
        texto += f"\nNombre: {est['nombre']} {est['apellido']}\n"
        texto += f"RUT: {Formateadores.formatear_rut(est['rut'])}\n"
        texto += f"Email: {est['email']}\n"
        texto += f"Carrera: {est['carrera']}\n"
        texto += f"Estado: {est['estado']}\n"
        texto += Formateadores.formatear_separador() + "\n"

        texto += f"Créditos actuales: {reporte['creditos_actuales']}/{est['creditos_maximos']}\n"
        texto += f"Cursos actuales: {reporte['cantidad_cursos_actuales']}\n"
        texto += f"Promedio general: {Formateadores.formatear_promedio(reporte['promedio_general'])}\n"
        texto += f"Créditos aprobados: {reporte['creditos_aprobados']}\n"

        if reporte['cursos_actuales']:
            texto += "\n" + Formateadores.formatear_titulo("CURSOS INSCRITOS", 60)
            for item in reporte['cursos_actuales']:
                c = item['curso']
                texto += f"\n• {c['codigo']} - {c['nombre']}\n"
                texto += f"  Créditos: {c['creditos']} | Estado: {item['estado']}\n"

        if reporte['historial']:
            texto += "\n" + Formateadores.formatear_titulo("HISTORIAL ACADÉMICO", 60)
            for h in reporte['historial']:
                texto += f"\nSemestre: {h['semestre']}\n"
                texto += f"Curso ID: {h['curso_id']} | Nota: {Formateadores.formatear_nota(h['nota'])} | Créditos: {h['creditos']}\n"

        return texto

    @staticmethod
    def formatear_reporte_curso(reporte: dict) -> str:
        # Formatea el reporte de curso para visualización
        c = reporte['curso']

        texto = Formateadores.formatear_titulo("REPORTE DE CURSO")
        texto += f"\nCódigo: {c['codigo']}\n"
        texto += f"Nombre: {c['nombre']}\n"
        texto += f"Créditos: {c['creditos']}\n"
        texto += f"Semestre: {c['semestre']}\n"
        texto += f"Estado: {c['estado']}\n"
        texto += Formateadores.formatear_separador() + "\n"

        if reporte['profesor']:
            p = reporte['profesor']
            texto += f"\nProfesor: {p['nombre']} {p['apellido']}\n"
            texto += f"Email: {p['email']}\n"
        else:
            texto += "\nProfesor: Sin asignar\n"

        texto += f"\nEstudiantes inscritos: {reporte['cantidad_estudiantes']}/{c['capacidad_maxima']}\n"

        if reporte['estudiantes_inscritos']:
            texto += "\n" + Formateadores.formatear_titulo("ESTUDIANTES INSCRITOS", 60)
            for e in reporte['estudiantes_inscritos']:
                texto += f"\n• {e['nombre']} {e['apellido']} ({Formateadores.formatear_rut(e['rut'])})\n"
                texto += f"  Carrera: {e['carrera']}\n"

        return texto
