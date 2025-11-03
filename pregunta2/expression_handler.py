# expression_handler.py

class Nodo:
    """
    Clase para representar un nodo en el Arbol de Sintaxis Abstracta (AST).
    Un nodo puede ser un operador (+, -, *, /) o un numero (operando).
    """
    def __init__(self, valor, izquierdo=None, derecho=None):
        self.valor = valor
        self.izquierdo = izquierdo
        self.derecho = derecho

    def __repr__(self):
        return f"Nodo({self.valor}, {self.izquierdo}, {self.derecho})"

def es_operador(token):
    """Verifica si un token es un operador valido."""
    return token in ['+', '-', '*', '/']

# --- Funciones de Parseo (a implementar) ---

def _construir_ast_prefijo_recursivo(tokens, indice_actual):
    if indice_actual >= len(tokens):
        raise ValueError("Expresion prefija invalida: fin inesperado.")
    
    token = tokens[indice_actual]
    indice_actual += 1

    if es_operador(token):
        # Es un operador, construir recursivamente los hijos
        izquierdo, indice_actual = _construir_ast_prefijo_recursivo(tokens, indice_actual)
        derecho, indice_actual = _construir_ast_prefijo_recursivo(tokens, indice_actual)
        return Nodo(token, izquierdo, derecho), indice_actual
    else:
        # Es un numero, crear un nodo hoja
        try:
            valor = int(token)
            return Nodo(valor), indice_actual
        except ValueError:
            raise ValueError(f"Token invalido: '{token}' no es un numero.")

def construir_ast_desde_prefijo(tokens):
    """Construye un AST a partir de una lista de tokens en notacion prefija."""
    if not tokens:
        return None
    
    arbol_completo, tokens_consumidos = _construir_ast_prefijo_recursivo(tokens, 0)
    
    if tokens_consumidos < len(tokens):
        raise ValueError("Expresion prefija invalida: sobran tokens.")
        
    return arbol_completo


def construir_ast_desde_postfijo(tokens):
    """Construye un AST a partir de una lista de tokens en notacion postfija."""
    pila = []
    for token in tokens:
        if es_operador(token):
            if len(pila) < 2:
                raise ValueError("Expresion postfija invalida: faltan operandos.")
            derecho = pila.pop()
            izquierdo = pila.pop()
            nodo = Nodo(token, izquierdo, derecho)
            pila.append(nodo)
        else:
            try:
                # Los operandos deben ser numeros enteros
                nodo = Nodo(int(token))
                pila.append(nodo)
            except ValueError:
                raise ValueError(f"Token invalido: '{token}' no es un numero.")
    
    if len(pila) != 1:
        raise ValueError("Expresion postfija invalida: sobran operandos.")
    
    return pila[0]

# --- Funciones de Accion  ---

def evaluar_ast(arbol):
    """Evalua el AST y devuelve el resultado numerico."""
    if arbol is None:
        return 0
    
    # Si el nodo es una hoja, es un numero
    if arbol.izquierdo is None and arbol.derecho is None:
        return arbol.valor

    # Evaluar recursivamente los hijos
    valor_izquierdo = evaluar_ast(arbol.izquierdo)
    valor_derecho = evaluar_ast(arbol.derecho)

    # Realizar la operacion
    if arbol.valor == '+':
        return valor_izquierdo + valor_derecho
    elif arbol.valor == '-':
        return valor_izquierdo - valor_derecho
    elif arbol.valor == '*':
        return valor_izquierdo * valor_derecho
    elif arbol.valor == '/':
        if valor_derecho == 0:
            raise ValueError("Division por cero.")
        # Usamos division entera como se especifica
        return valor_izquierdo // valor_derecho
    else:
        raise ValueError(f"Operador desconocido: {arbol.valor}")

def _get_precedencia(operador):
    if operador in ['+', '-']:
        return 1
    if operador in ['*', '/']:
        return 2
    return 0 # Para los numeros

def _mostrar_infijo_recursivo(arbol, precedencia_padre=0):
    if arbol is None:
        return ""
    
    if es_operador(arbol.valor):
        precedencia_actual = _get_precedencia(arbol.valor)
        
        # Procesar sub-arbol izquierdo
        expr_izquierda = _mostrar_infijo_recursivo(arbol.izquierdo, precedencia_actual)
        
        # Procesar sub-arbol derecho
        # Para operadores con igual precedencia, anadimos parentesis en el lado derecho
        # si asocian por la izquierda 
        precedencia_derecha = precedencia_actual + 1 if arbol.valor in ['-', '/'] else precedencia_actual
        expr_derecha = _mostrar_infijo_recursivo(arbol.derecho, precedencia_derecha)

        expresion = f"{expr_izquierda} {arbol.valor} {expr_derecha}"
        
        if precedencia_actual < precedencia_padre:
            return f"({expresion})"
        return expresion
    else:
        # Es un operando
        return str(arbol.valor)

def mostrar_infijo(arbol):
    """Convierte el AST a una cadena en notacion infija con parentesis minimos."""
    return _mostrar_infijo_recursivo(arbol)


# --- Bucle Principal del Programa ---

def main():
    """Bucle principal que maneja la interaccion con el usuario."""
    print("Calculadora de Expresiones Aritmeticas")
    print("Comandos disponibles: EVAL, MOSTRAR, SALIR")

    while True:
        try:
            entrada = input("> ").strip().split()
            if not entrada:
                continue

            comando = entrada[0].upper()

            if comando == "SALIR":
                break
            elif comando in ["EVAL", "MOSTRAR"]:
                if len(entrada) < 3:
                    print("Error: Faltan argumentos para el comando.")
                    continue

                orden = entrada[1].upper()
                expr_tokens = entrada[2:]

                if orden not in ["PRE", "POST"]:
                    print(f"Error: Orden '{orden}' no reconocido. Use PRE o POST.")
                    continue

                arbol = None
                try:
                    if orden == "PRE":
                        arbol = construir_ast_desde_prefijo(expr_tokens)
                    elif orden == "POST":
                        arbol = construir_ast_desde_postfijo(expr_tokens)
                except ValueError as e:
                    print(f"Error de expresion: {e}")
                    continue

                if arbol:
                    if comando == "EVAL":
                        try:
                            resultado = evaluar_ast(arbol)
                            print(resultado)
                        except ValueError as e:
                            print(f"Error de evaluacion: {e}")
                    elif comando == "MOSTRAR":
                        resultado_infijo = mostrar_infijo(arbol)
                        print(resultado_infijo)
            else:
                print(f"Error: Comando '{comando}' no reconocido.")

        except Exception as e:
            print(f"Ocurrio un error inesperado: {e}")

if __name__ == "__main__":
    main()
