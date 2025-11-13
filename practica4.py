nombre = []
cantidad = []
precio = []
bandera = "si"
while bandera.lower() == "si":
    n = input("Ingrese el nombre del producto: ")
    p = int(input("Ingrese la cantidad del producto: "))
    pr = float(input("Ingrese el precio del producto: "))
    nombre.append(n)
    cantidad.append(p)
    precio.append(pr)
    bandera = input("¿Desea agregar otro producto? (si/no): ").lower()

    print("============================================================")
    print("=                 super mercado mauri              =")
    print("============================================================")
    print("Producto | Cantidad | Precio Unitario | Total  = ")
    print(" Manzana | 5        | $30.00          | $150.00 ")
    for i in range(len(nombre)):
        print(f"-{nombre[i]:<12}|{cantidad[i]:<10}|{precio[i]:<17}|{cantidad[i]*precio[i]}-")
       