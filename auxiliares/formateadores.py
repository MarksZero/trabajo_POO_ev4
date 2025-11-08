#============================================
# auxiliares/formateadores.py
# Funciones de formateo y conversión de datos
#============================================


class Formateadores:
    #============================================
    # Clase con métodos estáticos para formatear datos
    #============================================

    #============================================
    # Formatea un RUT a lo chileno con puntos y guión
    #============================================
    @staticmethod
    def formatear_rut(rut: str) -> str:
        #============================================
        # Remover formato existente
        #============================================
        rut_limpio = rut.replace(".", "").replace("-", "")

        if len(rut_limpio) < 2:
            return rut

        #============================================
        # Separar número y dígito verificador
        #============================================
        cuerpo = rut_limpio[:-1]
        dv = rut_limpio[-1]

        #============================================
        # Agregar puntos cada 3 dígitos (de derecha a izquierda)
        #============================================
        cuerpo_formateado = ""
        for i, digito in enumerate(reversed(cuerpo)):
            if i > 0 and i % 3 == 0:
                cuerpo_formateado = "." + cuerpo_formateado
            cuerpo_formateado = digito + cuerpo_formateado

        return f"{cuerpo_formateado}-{dv}"

    #============================================
    # Formatea una nota con 1 decimal
    #============================================
    @staticmethod
    def formatear_nota(nota: float) -> str:
        return f"{nota:.1f}"

    #============================================
    # Formatea un promedio con 2 decimales
    #============================================
    @staticmethod
    def formatear_promedio(promedio: float) -> str:
        return f"{promedio:.2f}"

    #============================================
    # Formatea un título centrado con bordes
    #============================================
    @staticmethod
    def formatear_titulo(texto: str, ancho: int = 60) -> str:
        linea = "=" * ancho
        texto_centrado = texto.center(ancho)
        return f"\n{linea}\n{texto_centrado}\n{linea}"

    #============================================
    # Retorna un separador de línea
    #============================================
    @staticmethod
    def formatear_separador(ancho: int = 60) -> str:
        return "-" * ancho

    #============================================
    # Formatea una lista numerada
    #============================================
    @staticmethod
    def formatear_lista_numerada(items: list, prefijo: str = "") -> str:
        resultado = ""
        for i, item in enumerate(items, 1):
            resultado += f"{prefijo}{i}. {item}\n"
        return resultado

    #============================================
    # Formatea una tabla simple
    #============================================
    @staticmethod
    def formatear_tabla_simple(headers: list, rows: list) -> str:
        #============================================
        # Calcular ancho de columnas
        #============================================
        anchos = [len(str(h)) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                anchos[i] = max(anchos[i], len(str(cell)))

        #============================================
        # Crear formato
        #============================================
        formato = " | ".join([f"{{:<{ancho}}}" for ancho in anchos])

        #============================================
        # Header
        #============================================
        resultado = formato.format(*headers) + "\n"
        resultado += "-" * (sum(anchos) + 3 * (len(headers) - 1)) + "\n"

        #============================================
        # Rows
        #============================================
        for row in rows:
            resultado += formato.format(*row) + "\n"

        return resultado

    #============================================
    # Trunca un texto si excede la longitud máxima
    #============================================
    @staticmethod
    def truncar_texto(texto: str, longitud: int = 50) -> str:
        if len(texto) <= longitud:
            return texto
        return texto[:longitud - 3] + "..."

    #============================================
    # Capitaliza correctamente un nombre
    #============================================
    @staticmethod
    def capitalizar_nombre(nombre: str) -> str:
        return " ".join(word.capitalize() for word in nombre.split())
