print("bienvenido al sistema que calcula cualquier tabla de multiplicar")
numero_tabla = int(input("ingrese el numero de la tabla que desea calcular: "))
if(numero_tabla < 1 or numero_tabla > 10):
    print("error: el numero de la tabla debe estar entre 1 y 10")
elif(numero_tabla == 1):
    print("apoco no te la sabes?")
elif(numero_tabla == 7):
    print("la tabla del 7 es la mejor de todas")
else:
    print("tabla de multiplicar del numero", numero_tabla)
    #impresion de la tabla de multiplicar
for i in range(1,11):
    print(numero_tabla,"x" , i , "=", numero_tabla * i)
print("gracias por usar el sistema de tablas de multiplicar")