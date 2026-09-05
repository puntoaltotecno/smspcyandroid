#!/usr/bin/env python3
"""
ENVIAR SMS AUTOMATIZADO DESDE ARCHIVO
Lee contactos.txt y envía SMS a múltiples números con pausas
"""

import time
import sys
from pathlib import Path
from sms_sender_android import AndroidSMSSender


class EnviadorAutomatico:
    """Envía SMS automatizado desde un archivo de contactos"""
    
    def __init__(self, archivo: str = 'contactos.txt'):
        """
        Inicializa el enviador
        
        Args:
            archivo: Ruta al archivo de contactos (default: contactos.txt)
        """
        self.archivo = Path(archivo)
        self.sender = AndroidSMSSender()
        self.contactos = []
    
    def leer_archivo(self) -> bool:
        """
        Lee el archivo de contactos
        
        Formato: numero|mensaje
        Líneas que empiezan con # son comentarios
        
        Returns:
            True si se leyó correctamente, False en caso contrario
        """
        if not self.archivo.exists():
            print(f"❌ Archivo no encontrado: {self.archivo}")
            print(f"\n💡 Crea un archivo llamado '{self.archivo}' con este formato:")
            print("   +34123456789|Hola, este es tu mensaje")
            print("   +34987654321|Otro mensaje")
            return False
        
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                for num_linea, linea in enumerate(f, 1):
                    linea = linea.strip()
                    
                    # Ignorar líneas vacías y comentarios
                    if not linea or linea.startswith('#'):
                        continue
                    
                    # Parsear: numero|mensaje
                    if '|' not in linea:
                        print(f"⚠️  Línea {num_linea} inválida (falta |): {linea}")
                        continue
                    
                    partes = linea.split('|', 1)  # Split solo en el primer |
                    numero = partes[0].strip()
                    mensaje = partes[1].strip()
                    
                    # Validar
                    if not numero or not mensaje:
                        print(f"⚠️  Línea {num_linea} incompleta")
                        continue
                    
                    # Agregar + si no lo tiene
                    if not numero.startswith('+'):
                        numero = f"+{numero}"
                    
                    self.contactos.append({
                        'numero': numero,
                        'mensaje': mensaje,
                        'linea': num_linea
                    })
            
            return len(self.contactos) > 0
        
        except Exception as e:
            print(f"❌ Error al leer archivo: {e}")
            return False
    
    def mostrar_resumen(self):
        """Muestra un resumen de los contactos a enviar"""
        print("\n" + "="*60)
        print(f"📋 RESUMEN: {len(self.contactos)} SMS a enviar")
        print("="*60 + "\n")
        
        for i, contacto in enumerate(self.contactos, 1):
            numero = contacto['numero']
            mensaje = contacto['mensaje']
            
            # Truncar mensaje largo
            if len(mensaje) > 50:
                mensaje_display = mensaje[:47] + "..."
            else:
                mensaje_display = mensaje
            
            print(f"{i:2}. {numero:17} | {mensaje_display}")
        
        print()
    
    def confirmar(self) -> bool:
        """Pide confirmación antes de enviar"""
        print(f"⚠️  Se enviarán {len(self.contactos)} SMS\n")
        
        respuesta = input("¿Confirmas el envío? (s/n): ").strip().lower()
        return respuesta == 's'
    
    def enviar_todos(self, pausa: float = 2.0, reintentos: int = 2) -> dict:
        """
        Envía todos los SMS con pausas
        
        Args:
            pausa: Segundos de espera entre mensajes (default: 2)
            reintentos: Número de reintentos si falla (default: 2)
        
        Returns:
            Diccionario con estadísticas del envío
        """
        if not self.contactos:
            print("❌ No hay contactos para enviar")
            return {}
        
        stats = {
            'total': len(self.contactos),
            'exitosos': 0,
            'fallidos': 0,
            'errores': []
        }
        
        print("\n" + "="*60)
        print("📤 INICIANDO ENVÍO")
        print("="*60 + "\n")
        
        tiempo_inicio = time.time()
        
        for idx, contacto in enumerate(self.contactos, 1):
            numero = contacto['numero']
            mensaje = contacto['mensaje']
            
            # Mostrar progreso
            print(f"[{idx}/{len(self.contactos)}] Enviando a {numero}...")
            
            # Intentar enviar con reintentos
            enviado = False
            for intento in range(1, reintentos + 1):
                try:
                    resultado = self.sender.send_sms(numero, mensaje)
                    
                    if resultado:
                        print(f"     ✅ Enviado")
                        stats['exitosos'] += 1
                        enviado = True
                        break
                    else:
                        if intento < reintentos:
                            print(f"     ⚠️  Fallo, reintentando...")
                        else:
                            print(f"     ❌ Falló después de {reintentos} intentos")
                
                except Exception as e:
                    if intento < reintentos:
                        print(f"     ⚠️  Error: {e}, reintentando...")
                    else:
                        print(f"     ❌ Error: {e}")
                        stats['errores'].append(f"Línea {contacto['linea']}: {e}")
            
            if not enviado:
                stats['fallidos'] += 1
            
            # Pausa entre mensajes (excepto en el último)
            if idx < len(self.contactos):
                self._mostrar_pausa(pausa)
        
        # Mostrar tiempo total
        tiempo_total = time.time() - tiempo_inicio
        
        # Resumen final
        print("\n" + "="*60)
        print("📊 RESULTADO FINAL")
        print("="*60)
        print(f"✅ Exitosos: {stats['exitosos']}/{stats['total']}")
        print(f"❌ Fallidos: {stats['fallidos']}/{stats['total']}")
        print(f"⏱️  Tiempo total: {tiempo_total:.1f} segundos")
        
        if stats['errores']:
            print("\n⚠️  Errores:")
            for error in stats['errores'][:5]:  # Mostrar máximo 5 errores
                print(f"   • {error}")
        
        print()
        
        return stats
    
    @staticmethod
    def _mostrar_pausa(segundos: float):
        """Muestra una barra de progreso para la pausa"""
        for i in range(int(segundos), 0, -1):
            print(f"     ⏳ Pausa: {i}s", end='\r')
            time.sleep(1)
        print("     ✅ Continuando...")
    
    def ejecutar(self, pausa: float = 2.0) -> bool:
        """
        Ejecuta el flujo completo: leer, confirmar, enviar
        
        Args:
            pausa: Segundos de pausa entre mensajes
        
        Returns:
            True si se completó exitosamente
        """
        # Leer archivo
        print("📂 Leyendo archivo de contactos...")
        if not self.leer_archivo():
            return False
        
        # Mostrar resumen
        self.mostrar_resumen()
        
        # Pedir pausa personalizada
        try:
            pausa_input = input("Pausa entre SMS (segundos) [2]: ").strip()
            if pausa_input:
                pausa = float(pausa_input)
                if pausa < 0:
                    pausa = 0
            print(f"✅ Pausa configurada: {pausa} segundos\n")
        except ValueError:
            print(f"⚠️  Valor inválido, usando pausa por defecto: {pausa} segundos\n")
        
        # Confirmar
        if not self.confirmar():
            print("❌ Envío cancelado")
            return False
        
        # Enviar
        self.enviar_todos(pausa=pausa)
        
        return True


def main():
    """Función principal"""
    try:
        print("\n" + "🤖 "*20)
        print("ENVÍO AUTOMATIZADO DE SMS DESDE ARCHIVO")
        print("🤖 "*20 + "\n")
        
        # Crear enviador
        enviador = EnviadorAutomatico('contactos.txt')
        
        # Ejecutar
        exitoso = enviador.ejecutar()
        
        if exitoso:
            print("🎉 ¡Envío completado exitosamente!")
        
        sys.exit(0 if exitoso else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Envío cancelado por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
