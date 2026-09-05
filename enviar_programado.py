#!/usr/bin/env python3
"""
ENVÍO PROGRAMADO DE SMS
Programa envíos para una hora específica del día
"""

import time
import sys
from datetime import datetime, timedelta
from pathlib import Path
from enviar_desde_archivo import EnviadorAutomatico


class EnviadorProgramado:
    """Programa envíos de SMS para una hora específica"""
    
    def __init__(self, archivo: str = 'contactos.txt'):
        self.archivo = archivo
        self.enviador = EnviadorAutomatico(archivo)
    
    def solicitar_hora(self) -> tuple:
        """
        Solicita la hora de envío
        
        Returns:
            Tupla (hora, minuto) en formato 24h
        """
        print("\n⏰ PROGRAMAR ENVÍO")
        print("-" * 40)
        
        while True:
            try:
                hora_str = input("Hora (0-23) [ahora]: ").strip()
                
                if not hora_str:
                    # Envío inmediato
                    return None, None
                
                hora = int(hora_str)
                if not 0 <= hora <= 23:
                    print("❌ La hora debe estar entre 0 y 23")
                    continue
                
                minuto_str = input("Minuto (0-59) [0]: ").strip()
                
                if not minuto_str:
                    minuto = 0
                else:
                    minuto = int(minuto_str)
                    if not 0 <= minuto <= 59:
                        print("❌ El minuto debe estar entre 0 y 59")
                        continue
                
                return hora, minuto
            
            except ValueError:
                print("❌ Por favor ingresa números válidos")
    
    def calcular_tiempo_espera(self, hora: int, minuto: int) -> int:
        """
        Calcula cuántos segundos faltan para la hora programada
        
        Args:
            hora: Hora (0-23)
            minuto: Minuto (0-59)
        
        Returns:
            Segundos de espera
        """
        ahora = datetime.now()
        programado = ahora.replace(hour=hora, minute=minuto, second=0, microsecond=0)
        
        # Si la hora ya pasó hoy, programar para mañana
        if programado <= ahora:
            programado += timedelta(days=1)
        
        tiempo_espera = (programado - ahora).total_seconds()
        
        return int(tiempo_espera), programado
    
    def mostrar_cuenta_regresiva(self, segundos: int, programado: datetime):
        """Muestra una cuenta regresiva hasta el envío"""
        print(f"\n⏳ CUENTA REGRESIVA")
        print("-" * 40)
        print(f"Envío programado para: {programado.strftime('%H:%M:%S')}")
        print(f"Espera: {segundos // 60} minutos {segundos % 60} segundos")
        print("\nPresiona Ctrl+C para cancelar\n")
        
        segundos_restantes = segundos
        
        try:
            while segundos_restantes > 0:
                # Mostrar tiempo restante
                minutos = segundos_restantes // 60
                secs = segundos_restantes % 60
                
                if segundos_restantes <= 60:
                    # Últimos 60 segundos en conteo rápido
                    print(f"⏰ Faltam: {minutos:02d}:{secs:02d}s", end='\r')
                else:
                    # Cada minuto
                    if secs == 0:
                        print(f"⏰ Faltan: {minutos} minuto(s)")
                
                time.sleep(1)
                segundos_restantes -= 1
            
            print("\n✅ ¡Es hora de enviar!")
            return True
        
        except KeyboardInterrupt:
            print("\n\n⏹️  Envío cancelado")
            return False
    
    def ejecutar_programado(self, pausa: float = 2.0) -> bool:
        """Ejecuta el flujo de envío programado"""
        
        # Leer contactos
        print("📂 Leyendo contactos...")
        if not self.enviador.leer_archivo():
            return False
        
        # Mostrar resumen
        self.enviador.mostrar_resumen()
        
        # Solicitar hora
        hora, minuto = self.solicitar_hora()
        
        if hora is None:
            # Envío inmediato
            print("\n📤 Envío inmediato...")
            if not self.enviador.confirmar():
                return False
            self.enviador.enviar_todos(pausa=pausa)
            return True
        
        # Calcular tiempo de espera
        tiempo_espera, programado = self.calcular_tiempo_espera(hora, minuto)
        
        # Mostrar cuenta regresiva
        if not self.mostrar_cuenta_regresiva(tiempo_espera, programado):
            return False
        
        # Enviar cuando llegue la hora
        print("\n📤 INICIANDO ENVÍO PROGRAMADO")
        self.enviador.enviar_todos(pausa=pausa)
        
        return True


def main():
    """Función principal"""
    try:
        print("\n" + "⏰ "*20)
        print("ENVÍO PROGRAMADO DE SMS")
        print("⏰ "*20 + "\n")
        
        enviador = EnviadorProgramado('contactos.txt')
        exitoso = enviador.ejecutar_programado()
        
        if exitoso:
            print("\n🎉 ¡Envío completado!")
        
        sys.exit(0 if exitoso else 1)
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Operación cancelada")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
