lista_frutas =[]
bandera = "si"
while bandera.lower() == "si":
    n = input("Ingrese el nombre del producto: ")
    p = int(input("Ingrese la cantidad del producto: "))
    pr = float(input("Ingrese el precio del producto: "))
    fruta = {
        "nombre": n,
        "precio": p,
        "cantidad": pr
    }
    lista_frutas.append(fruta)
    bandera = input("¿Desea agregar otro producto? (si/no): ").lower()

    print("============================================================")
    print("=                 super mercado mamauri              =")
    print("============================================================")
    print("Producto | Cantidad | Precio Unitario | Total  = ")
    print(" Manzana | 5        | $30.00          | $150.00 ")
    for i in lista_frutas:
        print(f"-{fruta ['nombre']:<12}|{fruta['cantidad']:<10}|{fruta['precio']:<17}|{fruta['cantidad']* fruta['precio']:<11}-")
       