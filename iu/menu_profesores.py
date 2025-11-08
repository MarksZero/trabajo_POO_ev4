# ============================================
# iu/menu_profesores.py
# Menú de gestión de profesores
# ============================================

from sqlalchemy.orm import Session
from negocio.gestor_profesores import GestorProfesores
from auxiliares.formateadores import Formateadores


# --------------------------------------------
# Clase para el menú de gestión de profesores
# --------------------------------------------
class MenuProfesores:
    # Constructor: recibe la sesión de base de datos
    def __init__(self, session: Session):
        self.session = session

    # ----------------------------------------
    # Muestra el menú de opciones de profesores
    # ----------------------------------------
    def mostrar(self):
        while True:
            print(Formateadores.formatear_titulo("GESTIÓN DE PROFESORES"))
            print("1. Registrar Profesor")
            print("2. Ver Profesor por ID")
            print("3. Listar Todos los Profesores")
            print("4. Ver Cursos de Profesor")
            print("5. Actualizar Profesor")
            print("6. Eliminar Profesor")
            print("7. Verificar Carga Académica")
            print("0. Volver")
            print(Formateadores.formatear_separador())

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._registrar_profesor()
            elif opcion == "2":
                self._ver_profesor()
            elif opcion == "3":
                self._listar_profesores()
            elif opcion == "4":
                self._ver_cursos_profesor()
            elif opcion == "5":
                self._actualizar_profesor()
            elif opcion == "6":
                self._eliminar_profesor()
            elif opcion == "7":
                self._verificar_carga()
            elif opcion == "0":
                break
            else:
                print("✗ Opción inválida")

            if opcion != "0":
                input("\nPresione Enter para continuar...")

    # ----------------------------------------
    # Opción: registrar un nuevo profesor
    # ----------------------------------------
    def _registrar_profesor(self):
        print("\n--- REGISTRAR PROFESOR ---")
        try:
            rut = input("RUT: ").strip()
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()

            profesor, error = GestorProfesores.crear_profesor(
                self.session, rut, nombre, apellido, email
            )

            if profesor:
                print(f"\n✓ Profesor registrado exitosamente")
                print(f"ID: {profesor.profesor_id}")
                print(f"Nombre: {profesor.nombre_completo()}")
                print(f"RUT: {Formateadores.formatear_rut(profesor.rut)}")
            else:
                print(f"\n✗ Error: {error}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver información de un profesor
    # ----------------------------------------
    def _ver_profesor(self):
        print("\n--- VER PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            profesor, error = GestorProfesores.obtener_profesor(self.session, profesor_id)

            if error:
                print(f"\n✗ {error}")
                return

            print(f"\n{Formateadores.formatear_separador()}")
            print(f"ID: {profesor.profesor_id}")
            print(f"Nombre: {profesor.nombre_completo()}")
            print(f"RUT: {Formateadores.formatear_rut(profesor.rut)}")
            print(f"Email: {profesor.email}")
            print(f"Estado: {profesor.estado}")
            print(Formateadores.formatear_separador())

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: listar todos los profesores
    # ----------------------------------------
    def _listar_profesores(self):
        print("\n--- LISTA DE PROFESORES ---")
        try:
            solo_activos = input("¿Solo profesores activos? (S/N): ").strip().upper() == 'S'

            profesores = GestorProfesores.listar_profesores(self.session, solo_activos)

            if not profesores:
                print("\nNo hay profesores registrados")
                return

            print(f"\nTotal: {len(profesores)} profesor(es)")
            print(Formateadores.formatear_separador())

            from datos.profesor_dao import ProfesorDAO

            for p in profesores:
                cantidad_cursos = ProfesorDAO.contar_cursos(self.session, p.profesor_id)
                print(f"\nID {p.profesor_id}: {p.nombre_completo()}")
                print(f"  RUT: {Formateadores.formatear_rut(p.rut)}")
                print(f"  Email: {p.email}")
                print(f"  Cursos: {cantidad_cursos}")
                print(f"  Estado: {p.estado}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver cursos de un profesor
    # ----------------------------------------
    def _ver_cursos_profesor(self):
        print("\n--- CURSOS DEL PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            cursos, error = GestorProfesores.obtener_cursos_profesor(self.session, profesor_id)

            if error:
                print(f"\n✗ {error}")
                return

            if not cursos:
                print("\nEl profesor no tiene cursos asignados")
                return

            from datos.curso_dao import CursoDAO

            print(f"\nTotal de cursos: {len(cursos)}")
            print(Formateadores.formatear_separador())

            for c in cursos:
                inscritos = CursoDAO.contar_estudiantes_inscritos(self.session, c.curso_id)
                print(f"\n• {c.codigo} - {c.nombre}")
                print(f"  Créditos: {c.creditos}")
                print(f"  Estudiantes: {inscritos}/{c.capacidad_maxima}")
                print(f"  Semestre: {c.semestre}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: actualizar datos de un profesor
    # ----------------------------------------
    def _actualizar_profesor(self):
        print("\n--- ACTUALIZAR PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            profesor, error = GestorProfesores.obtener_profesor(self.session, profesor_id)
            if error:
                print(f"\n✗ {error}")
                return

            print(f"\nProfesor actual: {profesor.nombre_completo()}")
            print("\nDeje en blanco los campos que no desea modificar")

            email = input(f"Nuevo email ({profesor.email}): ").strip()

            datos = {}
            if email:
                datos['email'] = email

            if not datos:
                print("\nNo se realizaron cambios")
                return

            resultado, error = GestorProfesores.actualizar_profesor(
                self.session, profesor_id, **datos
            )

            if resultado:
                print(f"\n✓ Profesor actualizado exitosamente")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Formato de datos inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: eliminar un profesor
    # ----------------------------------------
    def _eliminar_profesor(self):
        print("\n--- ELIMINAR PROFESOR ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            confirmacion = input("¿Está seguro? Esta acción no se puede deshacer (S/N): ").strip().upper()

            if confirmacion != 'S':
                print("Operación cancelada")
                return

            exito, mensaje = GestorProfesores.eliminar_profesor(self.session, profesor_id)

            if exito:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: verificar carga académica del profesor
    # ----------------------------------------
    def _verificar_carga(self):
        print("\n--- VERIFICAR CARGA ACADÉMICA ---")
        try:
            profesor_id = int(input("ID del Profesor: "))

            puede, mensaje = GestorProfesores.validar_carga_academica(self.session, profesor_id)

            if puede:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")
