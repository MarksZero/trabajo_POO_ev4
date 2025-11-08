# ============================================
# iu/menu_estudiantes.py
# Menú de gestión de estudiantes
# ============================================

from sqlalchemy.orm import Session
from negocio.gestor_estudiantes import GestorEstudiantes
from auxiliares.formateadores import Formateadores


# --------------------------------------------
# Clase para el menú de gestión de estudiantes
# --------------------------------------------
class MenuEstudiantes:
    # Constructor: recibe la sesión de base de datos
    def __init__(self, session: Session):
        self.session = session

    # ----------------------------------------
    # Muestra el menú de opciones de estudiantes
    # ----------------------------------------
    def mostrar(self):
        while True:
            print(Formateadores.formatear_titulo("GESTIÓN DE ESTUDIANTES"))
            print("1. Registrar Estudiante")
            print("2. Ver Estudiante por ID")
            print("3. Listar Todos los Estudiantes")
            print("4. Listar por Carrera")
            print("5. Actualizar Estudiante")
            print("6. Cambiar Estado")
            print("7. Eliminar Estudiante")
            print("8. Ver Estadísticas por Carrera")
            print("0. Volver")
            print(Formateadores.formatear_separador())

            opcion = input("\nSeleccione una opción: ").strip()

            if opcion == "1":
                self._registrar_estudiante()
            elif opcion == "2":
                self._ver_estudiante()
            elif opcion == "3":
                self._listar_estudiantes()
            elif opcion == "4":
                self._listar_por_carrera()
            elif opcion == "5":
                self._actualizar_estudiante()
            elif opcion == "6":
                self._cambiar_estado()
            elif opcion == "7":
                self._eliminar_estudiante()
            elif opcion == "8":
                self._ver_estadisticas()
            elif opcion == "0":
                break
            else:
                print("✗ Opción inválida")

            if opcion != "0":
                input("\nPresione Enter para continuar...")

    # ----------------------------------------
    # Opción: registrar un nuevo estudiante
    # ----------------------------------------
    def _registrar_estudiante(self):
        print("\n--- REGISTRAR ESTUDIANTE ---")
        try:
            rut = input("RUT: ").strip()
            nombre = input("Nombre: ").strip()
            apellido = input("Apellido: ").strip()
            email = input("Email: ").strip()
            carrera = input("Carrera: ").strip()
            creditos_str = input("Créditos máximos (Enter para 20): ").strip()

            creditos_maximos = int(creditos_str) if creditos_str else None

            estudiante, error = GestorEstudiantes.crear_estudiante(
                self.session, rut, nombre, apellido, email, carrera, creditos_maximos
            )

            if estudiante:
                print(f"\n✓ Estudiante registrado exitosamente")
                print(f"ID: {estudiante.estudiante_id}")
                print(f"Nombre: {estudiante.nombre_completo()}")
                print(f"RUT: {Formateadores.formatear_rut(estudiante.rut)}")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Formato de datos inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: ver información de un estudiante
    # ----------------------------------------
    def _ver_estudiante(self):
        print("\n--- VER ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            estudiante, error = GestorEstudiantes.obtener_estudiante(self.session, estudiante_id)

            if error:
                print(f"\n✗ {error}")
                return

            print(f"\n{Formateadores.formatear_separador()}")
            print(f"ID: {estudiante.estudiante_id}")
            print(f"Nombre: {estudiante.nombre_completo()}")
            print(f"RUT: {Formateadores.formatear_rut(estudiante.rut)}")
            print(f"Email: {estudiante.email}")
            print(f"Carrera: {estudiante.carrera}")
            print(f"Créditos máximos: {estudiante.creditos_maximos}")
            print(f"Estado: {estudiante.estado}")
            print(Formateadores.formatear_separador())

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: listar todos los estudiantes
    # ----------------------------------------
    def _listar_estudiantes(self):
        print("\n--- LISTA DE ESTUDIANTES ---")
        try:
            solo_activos = input("¿Solo estudiantes activos? (S/N): ").strip().upper() == 'S'

            estudiantes = GestorEstudiantes.listar_estudiantes(self.session, solo_activos)

            if not estudiantes:
                print("\nNo hay estudiantes registrados")
                return

            print(f"\nTotal: {len(estudiantes)} estudiante(s)")
            print(Formateadores.formatear_separador())

            for e in estudiantes:
                print(f"\nID {e.estudiante_id}: {e.nombre_completo()}")
                print(f"  RUT: {Formateadores.formatear_rut(e.rut)}")
                print(f"  Carrera: {e.carrera}")
                print(f"  Estado: {e.estado}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: listar estudiantes por carrera
    # ----------------------------------------
    def _listar_por_carrera(self):
        print("\n--- ESTUDIANTES POR CARRERA ---")
        try:
            carrera = input("Carrera: ").strip()

            estudiantes = GestorEstudiantes.listar_por_carrera(self.session, carrera)

            if not estudiantes:
                print(f"\nNo hay estudiantes registrados en la carrera '{carrera}'")
                return

            print(f"\nTotal: {len(estudiantes)} estudiante(s) en {carrera}")
            print(Formateadores.formatear_separador())

            for e in estudiantes:
                print(f"\n• {e.nombre_completo()}")
                print(f"  ID: {e.estudiante_id} | RUT: {Formateadores.formatear_rut(e.rut)}")
                print(f"  Email: {e.email}")

        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: actualizar datos de un estudiante
    # ----------------------------------------
    def _actualizar_estudiante(self):
        print("\n--- ACTUALIZAR ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            estudiante, error = GestorEstudiantes.obtener_estudiante(self.session, estudiante_id)
            if error:
                print(f"\n✗ {error}")
                return

            print(f"\nEstudiante actual: {estudiante.nombre_completo()}")
            print("\nDeje en blanco los campos que no desea modificar")

            email = input(f"Nuevo email ({estudiante.email}): ").strip()
            carrera = input(f"Nueva carrera ({estudiante.carrera}): ").strip()
            creditos_str = input(f"Nuevos créditos máximos ({estudiante.creditos_maximos}): ").strip()

            datos = {}
            if email:
                datos['email'] = email
            if carrera:
                datos['carrera'] = carrera
            if creditos_str:
                datos['creditos_maximos'] = int(creditos_str)

            if not datos:
                print("\nNo se realizaron cambios")
                return

            resultado, error = GestorEstudiantes.actualizar_estudiante(
                self.session, estudiante_id, **datos
            )

            if resultado:
                print(f"\n✓ Estudiante actualizado exitosamente")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Formato de datos inválido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: cambiar el estado de un estudiante
    # ----------------------------------------
    def _cambiar_estado(self):
        print("\n--- CAMBIAR ESTADO ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            print("\nEstados disponibles:")
            print("1. Activo")
            print("2. Inactivo")
            print("3. Egresado")

            opcion = input("\nSeleccione nuevo estado: ").strip()
            estados = {'1': 'Activo', '2': 'Inactivo', '3': 'Egresado'}

            if opcion not in estados:
                print("✗ Opción inválida")
                return

            resultado, error = GestorEstudiantes.cambiar_estado_estudiante(
                self.session, estudiante_id, estados[opcion]
            )

            if resultado:
                print(f"\n✓ Estado cambiado a: {estados[opcion]}")
            else:
                print(f"\n✗ Error: {error}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: eliminar un estudiante
    # ----------------------------------------
    def _eliminar_estudiante(self):
        print("\n--- ELIMINAR ESTUDIANTE ---")
        try:
            estudiante_id = int(input("ID del Estudiante: "))

            confirmacion = input("¿Está seguro? Esta acción no se puede deshacer (S/N): ").strip().upper()

            if confirmacion != 'S':
                print("Operación cancelada")
                return

            exito, mensaje = GestorEstudiantes.eliminar_estudiante(self.session, estudiante_id)

            if exito:
                print(f"\n✓ {mensaje}")
            else:
                print(f"\n✗ {mensaje}")

        except ValueError:
            print("✗ Error: Debe ingresar un número válido")
        except Exception as e:
            print(f"✗ Error: {str(e)}")

    # ----------------------------------------
    # Opción: mostrar estadísticas por carrera
    # ----------------------------------------
    def _ver_estadisticas(self):
        print("\n--- ESTADÍSTICAS POR CARRERA ---")
        try:
            estadisticas = GestorEstudiantes.obtener_estadisticas_carreras(self.session)

            if not estadisticas:
                print("\nNo hay datos para mostrar")
                return

            print(Formateadores.formatear_separador())
            total = sum(cant for _, cant in estadisticas)
            print(f"Total de estudiantes activos: {total}")
            print(Formateadores.formatear_separador())

            for carrera, cantidad in estadisticas:
                porcentaje = (cantidad / total * 100) if total > 0 else 0
                print(f"\n{carrera}")
                print(f"  Estudiantes: {cantidad} ({porcentaje:.1f}%)")

        except Exception as e:
            print(f"✗ Error: {str(e)}")
