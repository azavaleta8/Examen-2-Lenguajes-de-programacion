const std = @import("std");

// Implementacion de la funcion f(n) del problema de Collatz.
// Si n es par, devuelve n / 2.
// Si n es impar, devuelve 3 * n + 1.
fn f(n: u64) u64 {
    if (n % 2 == 0) {
        return n / 2;
    } else {
        return 3 * n + 1;
    }
}

// Calcula la cantidad de pasos para que n llegue a 1.
fn count(n: u64) u64 {
    var current_n = n;
    var steps: u64 = 0;

    // El bucle se ejecuta hasta que el valor actual sea 1.
    while (current_n != 1) {
        current_n = f(current_n);
        steps += 1;
    }
    return steps;
}

// Funcion principal para probar el programa.
pub fn main() !void {
    const n: u64 = 42;
    const result = count(n);
    std.debug.print("count({d}) = {d}\n", .{ n, result });
}
