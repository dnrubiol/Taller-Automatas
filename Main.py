##########       DESARROLLADO POR DIEGO RUBIO        ##########
from LecturaArchivo import *
from AFD import *
from AFN import *
from Grafo import *
class Main:

    print()
    print("Escriba el nombre del archivo de texto, finalizando sin la extensión .txt:")
    entrada = input()
    arch = LecturaArchivo(entrada+".txt")
    lectura = arch.LeerArchivo()
    if lectura[0][0] == '#!dfa':
        autoAFD = AFD(lectura)
        print()
        print("Menu AFD:")
        print("1. Procesar Cadena")
        print("2. Procesar Cadena con Detalle")
        print("3. Graficar Automata")
        print("4. Hallar Complemento")
        print("Ingrese el numero de la opción deseada del menu:")
        opcion = input()
        if opcion == "1":
            print("Ingrese la cadena que desea procesar:")
            cad = input()
            if (autoAFD.procesarCadena(cad, "proceCad")) == True:
                print("|La cadena ES aceptada por el automata|")
            else:
                print("|La cadena NO ES aceptada por el automata|")
        elif opcion == "2":
            print("Ingrese la cadena que desea procesar:")
            cad = input()
            print(autoAFD.procesarCadenaConDetalles(cad))
        elif opcion == "3":
            autoAFD.graficarAutomata()
        elif opcion == "4":
            autoAFD.hallarComplemento()
        elif opcion == "5":
            autoAFD.minimizarAutomata()
        else:
            print("¡No ingresó una opcion válida!")

    elif lectura[0][0] == '#!nfa':
        autoAFN = AFN(lectura)
        print()
        print("Menu AFN:")
        print("1. Procesar Cadena")
        print("2. Graficar Automata")
        print("3. Convertir AFN a AFD")
        print("Ingrese el numero de la opción deseada del menu:")
        opcion = input()
        if opcion == "1":
            print("Ingrese la cadena que desea procesar:")
            cad = input()
            if (autoAFN.procesarCadena(cad,"procesarCadena")) == True:
                print("|La cadena ES aceptada por el automata|")
            else:
                print("|La cadena NO ES aceptada por el automata|")
        elif opcion == "2":
            autoAFN.graficarAutomata()
        elif opcion == "3":
            autoAFN.imprimirConversionArchivoTexto()
            archi = LecturaArchivo("ConversionAFNtoAFD.txt")
            lect = archi.LeerArchivo()
            autoAFN.graficarConversionToAFD(lect)
        else:
            print("¡No ingresó una opcion válida!")
