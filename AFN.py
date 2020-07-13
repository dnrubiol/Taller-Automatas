from graphviz import Digraph
from LecturaArchivo import *
from Grafo import *
class AFN:

    def __init__(self, cadena):
        self.Sigma = []         ##  Alfabeto
        self.Q = []             ##  Conjunto de estados
        self.q0 = []            ##  Estado inicial
        self.F = []             ##  Estados de aceptacion
        self.Delta = []         ##  Funcion de transicion

        self.cad = cadena
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
        grafo = Grafo(self.Q, self.Sigma, self.Delta, "AFN")
        alfa = grafo.auxAlfabeto
        est = grafo.auxEstados
        tran = grafo.auxtransi
        ax = [self.q0[1]]
        tranTemp = []
        estTemp = [ax]
        aceptTemp = []
        for z in range(1, len(self.F)):
            aceptTemp.append([self.F[z]])
   ########     trabajar el AFN como AFD    ##########
        for i in range(0, len(alfa)):
            if tran[i] != [None]:
                tranTemp.append(tran[i])
                if tran[i] not in estTemp:
                    estTemp.append(tran[i])
                    for w in range(1, len(self.F)):
                        if self.F[w] in tran[i] and tran[i] not in aceptTemp:
                            aceptTemp.append(tran[i])
            else:
                tranTemp.append([None])
        bandera = False
        while bandera == False:
            aux = estTemp[len(estTemp)-1]
            construc = []
            for k in range(len(alfa)):
                construc.append([])
            for i in range(len(aux)):
                for j in range(len(alfa)):
                    a = tran[est.index(aux[i]) + (j + (est.index(aux[i]) * (len(alfa)-1)))]
                    if a not in construc[j]:
                        construc[j].append(a)
            count = 0
            for l in range(len(construc)):
                mat = []
                for m in range(len(construc[l])):
                    for n in range(len(construc[l][m])):
                        if construc[l][m][n] not in mat and construc[l][m][n] != None:
                            mat.append(construc[l][m][n])
                mat.sort()
                if mat != []:
                    tranTemp.append(mat)
                else:
                    tranTemp.append([None])
                if mat not in estTemp and mat != []:
                    estTemp.append(mat)
                    for w in range(1, len(self.F)):
                        if self.F[w] in mat and mat not in aceptTemp:
                            aceptTemp.append(mat)
                else:
                    count += 1

                if count == len(alfa):
                    bandera = True
        bandera = False
        for y in range(len(cadena)):
            indest = estTemp.index(ax)
            indalfa = alfa.index(cadena[y])
            if tranTemp[estTemp.index(ax) + (indalfa + (indest * (len(alfa) - 1)))] != None:
                bandera = True
                ax = tranTemp[estTemp.index(ax) + (indalfa + (indest * (len(alfa) - 1)))]
            else:
                bandera = False
                break
        if operacion == "procesarCadena":
            if bandera == True and ax in aceptTemp:
                return True
            else:
                return False
        elif operacion == "retornartranTemp":
            return tranTemp
        elif operacion == "retornarestTemp":
            return estTemp
        elif operacion == "retornaraceptTemp":
            return aceptTemp

    def graficarAutomata(self, nombreArchivo='automataAFN'):
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

    def imprimirConversionArchivoTexto(self):
        ##self.Sigma
        ##self.q0
        varQinit = self.procesarCadena(str(self.Sigma[1]), "retornarestTemp")
        varFinit = self.procesarCadena(str(self.Sigma[1]), "retornaraceptTemp")
        varDeltainit = self.procesarCadena(str(self.Sigma[1]), "retornartranTemp")
        varQ = "#states;"
        varF = "#accepting;"
        varDelta = "#transitions;"
        cade = ""
        for i in range(len(varQinit)):
            for j in range(len(varQinit[i])):
                if cade != "" and j != 0:
                    cade += ","+str(varQinit[i][j])
                else:
                    cade += str(varQinit[i][j])
            cade += ";"
            for k in range(1, len(self.Sigma)):
                aux = []
                cade2 = ""
                if varDeltainit[varQinit.index([self.q0[1]]) + ((k-1) + (i * (len(self.Sigma) - 1)))] != [None]:
                    aux.append(varQinit[i])
                    aux.append(":")
                    aux.append([self.Sigma[k]])
                    aux.append(">")
                    aux.append(varDeltainit[varQinit.index([self.q0[1]]) + ((k-1) + (i * (len(self.Sigma) - 1)))])
                    aux.append(";")
                    for m in range(len(aux)):
                        for n in range(len(aux[m])):
                            if n == 0:
                                cade2 += str(aux[m][n])
                            else:
                                cade2 += ","+str(aux[m][n])
                    varDelta += cade2
        varQ += cade
        cadee = ""
        for i in range(len(varFinit)):
            for j in range(len(varFinit[i])):
                if cadee != "" and j != 0:
                    cadee += "," + str(varFinit[i][j])
                else:
                    cadee += str(varFinit[i][j])
            cadee += ";"
        varF += cadee
        varQ = varQ.split(";")
        varF = varF.split(";")
        varDelta = varDelta.split(";")
        f = open("ConversionAFNtoAFD.txt", "w")
        f.write("#!dfa\n")
        for a in range(len(self.Sigma)):
            if a == 0:
                f.write(str(self.Sigma[a])+"\n")
            else:
                if a == (len(self.Sigma)-1):
                    f.write(str(self.Sigma[a]) + "\n")
                else:
                    f.write(str(self.Sigma[a]) + "-")
        for b in range(len(varQ)-1):
            f.write(str(varQ[b]) + "\n")
        for c in range(len(self.q0)):
            f.write(str(self.q0[c]) + "\n")
        for d in range(len(varF)-1):
            f.write(str(varF[d]) + "\n")
        for e in range(len(varDelta)-1):
            f.write(str(varDelta[e]) + "\n")
        f.close()
        print("La 'Conversion AFN to AFD' ha sido guardada como archivo de texto")

    def graficarConversionToAFD(self, lect, nombreArchivo='AFNtoAFD'):
        grafo2 = AFN(lect)
        selSigma = grafo2.Sigma
        selQ0 = grafo2.q0
        selQ = grafo2.Q
        sellF = grafo2.F
        selDelta = grafo2.Delta
        dicc = {}
        listaLlaves = []

        dot = Digraph(comment='automata')
        dot.format = 'png'
        for i in range(1, len(selQ)):
            if (selQ[i] in sellF):
                dot.node(selQ[i], shape='doublecircle')
            else:
                dot.node(selQ[i])
        for i in range(1, len(selDelta)):
            pString = selDelta[i]
            pStringList = re.split(':|>|;', pString)
            for j in range(2, len(pStringList)):
                idDicc = pStringList[0] + ';' + pStringList[j]
                estaDiccionario = dicc.get(idDicc, 'no esta')
                if (estaDiccionario == 'no esta'):
                    listaLlaves.append(idDicc)
                    dicc[idDicc] = pStringList[1]
                else:
                    auxConca = dicc.get(idDicc, 'noo esta')
                    dicc[idDicc] = auxConca + ',' + pStringList[1]

        for i in listaLlaves:
            ppf = i.split(';')
            dot.edge(ppf[0], ppf[1], label=dicc[i])

        dot.render('Graficas/' + nombreArchivo, view=True)


