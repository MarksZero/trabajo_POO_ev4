#============================================
# auxiliares/validadores.py
# Funciones de validación de datos
#============================================

import re
from .constantes import Constantes


class Validadores:
    #============================================
    # Clase con métodos estáticos para validar datos
    #============================================

    #============================================
    # Valida formato de RUT chileno
    #============================================
    @staticmethod
    def validar_rut(rut: str) -> tuple[bool, str]:
        if not rut:
            return False, "RUT no puede estar vacío"

        #============================================
        # Remover puntos y guión
        #============================================
        rut_limpio = rut.replace(".", "").replace("-", "")

        if len(rut_limpio) < Constantes.LONGITUD_RUT_MIN or len(rut_limpio) > Constantes.LONGITUD_RUT_MAX:
            return False, f"RUT debe tener entre {Constantes.LONGITUD_RUT_MIN} y {Constantes.LONGITUD_RUT_MAX} caracteres"

        return True, "RUT válido"

    #============================================
    # Valida formato de email
    #============================================
    @staticmethod
    def validar_email(email: str) -> tuple[bool, str]:
        if not email:
            return False, "Email no puede estar vacío"

        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

        if not re.match(patron, email):
            return False, "Formato de email inválido"

        return True, "Email válido"

    #============================================
    # Valida que la nota esté en el rango válido
    #============================================
    @staticmethod
    def validar_nota(nota: float) -> tuple[bool, str]:
        if nota < Constantes.NOTA_MINIMA or nota > Constantes.NOTA_MAXIMA:
            return False, f"La nota debe estar entre {Constantes.NOTA_MINIMA} y {Constantes.NOTA_MAXIMA}"

        return True, "Nota válida"

    #============================================
    # Valida que los créditos sean positivos
    #============================================
    @staticmethod
    def validar_creditos(creditos: int) -> tuple[bool, str]:
        if creditos <= 0:
            return False, "Los créditos deben ser mayores a 0"

        if creditos > 20:
            return False, "Los créditos no pueden exceder 20"

        return True, "Créditos válidos"

    #============================================
    # Valida formato de semestre (ej: 2024-1)
    #============================================
    @staticmethod
    def validar_semestre(semestre: str) -> tuple[bool, str]:
        if not semestre:
            return False, "Semestre no puede estar vacío"

        if not re.match(Constantes.FORMATO_SEMESTRE, semestre):
            return False, "Formato de semestre inválido. Use: YYYY-1 o YYYY-2"

        return True, "Semestre válido"

    #============================================
    # Valida que un texto no esté vacío
    #============================================
    @staticmethod
    def validar_texto_no_vacio(texto: str, nombre_campo: str) -> tuple[bool, str]:
        if not texto or texto.strip() == "":
            return False, f"{nombre_campo} no puede estar vacío"

        return True, f"{nombre_campo} válido"

    #============================================
    # Valida que un número sea positivo
    #============================================
    @staticmethod
    def validar_numero_positivo(numero: int, nombre_campo: str) -> tuple[bool, str]:
        if numero <= 0:
            return False, f"{nombre_campo} debe ser mayor a 0"

        return True, f"{nombre_campo} válido"
