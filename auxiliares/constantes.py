#============================================
# auxiliares/constantes.py
# Constantes del sistema
#============================================

class Constantes:
    #============================================
    # Constantes generales del sistema
    #============================================

    #============================================
    # Límites del sistema
    #============================================
    CREDITOS_MAXIMOS_DEFAULT = 20
    CAPACIDAD_CURSO_DEFAULT = 40
    MAX_CURSOS_PROFESOR = 5

    #============================================
    # Rangos de notas
    #============================================
    NOTA_MINIMA = 1.0
    NOTA_MAXIMA = 7.0
    NOTA_APROBACION = 4.0

    #============================================
    # Estados
    #============================================
    ESTADOS_ESTUDIANTE = ['Activo', 'Inactivo', 'Egresado']
    ESTADOS_PROFESOR = ['Activo', 'Inactivo']
    ESTADOS_CURSO = ['Activo', 'Inactivo']
    ESTADOS_MATRICULA = ['Inscrito', 'Retirado', 'Aprobado', 'Reprobado']

    #============================================
    # Mensajes
    #============================================
    MSG_EXITO_CREACION = "Registro creado exitosamente"
    MSG_ERROR_DUPLICADO = "El registro ya existe"
    MSG_ERROR_NO_ENCONTRADO = "Registro no encontrado"
    MSG_EXITO_ACTUALIZACION = "Registro actualizado exitosamente"
    MSG_EXITO_ELIMINACION = "Registro eliminado exitosamente"

    #============================================
    # Formatos
    #============================================
    FORMATO_SEMESTRE = r'^\d{4}-[12]$'  # Ej: 2024-1 o 2024-2
    LONGITUD_RUT_MIN = 9
    LONGITUD_RUT_MAX = 12
