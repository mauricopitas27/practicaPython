# -------------------------------------------------
# ACTIVIDAD 14: Interfaz entre Servidor y Cliente
# -------------------------------------------------

def actividad14_interfaz():
    while True:
        print("\n--- ACTIVIDAD 14: INTERFAZ ---")
        print("Esta interfaz controla las actividades 12 (servidor) y 13 (cliente)")
        print("1. Iniciar Servidor (Actividad 12)")
        print("2. Iniciar Cliente (Actividad 13)")
        print("0. Regresar al menú principal")

        op = input("Selecciona una opción: ")

        if op == '1':
            print("\nIniciando Servidor de Actividad 12...")
            actividad12_servidor()        # Llama al servidor
        elif op == '2':
            print("\nIniciando Cliente de Actividad 13...")
            actividad13_cliente()        # Llama al cliente
        elif op == '0':
            print("Regresando al menú...")
            break
        else:
            print("Opción inválida, intenta de nuevo.")
