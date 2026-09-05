#!/usr/bin/env python3
"""
Verificador especial para Windows 10 + Android + ADB
Verifica que todo esté correctamente instalado y configurado
"""

import subprocess
import sys
import os
from pathlib import Path


def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def print_check(name, status, message=""):
    icon = "✅" if status else "❌"
    print(f"{icon} {name}")
    if message:
        print(f"   └─ {message}")


def check_python():
    """Verifica la versión de Python"""
    print_header("PYTHON")
    
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"   Versión: {version}")
    
    if sys.version_info >= (3, 6):
        print_check("Python", True, "Versión compatible")
        return True
    else:
        print_check("Python", False, "Requiere Python 3.6 o superior")
        return False


def find_adb():
    """Encuentra dónde está ADB"""
    common_paths = [
        "adb",
        "C:\\platform-tools\\adb.exe",
        os.path.expanduser("~\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
        "C:\\Android\\Sdk\\platform-tools\\adb.exe",
    ]
    
    for path in common_paths:
        try:
            result = subprocess.run(
                [path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return path
        except:
            continue
    
    return None


def check_adb():
    """Verifica si ADB está instalado"""
    print_header("ANDROID DEBUG BRIDGE (ADB)")
    
    adb_path = find_adb()
    
    if adb_path:
        try:
            result = subprocess.run(
                [adb_path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            version_line = result.stdout.split('\n')[0]
            print(f"   Ubicación: {adb_path}")
            print(f"   {version_line}")
            print_check("ADB", True, "Instalado y accesible")
            return True, adb_path
        except Exception as e:
            print_check("ADB", False, f"Error: {e}")
            return False, None
    else:
        print_check("ADB", False, "No encontrado en PATH")
        print("\n   📝 Para instalar ADB:")
        print("   1. Ve a: https://developer.android.com/studio/releases/platform-tools")
        print("   2. Descarga: 'Download for Windows'")
        print("   3. Extrae en: C:\\platform-tools\\")
        print("   4. En PowerShell (admin): setx PATH \"%PATH%;C:\\platform-tools\"")
        print("   5. Cierra y reabre PowerShell")
        return False, None


def check_adb_devices(adb_path):
    """Verifica si hay dispositivos conectados"""
    print_header("DISPOSITIVOS ANDROID CONECTADOS")
    
    if not adb_path:
        print_check("Dispositivos", False, "ADB no está disponible")
        return False
    
    try:
        result = subprocess.run(
            [adb_path, "devices"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        devices = []
        for line in result.stdout.split('\n')[1:]:
            line = line.strip()
            if line and "device" in line and not line.startswith("*"):
                device_id = line.split()[0]
                status = line.split()[1] if len(line.split()) > 1 else "device"
                devices.append((device_id, status))
        
        if devices:
            for device_id, status in devices:
                if status == "device":
                    print_check("Dispositivo", True, f"ID: {device_id}")
                elif status == "unauthorized":
                    print_check("Dispositivo", False, f"No autorizado: {device_id}")
                    print("   💡 Autoriza el dispositivo en el diálogo de Android")
                else:
                    print_check("Dispositivo", False, f"Estado: {status}")
            
            return any(s == "device" for _, s in devices)
        else:
            print_check("Dispositivos", False, "No hay dispositivos conectados")
            print("\n   📝 Para conectar tu Android:")
            print("   1. Conecta el cable USB")
            print("   2. En Android: Ajustes > Sistema > Información")
            print("   3. Toca 'Número de compilación' 7 veces")
            print("   4. Ve a: Ajustes > Sistema > Opciones de desarrollador")
            print("   5. Activa: 'Depuración por USB'")
            print("   6. Autoriza el diálogo en el Android")
            print("   7. Vuelve a ejecutar esto")
            return False
    
    except Exception as e:
        print_check("Dispositivos", False, str(e))
        return False


def test_adb_connection(adb_path):
    """Prueba la conexión ADB"""
    print_header("PRUEBA DE CONEXIÓN")
    
    if not adb_path:
        print_check("Conexión", False, "ADB no disponible")
        return False
    
    try:
        result = subprocess.run(
            [adb_path, "shell", "echo", "test"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            print_check("Conexión", True, "Comunicación exitosa con el dispositivo")
            return True
        else:
            print_check("Conexión", False, "No se puede comunicar")
            print(f"   Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print_check("Conexión", False, "Timeout (dispositivo sin respuesta)")
        return False
    except Exception as e:
        print_check("Conexión", False, str(e))
        return False


def check_sms_program():
    """Verifica si el programa de SMS está presente"""
    print_header("PROGRAMA PYTHON SMS")
    
    sms_path = Path("sms_sender_android.py")
    
    if sms_path.exists():
        print_check("Programa", True, f"Encontrado: {sms_path.absolute()}")
        return True
    else:
        print_check("Programa", False, "No encontrado en la carpeta actual")
        print(f"\n   Carpeta actual: {Path.cwd()}")
        print("   📝 Coloca 'sms_sender_android.py' en esta carpeta")
        return False


def show_next_steps():
    """Muestra los siguientes pasos"""
    print_header("PRÓXIMOS PASOS")
    
    print("""
1️⃣  Si todo está ✅:
    python sms_sender_android.py

2️⃣  Si algo está ❌:
    • Revisa los pasos anteriores
    • Cierra y reabre PowerShell
    • Desconecta y reconecta el Android

3️⃣  Para automatizar:
    • Guarda el script como .bat en tu escritorio
    • Úsalo desde el Programador de Tareas de Windows

4️⃣  Ejemplo de uso en código:
    
    from sms_sender_android import AndroidSMSSender
    
    sender = AndroidSMSSender()
    sender.send_sms('+34123456789', 'Hola!')
""")


def main():
    """Ejecuta todas las verificaciones"""
    
    print("\n" + "🔍 "*20)
    print("VERIFICACIÓN COMPLETA: WINDOWS 10 + ANDROID + ADB + PYTHON")
    print("🔍 "*20)
    
    results = {}
    
    # Verificar Python
    results['Python'] = check_python()
    
    # Verificar ADB
    adb_ok, adb_path = check_adb()
    results['ADB'] = adb_ok
    
    # Verificar dispositivos (si ADB funciona)
    if adb_ok:
        results['Dispositivos'] = check_adb_devices(adb_path)
        
        # Prueba de conexión (si hay dispositivos)
        if results['Dispositivos']:
            results['Conexión'] = test_adb_connection(adb_path)
    
    # Verificar programa
    results['Programa SMS'] = check_sms_program()
    
    # Resumen
    print_header("RESUMEN")
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for check, status in results.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {check}")
    
    print(f"\nEstado: {passed}/{total} verificaciones pasadas")
    
    # Recomendaciones
    if passed == total:
        print("\n🎉 ¡TODO ESTÁ LISTO!")
        print("\nPuedes ejecutar:")
        print("   python sms_sender_android.py")
    else:
        print("\n⚠️  Revisa los elementos con ❌")
    
    show_next_steps()
    
    # Pausa antes de cerrar
    print("\nPresiona ENTER para cerrar...")
    input()


if __name__ == "__main__":
    main()
