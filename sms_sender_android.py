#!/usr/bin/env python3
"""
Programa para enviar mensajes SMS desde Android usando ADB (Android Debug Bridge)
Requisitos:
- Android SDK Platform Tools (para ADB)
- Dispositivo Android conectado por USB con depuración habilitada
- Permisos de SMS en el dispositivo Android
"""

import subprocess
import sys
import os
from typing import Tuple, List


class AndroidSMSSender:
    """Envía mensajes SMS usando un dispositivo Android conectado vía ADB"""
    
    def __init__(self):
        self.adb_path = self._find_adb()
        if not self.adb_path:
            raise Exception("ADB no encontrado. Instala Android SDK Platform Tools")
    
    def _find_adb(self) -> str:
        """Busca la ruta de ADB en el sistema"""
        # Intentar encontrar ADB en rutas comunes
        common_paths = [
            "adb",  # En PATH
            os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
            "C:\\Android\\Sdk\\platform-tools\\adb.exe",  # Windows
            "/usr/bin/adb",  # Linux
            "/usr/local/bin/adb",  # macOS
        ]
        
        for path in common_paths:
            try:
                subprocess.run([path, "version"], capture_output=True, check=True)
                return path
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        
        return None
    
    def _run_adb(self, command: List[str]) -> Tuple[int, str, str]:
        """Ejecuta un comando ADB y retorna código de salida, stdout y stderr"""
        try:
            result = subprocess.run(
                [self.adb_path] + command,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Timeout en comando ADB"
        except Exception as e:
            return -1, "", str(e)
    
    def get_connected_devices(self) -> List[str]:
        """Obtiene lista de dispositivos Android conectados"""
        code, stdout, stderr = self._run_adb(["devices"])
        
        if code != 0:
            raise Exception(f"Error al obtener dispositivos: {stderr}")
        
        devices = []
        for line in stdout.split('\n')[1:]:  # Saltar primera línea
            line = line.strip()
            if line and "device" in line and not line.startswith("*"):
                device_id = line.split()[0]
                devices.append(device_id)
        
        return devices
    
    def send_sms(self, phone_number: str, message: str, device: str = None) -> bool:
        """
        Envía un SMS a través del dispositivo Android
        
        Args:
            phone_number: Número de teléfono (ej: "+34123456789" o "123456789")
            message: Contenido del mensaje
            device: ID del dispositivo (si hay varios conectados)
        
        Returns:
            True si el SMS se envió exitosamente, False en caso contrario
        """
        # Validar entrada
        if not phone_number or not message:
            print("❌ Error: Proporciona número de teléfono y mensaje")
            return False
        
        # Obtener dispositivos disponibles
        devices = self.get_connected_devices()
        
        if not devices:
            print("❌ No hay dispositivos Android conectados")
            return False
        
        # Seleccionar dispositivo
        if device is None:
            device = devices[0]
            if len(devices) > 1:
                print(f"⚠️  Múltiples dispositivos encontrados. Usando: {device}")
        
        if device not in devices:
            print(f"❌ Dispositivo {device} no encontrado")
            return False
        
        # Comando para enviar SMS usando am (Activity Manager) de Android
        # Abre la app de SMS con ACTION_SEND
        cmd = [
            "-s", device,
            "shell", "am", "start",
            "-a", "android.intent.action.SEND",
            "-t", "text/plain",
            "--es", "android.intent.extra.TEXT", message,
            "--es", "address", phone_number,
            "com.android.mms"
        ]
        
        print(f"\n📱 Enviando SMS...")
        print(f"   Dispositivo: {device}")
        print(f"   Número: {phone_number}")
        print(f"   Mensaje: {message}")
        
        code, stdout, stderr = self._run_adb(cmd)
        
        if code == 0:
            print("✅ SMS enviado exitosamente")
            return True
        else:
            print(f"❌ Error al enviar SMS: {stderr}")
            return False
    
    def send_sms_via_telephony(self, phone_number: str, message: str, device: str = None) -> bool:
        """
        Alternativa: Envía SMS usando la API de telefonía de Android
        Este método requiere que la app tenga permisos especiales
        """
        devices = self.get_connected_devices()
        
        if not devices:
            print("❌ No hay dispositivos Android conectados")
            return False
        
        if device is None:
            device = devices[0]
        
        # Usar settings para enviar SMS (puede requerir permisos root en algunos casos)
        cmd = [
            "-s", device,
            "shell", "service", "call", "isms", "sendText",
            "0", f"'{phone_number}'", "null",
            f"'{message}'", "null", "null"
        ]
        
        code, stdout, stderr = self._run_adb(cmd)
        
        if code == 0 and "Result: Parcel" in stdout:
            print("✅ SMS enviado mediante telefonía")
            return True
        else:
            print(f"❌ Error: {stderr if stderr else stdout}")
            return False


def main():
    """Función principal con ejemplos de uso"""
    try:
        # Inicializar el enviador
        sender = AndroidSMSSender()
        
        # Mostrar dispositivos conectados
        print("=== Dispositivos Android conectados ===")
        devices = sender.get_connected_devices()
        
        if not devices:
            print("❌ No hay dispositivos conectados")
            print("\n📝 Para conectar tu Android:")
            print("   1. Habilita 'Depuración USB' en Ajustes > Opciones de desarrollador")
            print("   2. Conecta el dispositivo por USB")
            print("   3. Autoriza la conexión en el diálogo del dispositivo")
            return
        
        for i, device in enumerate(devices, 1):
            print(f"   {i}. {device}")
        
        print("\n" + "="*40)
        
        # Ejemplo: enviar SMS
        while True:
            print("\n📲 ENVIAR SMS")
            phone = input("Número de teléfono: ").strip()
            if not phone:
                print("Cancelado")
                break
            
            msg = input("Mensaje: ").strip()
            if not msg:
                print("Cancelado")
                break
            
            # Enviar el SMS
            success = sender.send_sms(phone, msg)
            
            if success:
                otro = input("\n¿Enviar otro SMS? (s/n): ").strip().lower()
                if otro != 's':
                    break
            else:
                print("⚠️  Intenta de nuevo")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
