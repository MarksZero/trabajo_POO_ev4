# ============================================
# main.py
# Punto de entrada principal del sistema
# ============================================

from iu.menu_principal import MenuPrincipal


# --------------------------------------------
# Función principal que inicia el sistema
# --------------------------------------------
def main():
    print("\n" + "=" * 60)
    print("Iniciando Sistema de Matrícula Universitaria...")
    print("=" * 60 + "\n")

    # Crear y ejecutar el menú principal
    menu = MenuPrincipal()
    menu.ejecutar()


# --------------------------------------------
# Ejecución del programa
# --------------------------------------------
if __name__ == "__main__":
    main()
