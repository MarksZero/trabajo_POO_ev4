# ============================================
# iu/menu_principal.py
# Menú principal del sistema
# ============================================

from datos.conexion import SessionLocal
from .menu_estudiantes import MenuEstudiantes
from .menu_profesores import MenuProfesores
from .menu_cursos import MenuCursos
from .menu_reportes import MenuReportes
from auxiliares.formateadores import Formateadores
from negocio.gestor_sistema import GestorSistema


# --------------------------------------------
# Clase principal del menú del sistema
# --------------------------------------------
class MenuPrincipal:
    # Constructor: inicializa la sesión y los submenús
    def __init__(self):
        self.session = SessionLocal()
        self.menu_estudiantes = MenuEstudiantes(self.session)
        self.menu_profesores = MenuProfesores(self.session)
        self.menu_cursos = MenuCursos(self.session)
        self.menu_reportes = MenuReportes(self.session)

    # ----------------------------------------
    # Muestra el menú principal
    # ----------------------------------------
    def mostrar_menu(self):
        print(Formateadores.formatear_titulo("SISTEMA DE MATRÍCULA UNIVERSITARIA"))
        print("1.  Gestión de Estudiantes")
        print("2.  Gestión de Profesores")
        print("3.  Gestión de Cursos")
        print("4.  Gestión de Matrículas")
        print("5.  Reportes y Estadísticas")
        print("0.  Salir")
        print(Formateadores.formatear_separador())

    # ----------------------------------------
    # Ejecuta el menú principal
    # ----------------------------------------
    def ejecutar(self):
        try:
            while True:
                self.mostrar_menu()
                opcion = input("\nSeleccione una opción: ").strip()

                if opcion == "1":
                    self.menu_estudiantes.mostrar()
                elif opcion == "2":
                    self.menu_profesores.mostrar()
                elif opcion == "3":
                    self.menu_cursos.mostrar()
                elif opcion == "4":
                    self.gestionar_matriculas()
                elif opcion == "5":
                    self.menu_reportes.mostrar()
                elif opcion == "0":
                    print("\n¡Hasta luego!")
                    break
                else:
                    print("✗ Opción inválida")

                input("\nPresione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\nPrograma interrumpido por el usuario")
        except Exception as e:
            print(f"\n✗ Error: {str(e)}")
        finally:
            self.session.close()
            print("Conexión cerrada")

    # ----------------------------------------
    # Submenú: gestión de matrículas
    # ----------------------------------------
    def gestionar_matriculas(self):
        from negocio.gestor_matriculas import GestorMatriculas

        while True:
            print(Formateadores.formatear_titulo("GESTIÓN DE MATRÍCULAS"))
            print("1. Matricular Estudiante en Curso")
            print("2. Ver Cursos Disponibles para Estudiante")
            print("3. Retirar Estudiante de Curso")
            print("4. Registrar Nota")
            print("5. Ver Matrículas de Estudiante")
            print("6. Ver Matrículas de Curso")
            print("0. Volver")
            print(Formateadores.formatear_separador())

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._matricular_estudiante()
            elif opcion == "2":
                self._ver_cursos_disponibles()
            elif opcion == "3":
                self._retirar_estudiante()
            elif opcion == "4":
                self._registrar_nota()
            elif opcion == "5":
                self._ver_matriculas_estudiante()
            elif opcion == "6":
                self._ver_matriculas_curso()
            elif opcion == "0":
                break
            else:
                print("✗ Opción inválida")

            if opcion != "0":
                input("\nPresione Enter para continuar...")

    # ----------------------------------------
    # Opción: matricular estudiante
    # ----------------------------------------
    def _matricular_estudiante(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- MATRICULAR ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))
            curso_id = int(input("ID del Curso: "))

            exito, mensaje = GestorMatriculas.matricular_estudiante(
                self.session, estudiante_id, curso_id
            )

            if exito:
                print(f"✓ {mensaje}")
            else:
                print(f"✗ {mensaje}")
        except ValueError:
            print("✗ Error: Debe ingresar números válidos")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver cursos disponibles
    # ----------------------------------------
    def _ver_cursos_disponibles(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- CURSOS DISPONIBLES ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            cursos, error = GestorMatriculas.listar_cursos_disponibles(
                self.session, estudiante_id
            )

            if error:
                print(f"✗ {error}")
                return

            if not cursos:
                print("No hay cursos disponibles")
                return

            print("\nCursos disponibles:")
            for item in cursos:
                c = item['curso']
                estado = "✓" if item['puede_inscribir'] else "✗"
                print(f"\n{estado} ID {c['curso_id']}: {c['codigo']} - {c['nombre']}")
                print(f"   Créditos: {c['creditos']}")
                print(f"   Cupos: {item['cupos_disponibles']}/{c['capacidad_maxima']}")
                if item['motivo_rechazo']:
                    print(f"   Motivo: {item['motivo_rechazo']}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: retirar estudiante de curso
    # ----------------------------------------
    def _retirar_estudiante(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- RETIRAR ESTUDIANTE DE CURSO ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))
            curso_id = int(input("ID del Curso: "))

            exito, mensaje = GestorMatriculas.retirar_estudiante(
                self.session, estudiante_id, curso_id
            )

            if exito:
                print(f"✓ {mensaje}")
            else:
                print(f"✗ {mensaje}")
        except ValueError:
            print("✗ Error: Debe ingresar números válidos")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: registrar nota
    # ----------------------------------------
    def _registrar_nota(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- REGISTRAR NOTA ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))
            curso_id = int(input("ID del Curso: "))
            semestre = input("Semestre (ej: 2024-1): ")
            nota = float(input("Nota (1.0 - 7.0): "))

            exito, mensaje = GestorMatriculas.registrar_nota(
                self.session, estudiante_id, curso_id, semestre, nota
            )

            if exito:
                print(f"✓ {mensaje}")
            else:
                print(f"✗ {mensaje}")
        except ValueError:
            print("✗ Error: Formato inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver matrículas por estudiante
    # ----------------------------------------
    def _ver_matriculas_estudiante(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- MATRÍCULAS DEL ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            matriculas, error = GestorMatriculas.listar_matriculas_estudiante(
                self.session, estudiante_id, solo_inscritos=False
            )

            if error:
                print(f"✗ {error}")
                return

            if not matriculas:
                print("El estudiante no tiene matrículas registradas")
                return

            print(f"\nTotal de matrículas: {len(matriculas)}")
            for m in matriculas:
                print(f"\n• Curso: {m.curso.codigo} - {m.curso.nombre}")
                print(f"  Estado: {m.estado}")
                print(f"  Créditos: {m.curso.creditos}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver matrículas por curso
    # ----------------------------------------
    def _ver_matriculas_curso(self):
        from negocio.gestor_matriculas import GestorMatriculas

        print("\n--- MATRÍCULAS DEL CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))

            matriculas, error = GestorMatriculas.listar_matriculas_curso(
                self.session, curso_id, solo_inscritos=True
            )

            if error:
                print(f"✗ {error}")
                return

            if not matriculas:
                print("El curso no tiene estudiantes inscritos")
                return

            print(f"\nTotal de estudiantes inscritos: {len(matriculas)}")
            for m in matriculas:
                print(f"\n• {m.estudiante.nombre_completo()}")
                print(f"  RUT: {m.estudiante.rut}")
                print(f"  Carrera: {m.estudiante.carrera}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
