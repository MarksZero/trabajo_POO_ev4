#============================================
# negocio/gestor_estudiantes.py
# Gestor de lógica de negocio para Estudiantes
#============================================

from sqlalchemy.orm import Session
from datos.estudiante_dao import EstudianteDAO
from auxiliares.validadores import Validadores
from auxiliares.formateadores import Formateadores
from auxiliares.constantes import Constantes


class GestorEstudiantes:
    # Clase que implementa la lógica de negocio para estudiantes

    @staticmethod
    def crear_estudiante(session: Session, rut: str, nombre: str, apellido: str,
                        email: str, carrera: str, creditos_maximos: int = None):
        # Crea un estudiante con validaciones de negocio

        # Validar RUT
        valido, mensaje = Validadores.validar_rut(rut)
        if not valido:
            return None, mensaje

        # Validar email
        valido, mensaje = Validadores.validar_email(email)
        if not valido:
            return None, mensaje

        # Validar nombre
        valido, mensaje = Validadores.validar_texto_no_vacio(nombre, "Nombre")
        if not valido:
            return None, mensaje

        # Validar apellido
        valido, mensaje = Validadores.validar_texto_no_vacio(apellido, "Apellido")
        if not valido:
            return None, mensaje

        # Validar carrera
        valido, mensaje = Validadores.validar_texto_no_vacio(carrera, "Carrera")
        if not valido:
            return None, mensaje

        # Establecer créditos máximos por defecto
        if creditos_maximos is None:
            creditos_maximos = Constantes.CREDITOS_MAXIMOS_DEFAULT
        else:
            valido, mensaje = Validadores.validar_numero_positivo(creditos_maximos, "Créditos máximos")
            if not valido:
                return None, mensaje

        # Formatear datos
        nombre = Formateadores.capitalizar_nombre(nombre)
        apellido = Formateadores.capitalizar_nombre(apellido)

        # Crear en la base de datos
        return EstudianteDAO.crear(
            session, rut, nombre, apellido, email, carrera, creditos_maximos
        )

    @staticmethod
    def obtener_estudiante(session: Session, estudiante_id: int):
        # Obtiene un estudiante por ID
        estudiante = EstudianteDAO.obtener_por_id(session, estudiante_id)
        if not estudiante:
            return None, "Estudiante no encontrado"
        return estudiante, None

    @staticmethod
    def listar_estudiantes(session: Session, solo_activos: bool = True):
        # Lista todos los estudiantes
        return EstudianteDAO.obtener_todos(session, solo_activos)

    @staticmethod
    def listar_por_carrera(session: Session, carrera: str):
        # Lista estudiantes por carrera
        return EstudianteDAO.obtener_por_carrera(session, carrera)

    @staticmethod
    def actualizar_estudiante(session: Session, estudiante_id: int, **kwargs):
        # Actualiza un estudiante con validaciones

        # Validar email si se proporciona
        if 'email' in kwargs:
            valido, mensaje = Validadores.validar_email(kwargs['email'])
            if not valido:
                return None, mensaje

        # Validar créditos si se proporcionan
        if 'creditos_maximos' in kwargs:
            valido, mensaje = Validadores.validar_numero_positivo(
                kwargs['creditos_maximos'], "Créditos máximos"
            )
            if not valido:
                return None, mensaje

        # Formatear nombre y apellido si se proporcionan
        if 'nombre' in kwargs:
            kwargs['nombre'] = Formateadores.capitalizar_nombre(kwargs['nombre'])
        if 'apellido' in kwargs:
            kwargs['apellido'] = Formateadores.capitalizar_nombre(kwargs['apellido'])

        return EstudianteDAO.actualizar(session, estudiante_id, **kwargs)

    @staticmethod
    def eliminar_estudiante(session: Session, estudiante_id: int):
        # Elimina un estudiante
        return EstudianteDAO.eliminar(session, estudiante_id)

    @staticmethod
    def cambiar_estado_estudiante(session: Session, estudiante_id: int, nuevo_estado: str):
        # Cambia el estado de un estudiante
        if nuevo_estado not in Constantes.ESTADOS_ESTUDIANTE:
            return None, f"Estado inválido. Debe ser uno de: {', '.join(Constantes.ESTADOS_ESTUDIANTE)}"

        return EstudianteDAO.cambiar_estado(session, estudiante_id, nuevo_estado)

    @staticmethod
    def obtener_estadisticas_carreras(session: Session):
        # Obtiene estadísticas de estudiantes por carrera
        return EstudianteDAO.contar_por_carrera(session)
