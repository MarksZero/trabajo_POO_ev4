# ============================================
# iu/menu_reportes.py
# Menú de reportes y estadísticas
# ============================================

from sqlalchemy.orm import Session
from negocio.gestor_sistema import GestorSistema
from auxiliares.formateadores import Formateadores


# --------------------------------------------
# Clase para el menú de reportes y estadísticas
# --------------------------------------------
class MenuReportes:
    # Constructor: recibe la sesión de base de datos
    def __init__(self, session: Session):
        self.session = session

    # ----------------------------------------
    # Muestra el menú de opciones de reportes
    # ----------------------------------------
    def mostrar(self):
        while True:
            print(Formateadores.formatear_titulo("REPORTES Y ESTADÍSTICAS"))
            print("1. Reporte Completo de Estudiante")
            print("2. Reporte Completo de Curso")
            print("3. Reporte Completo de Profesor")
            print("4. Estadísticas Generales del Sistema")
            print("5. Historial Académico de Estudiante")
            print("0. Volver")
            print(Formateadores.formatear_separador())

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._reporte_estudiante()
            elif opcion == "2":
                self._reporte_curso()
            elif opcion == "3":
                self._reporte_profesor()
            elif opcion == "4":
                self._estadisticas_generales()
            elif opcion == "5":
                self._historial_academico()
            elif opcion == "0":
                break
            else:
                print("✗ Opción inválida")

            if opcion != "0":
                input("\nPresione Enter para continuar...")

    # ----------------------------------------
    # Opción: generar reporte completo de estudiante
    # ----------------------------------------
    def _reporte_estudiante(self):
        print("\n--- REPORTE DE ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            reporte, error = GestorSistema.generar_reporte_estudiante(
                self.session, estudiante_id
            )

            if error:
                print(f"\n✗ {error}")
                return

            texto = GestorSistema.formatear_reporte_estudiante(reporte)
            print(texto)

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: generar reporte completo de curso
    # ----------------------------------------
    def _reporte_curso(self):
        print("\n--- REPORTE DE CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))

            reporte, error = GestorSistema.generar_reporte_curso(
                self.session, curso_id
            )

            if error:
                print(f"\n✗ {error}")
                return

            texto = GestorSistema.formatear_reporte_curso(reporte)
            print(texto)

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: generar reporte completo de profesor
    # ----------------------------------------
    def _reporte_profesor(self):
        print("\n--- REPORTE DE PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            reporte, error = GestorSistema.generar_reporte_profesor(
                self.session, profesor_id
            )

            if error:
                print(f"\n✗ {error}")
                return

            p = reporte['profesor']
            print(Formateadores.formatear_titulo("REPORTE DE PROFESOR"))
            print(f"\nNombre: {p['nombre']} {p['apellido']}")
            print(f"RUT: {Formateadores.formatear_rut(p['rut'])}")
            print(f"Email: {p['email']}")
            print(f"Estado: {p['estado']}")
            print(Formateadores.formatear_separador())

            print(f"\nCantidad de cursos: {reporte['cantidad_cursos']}")
            print(f"Total de estudiantes: {reporte['total_estudiantes']}")

            if reporte['cursos']:
                print(Formateadores.formatear_titulo("CURSOS DICTADOS", 60))
                for item in reporte['cursos']:
                    c = item['curso']
                    print(f"\n• {c['codigo']} - {c['nombre']}")
                    print(f"  Créditos: {c['creditos']}")
                    print(f"  Estudiantes inscritos: {item['cantidad_estudiantes']}")
                    print(f"  Semestre: {c['semestre']}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: mostrar estadísticas generales del sistema
    # ----------------------------------------
    def _estadisticas_generales(self):
        print("\n--- ESTADÍSTICAS GENERALES ---")
        try:
            stats = GestorSistema.obtener_estadisticas_generales(self.session)

            print(Formateadores.formatear_titulo("ESTADÍSTICAS DEL SISTEMA"))
            print(f"\nTotal de Estudiantes: {stats['total_estudiantes']}")
            print(f"Total de Profesores: {stats['total_profesores']}")
            print(f"Total de Cursos: {stats['total_cursos']}")

            if stats['estudiantes_por_carrera']:
                print(Formateadores.formatear_titulo("ESTUDIANTES POR CARRERA", 60))
                total = sum(item['cantidad'] for item in stats['estudiantes_por_carrera'])

                for item in stats['estudiantes_por_carrera']:
                    porcentaje = (item['cantidad'] / total * 100) if total > 0 else 0
                    print(f"\n{item['carrera']}")
                    print(f"  Cantidad: {item['cantidad']} ({porcentaje:.1f}%)")

                    barra_length = int(porcentaje / 2)
                    barra = "█" * barra_length + "░" * (50 - barra_length)
                    print(f"  [{barra}]")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: mostrar historial académico de estudiante
    # ----------------------------------------
    def _historial_academico(self):
        print("\n--- HISTORIAL ACADÉMICO ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            from datos.estudiante_dao import EstudianteDAO
            from datos.historial_dao import HistorialDAO
            from datos.curso_dao import CursoDAO

            estudiante = EstudianteDAO.obtener_por_id(self.session, estudiante_id)
            if not estudiante:
                print("\n✗ Estudiante no encontrado")
                return

            historial = HistorialDAO.obtener_por_estudiante(self.session, estudiante_id)

            if not historial:
                print("\nEl estudiante no tiene historial académico registrado")
                return

            print(Formateadores.formatear_titulo("HISTORIAL ACADÉMICO"))
            print(f"Estudiante: {estudiante.nombre_completo()}")
            print(f"RUT: {Formateadores.formatear_rut(estudiante.rut)}")
            print(f"Carrera: {estudiante.carrera}")
            print(Formateadores.formatear_separador())

            semestres = {}
            for h in historial:
                if h.semestre not in semestres:
                    semestres[h.semestre] = []
                semestres[h.semestre].append(h)

            for semestre in sorted(semestres.keys()):
                print(f"\n{Formateadores.formatear_titulo(f'SEMESTRE {semestre}', 60)}")

                registros = semestres[semestre]
                suma_notas = 0
                suma_creditos = 0

                for h in registros:
                    curso = CursoDAO.obtener_por_id(self.session, h.curso_id)
                    nota_formateada = Formateadores.formatear_nota(float(h.nota))
                    estado = "✓ Aprobado" if h.nota >= 4.0 else "✗ Reprobado"

                    print(f"\n• {curso.codigo} - {curso.nombre}")
                    print(f"  Nota: {nota_formateada} | Créditos: {h.creditos} | {estado}")

                    suma_notas += float(h.nota) * h.creditos
                    suma_creditos += h.creditos

                if suma_creditos > 0:
                    promedio_semestre = suma_notas / suma_creditos
                    print(f"\nPromedio del semestre: {Formateadores.formatear_promedio(promedio_semestre)}")

            promedio_general = HistorialDAO.calcular_promedio(self.session, estudiante_id)
            creditos_aprobados = HistorialDAO.contar_creditos_aprobados(self.session, estudiante_id)
            total_creditos = sum(h.creditos for h in historial)

            print(Formateadores.formatear_titulo("RESUMEN GENERAL", 60))
            print(f"\nPromedio General: {Formateadores.formatear_promedio(promedio_general)}")
            print(f"Créditos Aprobados: {creditos_aprobados}")
            print(f"Créditos Totales Cursados: {total_creditos}")
            print(f"Porcentaje de Aprobación: {(creditos_aprobados / total_creditos * 100):.1f}%")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
