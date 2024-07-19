#!/bin/bash

# Nombre del programa
PROGRAMA="EnerPass"
VERSION="1.0.0"
ICONO="image.png"

# Directorios de instalación
DEST_DIR="/usr/local/bin"
ICON_DIR="/usr/local/share/icons"
DESKTOP_ENTRY="/usr/share/applications/$PROGRAMA.desktop"

# Comprobando si el programa ya está instalado
if [ -f "$DEST_DIR/$PROGRAMA" ]; then
    echo "$PROGRAMA ya está instalado en $DEST_DIR"
    echo "¿Desea sobrescribirlo? (s/n)"
    read SOBRESCRIBIR
    if [ "$SOBRESCRIBIR" != "s" ]; then
        echo "Instalación cancelada."
        exit 1
    fi
fi

# Comprobando si se requiere sudo
if [ "$EUID" -ne 0 ]; then
    echo "Por favor ejecute el script como superusuario."
    exit 1
fi

# Copiando el binario al directorio de destino
echo "Instalando $PROGRAMA en $DEST_DIR..."
cp "$PROGRAMA" "$DEST_DIR"
chmod +x "$DEST_DIR/$PROGRAMA"

# Copiando el icono al directorio de iconos
echo "Instalando el icono en $ICON_DIR..."

echo "cp $ICONO $ICON_DIR"
cp "$ICONO" "$ICON_DIR"/"$ICONO"

# Creando el archivo .desktop
echo "Creando el archivo .desktop..."
echo "[Desktop Entry]
Name=EnerPass
Comment=transfiere tus contraseñas de forma segura
Exec=$DEST_DIR/$PROGRAMA
Icon=$ICON_DIR/$ICONO
Terminal=false
Type=Application
Categories=Utility;Application;" > "$DESKTOP_ENTRY"

# Verificando la instalación
if [ -f "$DEST_DIR/$PROGRAMA" ]; then
    echo "$PROGRAMA instalado con éxito en $DEST_DIR"
    echo "Versión: $VERSION"
else
    echo "Error en la instalación de $PROGRAMA"
    exit 1
fi

# Añadiendo al PATH si no está ya incluido
if ! echo "$PATH" | grep -q "$DEST_DIR"; then
    echo "export PATH=\$PATH:$DEST_DIR" >> ~/.bashrc
    source ~/.bashrc
    echo "$DEST_DIR añadido al PATH."
fi

echo "Instalación completa."
