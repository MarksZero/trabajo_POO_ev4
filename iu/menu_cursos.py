# ============================================================
# MÓDULO: Menú de gestión de cursos
# ============================================================

from sqlalchemy.orm import Session
from negocio.gestor_cursos import GestorCursos
from auxiliares.formateadores import Formateadores


# ============================================================
# Clase para el menú de gestión de cursos
# ============================================================
class MenuCursos:

    def __init__(self, session: Session):
        self.session = session

    # --------------------------------------------------------
    # Muestra el menú principal de cursos
    # --------------------------------------------------------
    def mostrar(self):
        while True:
            print(Formateadores.formatear_titulo("GESTIÓN DE CURSOS"))
            print("1. Registrar Curso")
            print("2. Ver Curso por ID")
            print("3. Listar Todos los Cursos")
            print("4. Listar por Profesor")
            print("5. Listar por Semestre")
            print("6. Asignar Profesor a Curso")
            print("7. Ver Estudiantes del Curso")
            print("8. Actualizar Curso")
            print("9. Eliminar Curso")
            print("10. Verificar Disponibilidad")
            print("0. Volver")
            print(Formateadores.formatear_separador())

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._registrar_curso()
            elif opcion == "2":
                self._ver_curso()
            elif opcion == "3":
                self._listar_cursos()
            elif opcion == "4":
                self._listar_por_profesor()
            elif opcion == "5":
                self._listar_por_semestre()
            elif opcion == "6":
                self._asignar_profesor()
            elif opcion == "7":
                self._ver_estudiantes()
            elif opcion == "8":
                self._actualizar_curso()
            elif opcion == "9":
                self._eliminar_curso()
            elif opcion == "10":
                self._verificar_disponibilidad()
            elif opcion == "0":
                break
            else:
                print("✗ Opción inválida")

            if opcion != "0":
                input("\nPresione Enter para continuar...")

    # --------------------------------------------------------
    # Registrar un nuevo curso
    # --------------------------------------------------------
    def _registrar_curso(self):
        print("\n--- REGISTRAR CURSO ---")
        try:
            codigo = input("Código: ").strip()
            nombre = input("Nombre: ").strip()
            creditos = int(input("Créditos: "))
            capacidad_str = input("Capacidad máxima (Enter para 40): ").strip()
            semestre = input("Semestre (ej: 2024-1): ").strip()

            capacidad_maxima = int(capacidad_str) if capacidad_str else None

            curso, error = GestorCursos.crear_curso(
                self.session, codigo, nombre, creditos,
                None, capacidad_maxima, semestre if semestre else None
            )

            if curso:
                print(f"\n✓ Curso registrado exitosamente")
                print(f"ID: {curso.curso_id}")
                print(f"Código: {curso.codigo}")
                print(f"Nombre: {curso.nombre}")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Formato de datos inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Ver la información de un curso
    # --------------------------------------------------------
    def _ver_curso(self):
        print("\n--- VER CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))
            curso, error = GestorCursos.obtener_curso(self.session, curso_id)

            if error:
                print(f"\n✗ {error}")
                return

            from datos.curso_dao import CursoDAO
            inscritos = CursoDAO.contar_estudiantes_inscritos(self.session, curso_id)

            print(f"\n{Formateadores.formatear_separador()}")
            print(f"ID: {curso.curso_id}")
            print(f"Código: {curso.codigo}")
            print(f"Nombre: {curso.nombre}")
            print(f"Créditos: {curso.creditos}")
            print(f"Capacidad: {inscritos}/{curso.capacidad_maxima}")
            print(f"Semestre: {curso.semestre}")
            print(f"Estado: {curso.estado}")
            if curso.profesor:
                print(f"Profesor: {curso.profesor.nombre_completo()}")
            else:
                print("Profesor: Sin asignar")
            print(Formateadores.formatear_separador())

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Listar todos los cursos registrados
    # --------------------------------------------------------
    def _listar_cursos(self):
        print("\n--- LISTA DE CURSOS ---")
        try:
            solo_activos = input("¿Solo cursos activos? (S/N): ").strip().upper() == 'S'
            cursos = GestorCursos.listar_cursos(self.session, solo_activos)

            if not cursos:
                print("\nNo hay cursos registrados")
                return

            from datos.curso_dao import CursoDAO
            print(f"\nTotal: {len(cursos)} curso(s)")
            print(Formateadores.formatear_separador())

            for c in cursos:
                inscritos = CursoDAO.contar_estudiantes_inscritos(self.session, c.curso_id)
                profesor_nombre = c.profesor.nombre_completo() if c.profesor else "Sin asignar"
                print(f"\nID {c.curso_id}: {c.codigo} - {c.nombre}")
                print(f"  Créditos: {c.creditos} | Profesor: {profesor_nombre}")
                print(f"  Inscritos: {inscritos}/{c.capacidad_maxima} | Estado: {c.estado}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Listar cursos por profesor
    # --------------------------------------------------------
    def _listar_por_profesor(self):
        print("\n--- CURSOS POR PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))
            cursos = GestorCursos.listar_por_profesor(self.session, profesor_id)

            if not cursos:
                print("\nEl profesor no tiene cursos asignados")
                return

            from datos.curso_dao import CursoDAO
            print(f"\nTotal: {len(cursos)} curso(s)")
            print(Formateadores.formatear_separador())

            for c in cursos:
                inscritos = CursoDAO.contar_estudiantes_inscritos(self.session, c.curso_id)
                print(f"\n• {c.codigo} - {c.nombre}")
                print(f"  Créditos: {c.creditos}")
                print(f"  Inscritos: {inscritos}/{c.capacidad_maxima}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Listar cursos por semestre
    # --------------------------------------------------------
    def _listar_por_semestre(self):
        print("\n--- CURSOS POR SEMESTRE ---")
        try:
            semestre = input("Semestre (ej: 2024-1): ").strip()
            cursos, error = GestorCursos.listar_por_semestre(self.session, semestre)

            if error:
                print(f"\n✗ {error}")
                return

            if not cursos:
                print(f"\nNo hay cursos registrados en el semestre {semestre}")
                return

            from datos.curso_dao import CursoDAO
            print(f"\nTotal: {len(cursos)} curso(s)")
            print(Formateadores.formatear_separador())

            for c in cursos:
                inscritos = CursoDAO.contar_estudiantes_inscritos(self.session, c.curso_id)
                print(f"\n• {c.codigo} - {c.nombre}")
                print(f"  Créditos: {c.creditos}")
                print(f"  Inscritos: {inscritos}/{c.capacidad_maxima}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Asignar un profesor a un curso
    # --------------------------------------------------------
    def _asignar_profesor(self):
        print("\n--- ASIGNAR PROFESOR A CURSO ---")
        try:
            from negocio.gestor_profesores import GestorProfesores
            profesores = GestorProfesores.listar_profesores(self.session)

            if not profesores:
                print("\nNo hay profesores registrados")
                return

            print("\nProfesores disponibles:")
            for p in profesores:
                print(f"  ID {p.profesor_id}: {p.nombre_completo()}")

            profesor_id = int(input("\nID del Profesor: "))
            cursos = GestorCursos.listar_cursos(self.session)

            if not cursos:
                print("\nNo hay cursos registrados")
                return

            print("\nCursos disponibles:")
            for c in cursos:
                print(f"  ID {c.curso_id}: {c.codigo} - {c.nombre}")

            curso_id = int(input("\nID del Curso: "))
            resultado, error = GestorCursos.asignar_profesor(self.session, curso_id, profesor_id)

            if resultado:
                print(f"\n✓ Profesor asignado exitosamente")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Debe ingresar números válidos")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Ver los estudiantes inscritos en un curso
    # --------------------------------------------------------
    def _ver_estudiantes(self):
        print("\n--- ESTUDIANTES DEL CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))
            estudiantes, error = GestorCursos.obtener_estudiantes_curso(self.session, curso_id)

            if error:
                print(f"\n✗ {error}")
                return

            if not estudiantes:
                print("\nEl curso no tiene estudiantes inscritos")
                return

            print(f"\nTotal de estudiantes: {len(estudiantes)}")
            print(Formateadores.formatear_separador())

            for e in estudiantes:
                print(f"\n• {e.nombre_completo()}")
                print(f"  RUT: {Formateadores.formatear_rut(e.rut)}")
                print(f"  Carrera: {e.carrera}")
                print(f"  Email: {e.email}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Actualizar los datos de un curso
    # --------------------------------------------------------
    def _actualizar_curso(self):
        print("\n--- ACTUALIZAR CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))
            curso, error = GestorCursos.obtener_curso(self.session, curso_id)

            if error:
                print(f"\n✗ {error}")
                return

            print(f"\nCurso actual: {curso.codigo} - {curso.nombre}")
            print("\nDeje en blanco los campos que no desea modificar")

            nombre = input(f"Nuevo nombre ({curso.nombre}): ").strip()
            creditos_str = input(f"Nuevos créditos ({curso.creditos}): ").strip()
            capacidad_str = input(f"Nueva capacidad ({curso.capacidad_maxima}): ").strip()
            semestre = input(f"Nuevo semestre ({curso.semestre}): ").strip()

            datos = {}
            if nombre:
                datos['nombre'] = nombre
            if creditos_str:
                datos['creditos'] = int(creditos_str)
            if capacidad_str:
                datos['capacidad_maxima'] = int(capacidad_str)
            if semestre:
                datos['semestre'] = semestre

            if not datos:
                print("\nNo se realizaron cambios")
                return

            resultado, error = GestorCursos.actualizar_curso(self.session, curso_id, **datos)

            if resultado:
                print(f"\n✓ Curso actualizado exitosamente")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Formato de datos inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Eliminar un curso existente
    # --------------------------------------------------------
    def _eliminar_curso(self):
        print("\n--- ELIMINAR CURSO ---")
        try:
            curso_id = int(input("ID del Curso: "))
            confirmacion = input("¿Está seguro? Esta acción no se puede deshacer (S/N): ").strip().upper()

            if confirmacion != 'S':
                print("Operación cancelada")
                return

            exito, mensaje = GestorCursos.eliminar_curso(self.session, curso_id)

            if exito:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # --------------------------------------------------------
    # Verificar la disponibilidad de cupos en un curso
    # --------------------------------------------------------
    def _verificar_disponibilidad(self):
        print("\n--- VERIFICAR DISPONIBILIDAD ---")
        try:
            curso_id = int(input("ID del Curso: "))
            disponible, mensaje = GestorCursos.verificar_disponibilidad(self.session, curso_id)

            if disponible:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
