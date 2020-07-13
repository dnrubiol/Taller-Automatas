class LecturaArchivo:

    def __init__(self, NombreArchivo):
        self.nombre = NombreArchivo
        self.list = []

    def LeerArchivo(self):
        f = open(self.nombre, 'r')
        mensaje = f.read().splitlines()
        f.close()
        self.list.append(mensaje)
        return self.list

