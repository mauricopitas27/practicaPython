bandera = True
while bandera:
    numero1 = int(input("Ingrese el primer número: "))
    numero2 = int(input("Ingrese el segundo número: "))
    resultado = numero1 + numero2
    print("El resultado de la suma es:", resultado)
    opcion = input("¿Desea realizar otra suma? (s/n): ")
    if opcion.lower() != 's':
        bandera = False 
        print("Gracias por usar el sistema")