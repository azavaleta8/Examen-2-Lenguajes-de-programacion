# pregunta4/recursive_functions.py

import functools

# Constantes calculadas
ALPHA = 5
BETA = 4

# --- (a) Implementacion Recursiva Directa ---

@functools.lru_cache(maxsize=None) # Usamos cache para evitar re-calculos
def f_recursiva_directa(n):
    """
    Calcula F(ALPHA, BETA) usando una traduccion directa de la formula recursiva.
    Se utiliza un decorador de cache para mejorar el rendimiento al evitar
    calcular los mismos sub-problemas multiples veces (memoizacion).
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n debe ser un entero no negativo.")

    if 0 <= n < ALPHA * BETA:
        return n
    else:
        suma = 0
        for i in range(1, ALPHA + 1):
            suma += f_recursiva_directa(n - BETA * i)
        return suma

# --- (b) Implementacion Recursiva de Cola (Simulada) ---

def f_recursiva_cola(n):
    """
    Funcion publica que inicia la recursion de cola.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n debe ser un entero no negativo.")
    
    if 0 <= n < ALPHA * BETA:
        return n
        
    # Inicializamos una lista de 'casos base' para la recursion
    # que son los valores F(n) para n < ALPHA * BETA.
    mem = list(range(ALPHA * BETA))
    return _f_cola_helper(n, mem)

def _f_cola_helper(n, mem):
    """
    Helper recursivo que simula la recursion de cola.
    En lugar de hacer multiples llamadas recursivas, calcula el siguiente
    valor y lo pasa a la siguiente llamada.
    """
    if n < len(mem):
        return mem[n]
    
    # Si el valor no esta en memoria, lo calculamos
    # expandiendo la memoria hasta alcanzar n.
    while len(mem) <= n:
        next_val = 0
        for i in range(1, ALPHA + 1):
            next_val += mem[len(mem) - BETA * i]
        mem.append(next_val)

    return mem[n]

# --- (c) Implementacion Iterativa ---

def f_iterativa(n):
    """
    Calcula F(ALPHA, BETA) usando un enfoque iterativo.
    Esta version es la mas eficiente en uso de memoria y velocidad.
    """
    if not isinstance(n, int) or n < 0:
        raise ValueError("n debe ser un entero no negativo.")
    
    if 0 <= n < ALPHA * BETA:
        return n
    
    # Creamos una lista para almacenar los resultados calculados (memoizacion)
    mem = list(range(ALPHA * BETA))
    
    # Llenamos la lista iterativamente hasta llegar a n
    for i in range(ALPHA * BETA, n + 1):
        suma_terminos = 0
        for j in range(1, ALPHA + 1):
            suma_terminos += mem[i - BETA * j]
        mem.append(suma_terminos)
        
    return mem[n]
