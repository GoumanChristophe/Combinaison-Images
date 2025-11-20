@echo off
echo ========================================
echo   IMAGE COMBINER - Compilation EXE
echo ========================================
echo.

echo [1/3] Verification des dependances...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller n'est pas installe. Installation...
    pip install pyinstaller flask pillow werkzeug
) else (
    echo PyInstaller est installe !
)

echo.
echo [2/3] Nettoyage des anciens fichiers...
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
echo Nettoyage termine !

echo.
echo [3/3] Compilation de l'executable...
pyinstaller ImageCombiner.spec

echo.
if exist dist\ImageCombiner.exe (
    echo ========================================
    echo   COMPILATION REUSSIE !
    echo ========================================
    echo.
    echo L'executable se trouve dans : dist\ImageCombiner.exe
    echo.
    echo Tu peux maintenant :
    echo - Lancer dist\ImageCombiner.exe
    echo - Distribuer ce fichier
    echo.
    pause
) else (
    echo ========================================
    echo   ERREUR DE COMPILATION
    echo ========================================
    echo.
    echo Verifie les messages d'erreur ci-dessus
    echo.
    pause
)
