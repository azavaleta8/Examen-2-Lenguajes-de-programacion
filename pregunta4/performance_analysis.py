# pregunta4/performance_analysis.py

import timeit
import matplotlib.pyplot as plt
from recursive_functions import f_recursiva_directa, f_recursiva_cola, f_iterativa

# Hacemos las funciones visibles globalmente para que timeit las encuentre
__all__ = ['f_recursiva_directa', 'f_recursiva_cola', 'f_iterativa']

def medir_tiempo(func_name, n):
    """Mide el tiempo de ejecucion de una funcion para un n dado."""
    setup_code = f"from recursive_functions import {func_name}"
    stmt_code = f"{func_name}({n})"
    
    numero_de_ejecuciones = 100
    tiempo = timeit.timeit(stmt=stmt_code, setup=setup_code, number=numero_de_ejecuciones)
    return tiempo / numero_de_ejecuciones

def analizar_rendimiento():
    """Ejecuta el analisis de rendimiento y genera el grafico."""
    valores_n = range(20, 35)
    tiempos_directa = []
    tiempos_cola = []
    tiempos_iterativa = []

    print("Iniciando analisis de rendimiento (esto puede tardar un momento)...")
    for n in valores_n:
        print(f"Calculando para n = {n}...")
        tiempos_directa.append(medir_tiempo('f_recursiva_directa', n))
        tiempos_cola.append(medir_tiempo('f_recursiva_cola', n))
        tiempos_iterativa.append(medir_tiempo('f_iterativa', n))

    # Generar el grafico
    plt.figure(figsize=(12, 7))
    plt.plot(valores_n, tiempos_directa, 'o-', label='Recursiva Directa (con cache)')
    plt.plot(valores_n, tiempos_cola, 's-', label='Recursiva de Cola (Simulada)')
    plt.plot(valores_n, tiempos_iterativa, '^-', label='Iterativa')
    
    plt.xlabel('Valor de n')
    plt.ylabel('Tiempo de Ejecucion Promedio (segundos)')
    plt.title('Comparacion de Rendimiento de Implementaciones Recursivas vs. Iterativa')
    plt.legend()
    plt.grid(True)
    
    nombre_archivo = 'performance_comparison.png'
    plt.savefig(nombre_archivo)
    print(f"\nAnalisis completado. Grafico guardado como '{nombre_archivo}'")

if __name__ == "__main__":
    analizar_rendimiento()
