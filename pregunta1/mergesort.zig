const std = @import("std");

// Implementacion del algoritmo Mergesort.
// Es una funcion recursiva que divide el arreglo y luego combina los resultados.
// Requiere un 'allocator' para gestionar la memoria de los arreglos temporales.
pub fn mergesort(items: []i32, allocator: std.mem.Allocator) ![]i32 {
    // Caso base: si el arreglo tiene 1 o 0 elementos, ya esta ordenado.
    if (items.len <= 1) {
        return items;
    }

    // Se divide el arreglo en dos mitades.
    const mid = items.len / 2;
    var left = try mergesort(items[0..mid], allocator);
    var right = try mergesort(items[mid..], allocator);

    // Se combinan las dos mitades ordenadas.
    return merge(left, right, allocator);
}

// Funcion para combinar (merge) dos arreglos ordenados en uno solo.
fn merge(left: []i32, right: []i32, allocator: std.mem.Allocator) ![]i32 {
    // Se reserva memoria para el arreglo resultante.
    var result = try allocator.alloc(i32, left.len + right.len);
    var i: usize = 0; // Indice para el arreglo 'left'
    var j: usize = 0; // Indice para el arreglo 'right'
    var k: usize = 0; // Indice para el arreglo 'result'

    // Se comparan los elementos de 'left' y 'right' y se agregan al resultado en orden.
    while (i < left.len and j < right.len) {
        if (left[i] < right[j]) {
            result[k] = left[i];
            i += 1;
        } else {
            result[k] = right[j];
            j += 1;
        }
        k += 1;
    }

    // Si quedan elementos en 'left', se agregan al final del resultado.
    while (i < left.len) {
        result[k] = left[i];
        i += 1;
        k += 1;
    }

    // Si quedan elementos en 'right', se agregan al final del resultado.
    while (j < right.len) {
        result[k] = right[j];
        j += 1;
        k += 1;
    }
    
    return result;
}

// Funcion principal para probar el algoritmo.
pub fn main() !void {
    // Se necesita un allocator para que Mergesort pueda reservar memoria.
    var gpa = std.heap.GeneralPurposeAllocator(.{}){};
    const allocator = gpa.allocator();

    var data = [_]i32{ 38, 27, 43, 3, 9, 82, 10 };
    std.debug.print("Original: {any}\n", .{data});
    
    var sorted_data = try mergesort(&data, allocator);
    std.debug.print("Ordenado: {any}\n", .{sorted_data});
}
