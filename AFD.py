from graphviz import Digraph
from LecturaArchivo import *
from Grafo import *
class AFD:

    def __init__(self, cadena):
        self.Sigma = []         ##  Alfabeto
        self.Q = []             ##  Conjunto de estados
        self.q0 = []            ##  Estado inicial
        self.F = []             ##  Estados de aceptacion
        self.Delta = []         ##  Funcion de transicion

        self.cad = cadena
        self.cad2 = self.cad
        self.cad[0].pop(0)
        while self.cad[0][0] != '#states':
            if self.cad[0][0] == '#alphabet':
                self.Sigma.append(self.cad[0][0])
                self.cad[0].pop(0)
            else:
                aux = []
                aux.append(self.cad[0][0].split("-"))
                for f in range(0, len(aux[0])):
                    self.Sigma.append(aux[0][f])
                self.cad[0].pop(0)
        while self.cad[0][0] != '#initial':
            self.Q.append(self.cad[0][0])
            self.cad[0].pop(0)
        while self.cad[0][0] != '#accepting':
            self.q0.append(self.cad[0][0])
            self.cad[0].pop(0)
        while self.cad[0][0] != '#transitions':
            self.F.append(self.cad[0][0])
            self.cad[0].pop(0)
        while len(self.cad[0]) > 0:
            self.Delta.append(self.cad[0][0])
            self.cad[0].pop(0)

    def procesarCadena(self, cadena, operacion):
        grafo = Grafo(self.Q, self.Sigma, self.Delta, "AFD")
        alfa = grafo.auxAlfabeto
        est = grafo.auxEstados
        tran = grafo.auxtransi
        ax = self.q0[1]
        bandera = False
        for i in range(len(cadena)):
            indest = est.index(ax)
            indalfa = alfa.index(cadena[i])
            if tran[est.index(ax) + (indalfa + (indest * (len(alfa)-1)))] != None:
                bandera = True
                ax = tran[est.index(ax) + (indalfa + (indest * (len(alfa)-1)))]
            else:
                bandera = False
                break
        if operacion == "proceCad":
            if bandera == True and ax in self.F:
                return True
            else:
                return False
        elif operacion == "returnTran":
            return tran
        elif operacion == "returnAlfa":
            return alfa
        elif operacion == "returnEst":
            return est

    def procesarCadenaConDetalles(self, cadena):
        grafo = Grafo(self.Q, self.Sigma, self.Delta, "AFD")
        alfa = grafo.auxAlfabeto
        est = grafo.auxEstados
        tran = grafo.auxtransi
        ax = self.q0[1]
        bandera = False
        estadosRecorridos = str(self.q0[1])
        for i in range(len(cadena)):
            indest = est.index(ax)
            indalfa = alfa.index(cadena[i])
            if tran[est.index(ax) + (indalfa + (indest * (len(alfa)-1)))] != None:
                bandera = True
                ax = tran[est.index(ax) + (indalfa + (indest * (len(alfa)-1)))]
                estadosRecorridos += (" -> "+str(ax))
            else:
                estadosRecorridos += " -> ?? "
                bandera = False
                break
        if bandera == True and ax in self.F:
            estadosRecorridos += "      |CADENA ACEPTADA| "
            return estadosRecorridos
        else:
            estadosRecorridos += "      |CADENA NO ACEPTADA| "
            return estadosRecorridos

    def graficarAutomata(self, nombreArchivo='automataAFD'):
        diccionario = {}
        listaKeys = []
        dot = Digraph(comment='automata')
        dot.format = 'png'
        for i in range(1, len(self.Q)):
            if (self.Q[i] in self.F):
                dot.node(self.Q[i], shape='doublecircle')
            else:
                dot.node(self.Q[i])
        for i in range(1, len(self.Delta)):
            pruebaString = self.Delta[i]
            pruebaStringList = re.split(':|>|;', pruebaString)
            for j in range(2, len(pruebaStringList)):
                idDiccionario = pruebaStringList[0] + ';' + pruebaStringList[j]
                estaIDDiccionario = diccionario.get(idDiccionario, 'no esta')
                if (estaIDDiccionario == 'no esta'):
                    listaKeys.append(idDiccionario)
                    diccionario[idDiccionario] = pruebaStringList[1]
                else:
                    auxConcatenacion = diccionario.get(idDiccionario, 'noo esta')
                    diccionario[idDiccionario] = auxConcatenacion + ',' + pruebaStringList[1]

        for i in listaKeys:
            pipf = i.split(';')
            dot.edge(pipf[0], pipf[1], label=diccionario[i])

        dot.render('Graficas/' + nombreArchivo, view=True)

    def hallarComplemento(self):
        acep = self.F
        tochan = self.Q
        nuevosAceptacion = ["#accepting"]
        for k in range(1, len(acep)):
            for m in range(1, len(tochan)):
                if acep[k] != tochan[m]:
                    nuevosAceptacion.append(tochan[m])
        file = open("ComplementoAFD.txt", "w")
        file.write("#!DFA" + '\n')
        file.write(self.Sigma[0] + '\n')
        for k in range(1, (len(self.Sigma) - 1)):
            file.write(self.Sigma[k] + "-")
        file.write(self.Sigma[len(self.Sigma) - 1] + '\n')
        for l in range(0, len(self.Q)):
            file.write(self.Q[l] + '\n')
        for m in range(0, len(self.q0)):
            file.write(self.q0[m] + '\n')
        file.write(self.F[0] + '\n')
        for n in range(1, len(nuevosAceptacion)):
            file.write(nuevosAceptacion[n] + '\n')
        for o in range(0, len(self.Delta)):
            file.write(self.Delta[o] + '\n')
        file.close()
        print("El 'Complemento AFD' ha sido guardado como archivo de texto")

    def minimizarAutomata(self):
        print(self.Sigma[1])        ########################3
        estados = self.procesarCadena(str(self.Sigma[1]), "returnEst")
        alfa = self.procesarCadena(str(self.Sigma[1]), "returnAlfa")
        transi = self.procesarCadena(str(self.Sigma[1]), "returnTran")
        print(estados)          ########################
        print(alfa)         ######################3
        print(transi)           ######################
        aux = []
        equivalentes = []
        print(transi)       ####################33
        for i in range(0, len(estados)):
            for j in range(0, len(estados)):
                if estados[i] != estados[j]:
                    if ((estados[i] in self.F and estados[j] in self.F) or (estados[i] not in self.F and estados[j] not in self.F)):
                        count = 0
                        aux = [estados[i], estados[j]]
                        aux.sort()
                        print(aux)          ##############
                        for k in range(1, len(self.Sigma)):
                            a = transi[(k-1) + (i*(len(alfa)-1))]
                            b = transi[(k-1) + (j*(len(alfa)-1))]
                            if a in self.F and b in self.F:
                                count += 1
                            elif a not in self.F and b not in self.F:
                                count += 1
                            print((a in self.F))
                            print((b in self.F))
                            print((a not in self.F))
                            print((b not in self.F))
                        if aux not in equivalentes and count == 2:
                            equivalentes.append(aux)
                            print("Agregado")       ########################
                        aux = []
        print(equivalentes)  ##############
