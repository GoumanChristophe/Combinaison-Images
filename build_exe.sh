#!/bin/bash

echo "========================================"
echo "  IMAGE COMBINER - Compilation EXE"
echo "========================================"
echo ""

echo "[1/3] Vérification des dépendances..."
if ! pip show pyinstaller &> /dev/null; then
    echo "PyInstaller n'est pas installé. Installation..."
    pip install pyinstaller flask pillow werkzeug
else
    echo "PyInstaller est installé !"
fi

echo ""
echo "[2/3] Nettoyage des anciens fichiers..."
rm -rf build dist
echo "Nettoyage terminé !"

echo ""
echo "[3/3] Compilation de l'exécutable..."
pyinstaller ImageCombiner.spec

echo ""
if [ -f "dist/ImageCombiner" ]; then
    echo "========================================"
    echo "  COMPILATION RÉUSSIE !"
    echo "========================================"
    echo ""
    echo "L'exécutable se trouve dans : dist/ImageCombiner"
    echo ""
    echo "Tu peux maintenant :"
    echo "- Lancer ./dist/ImageCombiner"
    echo "- Distribuer ce fichier"
    echo ""
else
    echo "========================================"
    echo "  ERREUR DE COMPILATION"
    echo "========================================"
    echo ""
    echo "Vérifie les messages d'erreur ci-dessus"
    echo ""
fi
