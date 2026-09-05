#!/usr/bin/env python3
"""
MENÚ PRINCIPAL
Centro de control para todas las funcionalidades de SMS
"""

import subprocess
import sys
import os
from pathlib import Path


class MenuPrincipal:
    """Menú centralizado para el sistema de SMS"""
    
    def __init__(self):
        self.opciones = {
            '1': {
                'nombre': 'Enviar SMS individual',
                'descripcion': 'Envía un SMS escribiendo el número y mensaje',
                'script': 'sms_sender_android.py'
            },
            '2': {
                'nombre': 'Envío automático desde archivo',
                'descripcion': 'Lee contactos.txt y envía a múltiples números',
                'script': 'enviar_desde_archivo.py'
            },
            '3': {
                'nombre': 'Envío programado',
                'descripcion': 'Programa envíos para una hora específica',
                'script': 'enviar_programado.py'
            },
            '4': {
                'nombre': 'Validar contactos',
                'descripcion': 'Valida y genera archivo de contactos',
                'script': 'validar_contactos.py'
            },
            '5': {
                'nombre': 'Ver historial',
                'descripcion': 'Consulta historial de envíos realizados',
                'script': 'historial_envios.py'
            },
            '6': {
                'nombre': 'Ver ejemplos de código',
                'descripcion': 'Muestra 11 ejemplos prácticos de uso',
                'script': 'ejemplos_uso.py'
            },
            '7': {
                'nombre': 'Verificar instalación',
                'descripcion': 'Verifica que todo esté configurado correctamente',
                'script': 'verificar_windows.py'
            }
        }
    
    def mostrar_menu(self):
        """Muestra el menú principal"""
        print("\n" + "="*70)
        print(" "*15 + "📱 CENTRO DE CONTROL SMS 📱")
        print("="*70 + "\n")
        
        for key, opcion in self.opciones.items():
            print(f"{key}. {opcion['nombre']}")
            print(f"   └─ {opcion['descripcion']}\n")
        
        print("0. Salir")
        print("\n" + "="*70)
    
    def ejecutar_script(self, script: str) -> bool:
        """
        Ejecuta un script Python
        
        Args:
            script: Nombre del script a ejecutar
        
        Returns:
            True si se ejecutó correctamente
        """
        archivo = Path(script)
        
        if not archivo.exists():
            print(f"\n❌ Script no encontrado: {script}")
            return False
        
        print(f"\n▶️  Ejecutando {script}...\n")
        
        try:
            # Ejecutar el script
            resultado = subprocess.run(
                [sys.executable, script],
                check=False
            )
            
            return resultado.returncode == 0
        
        except Exception as e:
            print(f"❌ Error al ejecutar: {e}")
            return False
    
    def mostrar_atajos(self):
        """Muestra comandos de atajo"""
        print("\n" + "="*70)
        print("⚡ COMANDOS DE ATAJO")
        print("="*70)
        print("""
Puedes ejecutar los scripts directamente desde cmd/PowerShell:

  python sms_sender_android.py          # Envío individual
  python enviar_desde_archivo.py        # Envío automático
  python enviar_programado.py           # Envío programado
  python validar_contactos.py           # Validar contactos
  python historial_envios.py            # Ver historial
  python ejemplos_uso.py                # Ver ejemplos
  python verificar_windows.py           # Verificar sistema

O ejecuta este menú nuevamente:
  python menu.py

""")
    
    def mostrar_ayuda(self):
        """Muestra información de ayuda"""
        print("\n" + "="*70)
        print("❓ AYUDA RÁPIDA")
        print("="*70)
        print("""
PARA EMPEZAR:

1. Crear archivo contactos.txt
   Formato: numero|mensaje
   Ejemplo: +34600111111|Hola mundo

2. Ejecutar: python enviar_desde_archivo.py

3. Seguir las instrucciones

ARCHIVOS IMPORTANTES:

  contactos.txt           - Lista de números y mensajes
  historial_envios.json   - Registro de envíos
  CHECKLIST.md           - Guía paso a paso
  GUIA_AUTOMATIZACION.md - Guía detallada

PROBLEMAS?

  python verificar_windows.py

EJEMPLOS DE CÓDIGO?

  python ejemplos_uso.py

""")
    
    def mostrar_estado(self):
        """Muestra el estado del sistema"""
        print("\n" + "="*70)
        print("📊 ESTADO DEL SISTEMA")
        print("="*70 + "\n")
        
        # Verificar archivos
        archivos = {
            'contactos.txt': 'Archivo de contactos',
            'historial_envios.json': 'Historial de envíos',
        }
        
        for archivo, descripcion in archivos.items():
            path = Path(archivo)
            if path.exists():
                tamaño = path.stat().st_size
                print(f"✅ {descripcion}")
                print(f"   └─ {archivo} ({tamaño} bytes)")
            else:
                print(f"⚠️  {descripcion}")
                print(f"   └─ {archivo} (no encontrado)")
        
        # Verificar ADB
        print("\n🔧 Dispositivos Android:")
        try:
            resultado = subprocess.run(
                ['adb', 'devices'],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if 'device' in resultado.stdout:
                print("✅ Android conectado")
            else:
                print("⚠️  No hay dispositivos conectados")
        except:
            print("❌ ADB no disponible")
        
        print()
    
    def ejecutar(self):
        """Ejecuta el menú principal"""
        while True:
            self.mostrar_menu()
            
            opcion = input("Selecciona una opción (0-7): ").strip()
            
            if opcion == '0':
                print("\n👋 ¡Hasta luego!\n")
                break
            
            elif opcion == '?':
                self.mostrar_ayuda()
            
            elif opcion == 's':
                self.mostrar_estado()
            
            elif opcion in self.opciones:
                script = self.opciones[opcion]['script']
                self.ejecutar_script(script)
                
                input("\nPresiona ENTER para continuar...")
            
            else:
                print("\n❌ Opción no válida")
                input("Presiona ENTER para continuar...")


def main():
    """Función principal"""
    try:
        menu = MenuPrincipal()
        
        # Mostrar bienvenida
        print("\n" + "🎯 "*25)
        print("BIENVENIDO AL SISTEMA DE ENVÍO DE SMS")
        print("🎯 "*25)
        
        print("\n💡 Consejos:")
        print("  • Presiona '?' para ver la ayuda")
        print("  • Presiona 's' para ver el estado")
        print("  • Asegúrate de que Android esté conectado\n")
        
        # Ejecutar menú
        menu.ejecutar()
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
