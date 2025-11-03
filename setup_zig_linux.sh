#!/bin/bash
# Script para descargar y configurar el compilador de Zig para Linux.

echo "Descargando el compilador de Zig..."

# URL del archivo .tar.xz de Zig para Linux x64
ZIG_URL="https://ziglang.org/download/0.11.0/zig-linux-x86_64-0.11.0.tar.xz"
OUTPUT_TAR="zig.tar.xz"
OUTPUT_DIR="zig_compiler"

# Descargar el archivo
wget -O $OUTPUT_TAR $ZIG_URL

# Crear el directorio y descomprimir
echo "Descomprimiendo..."
mkdir -p $OUTPUT_DIR
tar -xf $OUTPUT_TAR -C $OUTPUT_DIR --strip-components=1

# Limpiar el archivo .tar.xz
rm $OUTPUT_TAR

echo "-----------------------------------------------------"
echo "Instalacion completada."
echo "La carpeta '$OUTPUT_DIR' ha sido creada."
echo "No se necesita anadir nada a su PATH."
echo "-----------------------------------------------------"
