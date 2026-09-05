#!/usr/bin/env python3
"""
HISTORIAL DE ENVÍOS
Registra y consulta el historial de SMS enviados
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict


class HistorialEnvios:
    """Gestiona el historial de envíos de SMS"""
    
    ARCHIVO_HISTORIAL = 'historial_envios.json'
    
    def __init__(self):
        self.historial = self._cargar_historial()
    
    def _cargar_historial(self) -> List[Dict]:
        """Carga el historial del archivo"""
        archivo = Path(self.ARCHIVO_HISTORIAL)
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _guardar_historial(self) -> bool:
        """Guarda el historial al archivo"""
        try:
            with open(self.ARCHIVO_HISTORIAL, 'w', encoding='utf-8') as f:
                json.dump(self.historial, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error al guardar historial: {e}")
            return False
    
    def registrar_envio(self, numero: str, mensaje: str, exitoso: bool, 
                       motivo_error: str = None) -> bool:
        """
        Registra un envío en el historial
        
        Args:
            numero: Número de teléfono
            mensaje: Contenido del SMS
            exitoso: Si fue exitoso
            motivo_error: Razón del error (si aplica)
        
        Returns:
            True si se registró correctamente
        """
        registro = {
            'timestamp': datetime.now().isoformat(),
            'numero': numero,
            'mensaje': mensaje[:50] + '...' if len(mensaje) > 50 else mensaje,
            'exitoso': exitoso,
            'motivo_error': motivo_error
        }
        
        self.historial.append(registro)
        return self._guardar_historial()
    
    def registrar_lote(self, resultados: List[Dict]) -> bool:
        """
        Registra un lote completo de envíos
        
        Args:
            resultados: Lista de diccionarios con resultados
        
        Returns:
            True si se registró correctamente
        """
        timestamp_lote = datetime.now().isoformat()
        
        for resultado in resultados:
            registro = {
                'timestamp': timestamp_lote,
                'numero': resultado.get('numero'),
                'mensaje': resultado.get('mensaje', ''),
                'exitoso': resultado.get('success', False),
                'motivo_error': resultado.get('error')
            }
            self.historial.append(registro)
        
        return self._guardar_historial()
    
    def obtener_ultimos(self, cantidad: int = 10) -> List[Dict]:
        """Obtiene los últimos N envíos"""
        return self.historial[-cantidad:]
    
    def obtener_por_numero(self, numero: str) -> List[Dict]:
        """Obtiene todos los envíos a un número específico"""
        return [r for r in self.historial if r['numero'] == numero]
    
    def obtener_por_fecha(self, fecha: str) -> List[Dict]:
        """
        Obtiene envíos de una fecha específica
        
        Args:
            fecha: Formato YYYY-MM-DD
        
        Returns:
            Lista de registros de esa fecha
        """
        return [r for r in self.historial 
                if r['timestamp'].startswith(fecha)]
    
    def obtener_estadisticas(self) -> Dict:
        """Obtiene estadísticas del historial"""
        if not self.historial:
            return {
                'total': 0,
                'exitosos': 0,
                'fallidos': 0,
                'tasa_exito': 0
            }
        
        total = len(self.historial)
        exitosos = sum(1 for r in self.historial if r.get('exitoso', False))
        fallidos = total - exitosos
        tasa_exito = (exitosos / total * 100) if total > 0 else 0
        
        return {
            'total': total,
            'exitosos': exitosos,
            'fallidos': fallidos,
            'tasa_exito': f"{tasa_exito:.1f}%"
        }
    
    def limpiar_historial(self) -> bool:
        """Limpia todo el historial"""
        respuesta = input("\n⚠️  ¿Estás seguro de que quieres borrar todo el historial? (s/n): ")
        
        if respuesta.lower() == 's':
            self.historial = []
            return self._guardar_historial()
        return False
    
    def mostrar_historial(self, cantidad: int = None):
        """Muestra el historial en pantalla"""
        print("\n" + "="*80)
        print("📋 HISTORIAL DE ENVÍOS")
        print("="*80 + "\n")
        
        if not self.historial:
            print("No hay registros en el historial\n")
            return
        
        registros = self.obtener_ultimos(cantidad) if cantidad else self.historial
        
        for i, registro in enumerate(registros, 1):
            timestamp = registro['timestamp'].split('T')[1][:8]
            estado = "✅" if registro.get('exitoso') else "❌"
            numero = registro['numero']
            mensaje = registro['mensaje']
            
            print(f"{i:3}. {estado} [{timestamp}] {numero}")
            print(f"     {mensaje}")
            
            if not registro.get('exitoso') and registro.get('motivo_error'):
                print(f"     Error: {registro['motivo_error']}")
            print()
    
    def exportar_csv(self, archivo: str = 'historial_envios.csv') -> bool:
        """Exporta el historial a CSV"""
        try:
            import csv
            
            with open(archivo, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Fecha', 'Hora', 'Número', 'Mensaje', 'Exitoso', 'Error'])
                
                for r in self.historial:
                    fecha_hora = r['timestamp'].split('T')
                    writer.writerow([
                        fecha_hora[0],
                        fecha_hora[1][:8],
                        r['numero'],
                        r['mensaje'],
                        'Sí' if r.get('exitoso') else 'No',
                        r.get('motivo_error', '')
                    ])
            
            print(f"✅ Exportado a {archivo}")
            return True
        except Exception as e:
            print(f"❌ Error al exportar: {e}")
            return False


def menu_principal():
    """Menú principal del historial"""
    try:
        print("\n" + "📊 "*20)
        print("GESTOR DE HISTORIAL DE ENVÍOS")
        print("📊 "*20 + "\n")
        
        historial = HistorialEnvios()
        
        while True:
            print("Opciones:")
            print("1. Ver últimos envíos")
            print("2. Ver estadísticas")
            print("3. Buscar por número")
            print("4. Buscar por fecha")
            print("5. Exportar a CSV")
            print("6. Limpiar historial")
            print("0. Salir")
            
            opcion = input("\nSelecciona una opción: ").strip()
            
            if opcion == '1':
                cantidad = input("¿Cuántos registros? [10]: ").strip()
                cantidad = int(cantidad) if cantidad else 10
                historial.mostrar_historial(cantidad)
            
            elif opcion == '2':
                stats = historial.obtener_estadisticas()
                print("\n" + "="*40)
                print("📊 ESTADÍSTICAS")
                print("="*40)
                print(f"Total de envíos: {stats['total']}")
                print(f"✅ Exitosos: {stats['exitosos']}")
                print(f"❌ Fallidos: {stats['fallidos']}")
                print(f"📈 Tasa de éxito: {stats['tasa_exito']}\n")
            
            elif opcion == '3':
                numero = input("\nIngresa el número: ").strip()
                registros = historial.obtener_por_numero(numero)
                
                if registros:
                    print(f"\n📋 {len(registros)} envíos a {numero}:\n")
                    for r in registros:
                        estado = "✅" if r.get('exitoso') else "❌"
                        print(f"{estado} {r['timestamp']}: {r['mensaje']}")
                    print()
                else:
                    print(f"\n❌ No hay registros para {numero}\n")
            
            elif opcion == '4':
                fecha = input("\nIngresa la fecha (YYYY-MM-DD): ").strip()
                registros = historial.obtener_por_fecha(fecha)
                
                if registros:
                    print(f"\n📋 {len(registros)} envíos en {fecha}:\n")
                    for r in registros:
                        estado = "✅" if r.get('exitoso') else "❌"
                        print(f"{estado} {r['numero']}: {r['mensaje']}")
                    print()
                else:
                    print(f"\n❌ No hay registros para {fecha}\n")
            
            elif opcion == '5':
                archivo = input("Nombre del archivo [historial_envios.csv]: ").strip()
                archivo = archivo or 'historial_envios.csv'
                historial.exportar_csv(archivo)
            
            elif opcion == '6':
                if historial.limpiar_historial():
                    print("✅ Historial eliminado")
            
            elif opcion == '0':
                print("👋 Adiós")
                break
            
            else:
                print("❌ Opción no válida")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelado")
        sys.exit(1)


if __name__ == "__main__":
    menu_principal()
