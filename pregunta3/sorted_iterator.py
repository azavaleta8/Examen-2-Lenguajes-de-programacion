# pregunta3/sorted_iterator.py

import heapq

def iterador_ordenado(lista_desordenada):
    """
    Iterador que devuelve los elementos de una lista en orden (de menor a mayor)
    sin ordenar la lista de antemano.

    Utiliza un min-heap para extraer eficientemente el elemento mas pequeno
    en cada paso.
    """
    # Crear una copia para no modificar la lista original
    heap = list(lista_desordenada)
    heapq.heapify(heap)  # Convierte la lista en un min-heap en O(n)

    # Mientras el heap no este vacio, extraer y devolver el minimo
    while heap:
        yield heapq.heappop(heap)

def main():
    """Funcion principal para probar el iterador."""
    lista = [1, 3, 3, 2, 1]
    print(f"Lista original: {lista}")

    print("Elementos producidos por el iterador:")
    resultado = []
    for elemento in iterador_ordenado(lista):
        print(elemento, end=' ')
        resultado.append(elemento)
    print("\n")

    lista_ordenada_nativa = sorted(lista)
    print(f"Lista ordenada con sorted(): {lista_ordenada_nativa}")
    assert resultado == lista_ordenada_nativa
    print("Verificacion exitosa: el iterador produjo la secuencia correcta.")

if __name__ == "__main__":
    main()
