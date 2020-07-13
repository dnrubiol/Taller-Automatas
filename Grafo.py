import re

class Grafo:

    def __init__(self, Q, sigma, delta, typeAutom):
        self.estados = Q
        self.alfabeto = sigma
        self.transiciones = delta
        self.auxtransi = []
        self.auxEstados = []
        self.auxAlfabeto = []
        self.type = typeAutom

        for i in range(1, len(self.estados)):
            self.auxEstados.append(self.estados[i])
        for h in range(1, len(self.alfabeto)):
            self.auxAlfabeto.append(self.alfabeto[h])
        for l in range(len(self.auxEstados)*len(self.auxAlfabeto)):
            self.auxtransi.append(None)
        if self.type == "AFD":
            aux = []
            for m in range(1, len(self.transiciones)):
                aux = str(self.transiciones[m]).replace(">", ":").split(":")
                indEstados = self.auxEstados.index(aux[0])
                indAlfabeto = self.auxAlfabeto.index(aux[1])
                self.auxtransi[indEstados + (indAlfabeto + (indEstados * (len(self.auxAlfabeto) - 1)))] = aux[2]
        else:
            aux = []
            for m in range(1, len(self.transiciones)):
                aux = str(self.transiciones[m]).replace(">", ":").split(":")
                indEstados = self.auxEstados.index(aux[0])
                indAlfabeto = self.auxAlfabeto.index(aux[1])
                if len(aux[2]) > 2:
                    self.auxtransi[indEstados + (indAlfabeto + (indEstados * (len(self.auxAlfabeto) - 1)))] = aux[2].split(";")
                    self.auxtransi[indEstados + (indAlfabeto + (indEstados * (len(self.auxAlfabeto) - 1)))].sort()
                else:
                    self.auxtransi[indEstados + (indAlfabeto + (indEstados * (len(self.auxAlfabeto) - 1)))] = [aux[2]]
            for n in range (0,len(self.auxtransi)):
                if self.auxtransi[n] == None:
                    self.auxtransi[n] = [None]

    def retornarAutom(self):
        return self.auxtransi

    def retornarEstados(self):
        return self.auxEstados

    def retornarAlfabeto(self):
        return self.auxAlfabeto






