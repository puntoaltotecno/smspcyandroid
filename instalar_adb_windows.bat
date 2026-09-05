@echo off
REM Script para instalar ADB automáticamente en Windows 10
REM Debe ejecutarse como ADMINISTRADOR

setlocal enabledelayedexpansion

echo ========================================
echo INSTALADOR AUTOMÁTICO DE ADB - WINDOWS 10
echo ========================================
echo.

REM Verificar si se ejecuta como admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo.
    echo ERROR: Este script requiere permisos de ADMINISTRADOR
    echo.
    echo Sigue estos pasos:
    echo 1. Haz click derecho en este archivo
    echo 2. Selecciona "Ejecutar como administrador"
    echo.
    pause
    exit /b 1
)

REM Verificar si Platform Tools ya está instalado
echo Verificando instalación anterior...
if exist "C:\platform-tools\adb.exe" (
    echo ✅ Platform Tools ya está instalado en C:\platform-tools\
    echo.
    goto add_path
)

REM Descargar Platform Tools
echo Descargando Android Platform Tools...
echo.
echo Abriendo navegador en 5 segundos...
timeout /t 5

start https://developer.android.com/studio/releases/platform-tools

echo.
echo Por favor:
echo 1. Descarga el archivo para Windows
echo 2. Extrae el ZIP en C:\ (quedará como C:\platform-tools\)
echo 3. Cuando termines, presiona cualquier tecla
echo.
pause

REM Verificar descarga
if not exist "C:\platform-tools\adb.exe" (
    echo.
    echo ERROR: Platform Tools no se encontró en C:\platform-tools\
    echo.
    echo Por favor, extrae manualmente:
    echo 1. Descarga desde: https://developer.android.com/studio/releases/platform-tools
    echo 2. Extrae en: C:\
    echo 3. Debería quedar: C:\platform-tools\adb.exe
    echo.
    pause
    exit /b 1
)

:add_path
echo.
echo Agregando ADB al PATH...
setx PATH "%PATH%;C:\platform-tools"

if %errorLevel% equ 0 (
    echo ✅ ADB agregado al PATH exitosamente
) else (
    echo ❌ Error al agregar al PATH
    pause
    exit /b 1
)

echo.
echo ========================================
echo ✅ INSTALACIÓN COMPLETADA
echo ========================================
echo.
echo Próximos pasos:
echo.
echo 1. CIERRA esta ventana de CMD
echo 2. ABRE una NUEVA ventana de PowerShell o CMD
echo 3. Verifica: adb version
echo 4. Conecta tu Android por USB
echo 5. Ejecuta: python sms_sender_android.py
echo.
echo Para conectar tu Android:
echo   • Ajustes ^> Sistema ^> Información del dispositivo
echo   • Toca "Número de compilación" 7 veces
echo   • Ajustes ^> Opciones de desarrollador
echo   • Activa "Depuración por USB"
echo   • Autoriza el dispositivo
echo.
pause
