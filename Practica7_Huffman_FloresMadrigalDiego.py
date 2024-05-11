import heapq
import os

class NodoHuffman:
    def __init__(self, caracter, frecuencia):
        self.caracter = caracter
        self.frecuencia = frecuencia
        self.izquierda = None
        self.derecha = None

    def __lt__(self, otro):
        return self.frecuencia < otro.frecuencia

class Huffman:
    def __init__(self, texto):
        self.texto = texto
        self.codificacion = {}
        self.arbol = None

    def calcular_frecuencias(self):
        frecuencias = {}
        for caracter in self.texto:
            if caracter in frecuencias:
                frecuencias[caracter] += 1
            else:
                frecuencias[caracter] = 1
        return frecuencias

    def construir_arbol_huffman(self, frecuencias):
        cola = []
        for caracter, frecuencia in frecuencias.items():
            nodo = NodoHuffman(caracter, frecuencia)
            heapq.heappush(cola, nodo)

        while len(cola) > 1:
            izquierda = heapq.heappop(cola)
            derecha = heapq.heappop(cola)
            nuevo_nodo = NodoHuffman(None, izquierda.frecuencia + derecha.frecuencia)
            nuevo_nodo.izquierda = izquierda
            nuevo_nodo.derecha = derecha
            heapq.heappush(cola, nuevo_nodo)

        self.arbol = cola[0]

    def generar_codificacion(self, nodo, codigo_actual):
        if nodo is not None:
            if nodo.caracter is not None:
                self.codificacion[nodo.caracter] = codigo_actual
            self.generar_codificacion(nodo.izquierda, codigo_actual + "0")
            self.generar_codificacion(nodo.derecha, codigo_actual + "1")

    def codificar_texto(self):
        texto_codificado = ""
        for caracter in self.texto:
            texto_codificado += self.codificacion[caracter]
        return texto_codificado

    def decodificar_texto(self, texto_codificado):
        texto_decodificado = ""
        nodo_actual = self.arbol
        for bit in texto_codificado:
            if bit == '0':
                nodo_actual = nodo_actual.izquierda
            else:
                nodo_actual = nodo_actual.derecha
            if nodo_actual.caracter is not None:
                texto_decodificado += nodo_actual.caracter
                nodo_actual = self.arbol
        return texto_decodificado

    def guardar_texto(self, nombre_archivo, texto):
        with open(nombre_archivo, 'w') as archivo:
            archivo.write(texto)

    def ejecutar_codificacion(self):
        frecuencias = self.calcular_frecuencias()
        self.construir_arbol_huffman(frecuencias)
        self.generar_codificacion(self.arbol, "")
        texto_codificado = self.codificar_texto()
        self.guardar_texto('texto_original.txt', self.texto)
        self.guardar_texto('texto_codificado.txt', texto_codificado)
        return texto_codificado

    def ejecutar_decodificacion(self, texto_codificado):
        texto_decodificado = self.decodificar_texto(texto_codificado)
        self.guardar_texto('texto_decodificado.txt', texto_decodificado)
        return texto_decodificado

# Parte 1: Codificación de Huffman
texto_usuario = input("Ingrese el texto a codificar: ")
huffman = Huffman(texto_usuario)
texto_codificado = huffman.ejecutar_codificacion()
print("Texto codificado:", texto_codificado)

# Parte 2: Decodificación Huffman
texto_decodificado = huffman.ejecutar_decodificacion(texto_codificado)
print("Texto decodificado:", texto_decodificado)
