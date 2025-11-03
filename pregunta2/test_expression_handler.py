# test_expression_handler.py

import unittest
from unittest.mock import patch
from io import StringIO
import sys

from expression_handler import (
    main,
    Nodo, 
    es_operador,
    construir_ast_desde_postfijo,
    evaluar_ast,
    mostrar_infijo,
    construir_ast_desde_prefijo
)

class TestExpressionHandler(unittest.TestCase):

    def test_es_operador(self):
        """Prueba la funcion de utilidad es_operador."""
        self.assertTrue(es_operador('+'))
        self.assertTrue(es_operador('-'))
        self.assertTrue(es_operador('*'))
        self.assertTrue(es_operador('/'))
        self.assertFalse(es_operador('5'))
        self.assertFalse(es_operador('a'))

    # --- Pruebas para las funciones de parseo ---

    def test_construir_ast_desde_prefijo_simple(self):
        """Prueba una expresion prefija simple."""
        tokens = "+ 3 4".split()
        arbol = construir_ast_desde_prefijo(tokens)
        self.assertEqual(arbol.valor, '+')
        self.assertEqual(arbol.izquierdo.valor, 3)
        self.assertEqual(arbol.derecho.valor, 4)

    def test_construir_ast_desde_prefijo_compleja(self):
        """Prueba la expresion prefija compleja del enunciado."""
        tokens = "+ * + 3 4 5 7".split()
        arbol = construir_ast_desde_prefijo(tokens)
        # Raiz debe ser '+'
        self.assertEqual(arbol.valor, '+')
        # Hijo derecho debe ser '7'
        self.assertEqual(arbol.derecho.valor, 7)
        # Hijo izquierdo debe ser '* + 3 4 5'
        sub_arbol_izq = arbol.izquierdo
        self.assertEqual(sub_arbol_izq.valor, '*')
        self.assertEqual(sub_arbol_izq.derecho.valor, 5)
        # Nieto izquierdo debe ser '+ 3 4'
        sub_arbol_nieto = sub_arbol_izq.izquierdo
        self.assertEqual(sub_arbol_nieto.valor, '+')
        self.assertEqual(sub_arbol_nieto.izquierdo.valor, 3)
        self.assertEqual(sub_arbol_nieto.derecho.valor, 4)

    def test_construir_ast_desde_postfijo_simple(self):
        """Prueba una expresion postfija simple."""
        tokens = "3 4 +".split()
        arbol = construir_ast_desde_postfijo(tokens)
        self.assertEqual(arbol.valor, '+')
        self.assertEqual(arbol.izquierdo.valor, 3)
        self.assertEqual(arbol.derecho.valor, 4)

    def test_construir_ast_desde_postfijo_compleja(self):
        """Prueba la expresion postfija compleja del enunciado."""
        tokens = "8 3 - 8 4 4 + * +".split()
        arbol = construir_ast_desde_postfijo(tokens)
        # Raiz debe ser '+'
        self.assertEqual(arbol.valor, '+')
        # Hijo izquierdo debe ser '8 3 -'
        self.assertEqual(arbol.izquierdo.valor, '-')
        self.assertEqual(arbol.izquierdo.izquierdo.valor, 8)
        self.assertEqual(arbol.izquierdo.derecho.valor, 3)
        # Hijo derecho debe ser '8 4 4 + *'
        self.assertEqual(arbol.derecho.valor, '*')
        self.assertEqual(arbol.derecho.izquierdo.valor, 8)
        self.assertEqual(arbol.derecho.derecho.valor, '+')
        self.assertEqual(arbol.derecho.derecho.izquierdo.valor, 4)
        self.assertEqual(arbol.derecho.derecho.derecho.valor, 4)

    # --- Pruebas para las funciones de accion ---

    def test_evaluar_ast_prefijo(self):
        """Prueba la evaluacion de la expresion prefija del enunciado."""
        tokens = "+ * + 3 4 5 7".split()
        arbol = construir_ast_desde_prefijo(tokens)
        resultado = evaluar_ast(arbol)
        self.assertEqual(resultado, 42)

    def test_evaluar_ast_postfijo(self):
        """Prueba la evaluacion de la expresion postfija del enunciado."""
        tokens = "8 3 - 8 4 4 + * +".split()
        arbol = construir_ast_desde_postfijo(tokens)
        resultado = evaluar_ast(arbol)
        self.assertEqual(resultado, 69)

    def test_mostrar_infijo_prefijo(self):
        """Prueba la conversion a infijo de la expresion prefija del enunciado."""
        tokens = "+ * + 3 4 5 7".split()
        arbol = construir_ast_desde_prefijo(tokens)
        resultado = mostrar_infijo(arbol)
        # Salida esperada: "(3 + 4) * 5 + 7"
        self.assertEqual("".join(resultado.split()), "(3+4)*5+7")

    def test_mostrar_infijo_postfijo(self):
        """Prueba la conversion a infijo de la expresion postfija del enunciado."""
        tokens = "8 3 - 8 4 4 + * +".split()
        arbol = construir_ast_desde_postfijo(tokens)
        resultado = mostrar_infijo(arbol)
        # La salida esperada es "8 - 3 + 8 * (4 + 4)"
        # Eliminamos los espacios para hacer la comparacion mas robusta
        self.assertEqual("".join(resultado.split()), "8-3+8*(4+4)")

    def test_mostrar_infijo_con_parentesis_necesarios(self):
        """Prueba una expresion que necesita parentesis por precedencia."""
        tokens = "3 4 + 5 *".split() # (3 + 4) * 5
        arbol = construir_ast_desde_postfijo(tokens)
        resultado = mostrar_infijo(arbol)
        self.assertEqual("".join(resultado.split()), "(3+4)*5")

    def test_expresiones_invalidas(self):
        """Prueba que las expresiones invalidas lancen errores."""
        # Postfija: faltan operandos
        with self.assertRaises(ValueError):
            construir_ast_desde_postfijo("3 +".split())
        # Postfija: sobran operandos
        with self.assertRaises(ValueError):
            construir_ast_desde_postfijo("3 4 5 +".split())
        # Prefija: fin inesperado
        with self.assertRaises(ValueError):
            construir_ast_desde_prefijo("+ 3".split())
        # Prefija: sobran tokens
        with self.assertRaises(ValueError):
            construir_ast_desde_prefijo("+ 3 4 5".split())

    def test_division_por_cero(self):
        """Prueba que la division por cero lance un error."""
        tokens = "/ 3 0".split()
        arbol = construir_ast_desde_prefijo(tokens)
        with self.assertRaises(ValueError):
            evaluar_ast(arbol)

    def test_token_invalido(self):
        """Prueba que un token no numerico lance un error."""
        with self.assertRaises(ValueError):
            construir_ast_desde_postfijo("3 a +".split())
        with self.assertRaises(ValueError):
            construir_ast_desde_prefijo("+ a 3".split())


class TestMainProgramFlow(unittest.TestCase):
    """Pruebas para el flujo principal del programa, simulando entrada de usuario."""

    def run_main_with_input(self, input_string):
        """Helper para ejecutar main() con una entrada simulada."""
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch('sys.stdin', new=StringIO(input_string)):
                try:
                    main()
                except SystemExit:
                    pass # Evitar que main() cierre el proceso de pruebas
                return fake_out.getvalue().strip()

    def test_comando_salir(self):
        """Prueba que el comando SALIR termine el programa."""
        output = self.run_main_with_input("SALIR\n")
        self.assertIn("Calculadora de Expresiones Aritmeticas", output)

    def test_comandos_invalidos(self):
        """Prueba el manejo de comandos y argumentos invalidos."""
        input_str = (
            "INVENTADO\n"
            "EVAL\n"
            "EVAL INVALIDO + 1 2\n"
            "SALIR\n"
        )
        output = self.run_main_with_input(input_str)
        self.assertIn("Comando 'INVENTADO' no reconocido", output)
        self.assertIn("Faltan argumentos para el comando", output)
        self.assertIn("Orden 'INVALIDO' no reconocido", output)


if __name__ == '__main__':
    unittest.main()
