#!/usr/bin/env python3
"""
CONFIGURACIÓN DEL SISTEMA SMS
Archivo centralizado de configuración
"""

import json
from pathlib import Path
from typing import Any, Dict


class Config:
    """Gestiona la configuración del sistema"""
    
    ARCHIVO_CONFIG = 'config.json'
    
    # Configuración por defecto
    CONFIG_DEFECTO = {
        'android': {
            'pausas': {
                'entre_mensajes': 2.0,
                'reintento': 1.0,
                'descripcion': 'Tiempo en segundos entre envíos'
            },
            'reintentos': {
                'cantidad': 2,
                'descripcion': 'Número de intentos si falla un SMS'
            }
        },
        'archivos': {
            'contactos': 'contactos.txt',
            'historial': 'historial_envios.json',
            'validados': 'contactos_validados.txt',
            'descripcion': 'Rutas de archivos importantes'
        },
        'validacion': {
            'pais': 'ES',
            'agregar_prefijo': True,
            'descripcion': 'Configuración de validación de números'
        },
        'formato_mensaje': {
            'max_caracteres': 160,
            'max_caracteres_acentos': 140,
            'descripcion': 'Límites de caracteres por SMS'
        }
    }
    
    def __init__(self):
        self.config = self._cargar_config()
    
    def _cargar_config(self) -> Dict[str, Any]:
        """Carga la configuración desde archivo o usa por defecto"""
        archivo = Path(self.ARCHIVO_CONFIG)
        
        if archivo.exists():
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"⚠️  Error al cargar config.json: {e}")
                print("   Usando configuración por defecto")
                return self.CONFIG_DEFECTO.copy()
        
        # Si no existe, crear con valores por defecto
        self._guardar_config(self.CONFIG_DEFECTO)
        return self.CONFIG_DEFECTO.copy()
    
    def _guardar_config(self, config: Dict) -> bool:
        """Guarda la configuración al archivo"""
        try:
            with open(self.ARCHIVO_CONFIG, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"❌ Error al guardar config: {e}")
            return False
    
    def obtener(self, clave: str, valor_defecto: Any = None) -> Any:
        """Obtiene un valor de la configuración"""
        claves = clave.split('.')
        valor = self.config
        
        for clave_parte in claves:
            if isinstance(valor, dict):
                valor = valor.get(clave_parte)
            else:
                return valor_defecto
        
        return valor if valor is not None else valor_defecto
    
    def establecer(self, clave: str, valor: Any) -> bool:
        """Establece un valor en la configuración"""
        claves = clave.split('.')
        config = self.config
        
        # Navegar hasta la penúltima clave
        for clave_parte in claves[:-1]:
            if clave_parte not in config:
                config[clave_parte] = {}
            config = config[clave_parte]
        
        # Establecer el valor
        config[claves[-1]] = valor
        
        return self._guardar_config(self.config)
    
    def mostrar_config(self):
        """Muestra la configuración actual"""
        print("\n" + "="*60)
        print("⚙️  CONFIGURACIÓN DEL SISTEMA")
        print("="*60 + "\n")
        
        print("Android:")
        print(f"  Pausa entre mensajes: {self.obtener('android.pausas.entre_mensajes')}s")
        print(f"  Reintentos: {self.obtener('android.reintentos.cantidad')}")
        
        print("\nArchivos:")
        print(f"  Contactos: {self.obtener('archivos.contactos')}")
        print(f"  Historial: {self.obtener('archivos.historial')}")
        
        print("\nValidación:")
        print(f"  País: {self.obtener('validacion.pais')}")
        print(f"  Agregar prefijo: {self.obtener('validacion.agregar_prefijo')}")
        
        print("\nFormato de mensaje:")
        print(f"  Máx caracteres: {self.obtener('formato_mensaje.max_caracteres')}")
        print(f"  Máx con acentos: {self.obtener('formato_mensaje.max_caracteres_acentos')}\n")
    
    def editar_config_interactiva(self):
        """Permite editar la configuración interactivamente"""
        print("\n" + "="*60)
        print("✏️  EDITAR CONFIGURACIÓN")
        print("="*60 + "\n")
        
        print("Opciones:")
        print("1. Cambiar pausa entre mensajes")
        print("2. Cambiar número de reintentos")
        print("3. Cambiar país de validación")
        print("4. Restaurar configuración por defecto")
        print("0. Volver")
        
        opcion = input("\nSelecciona (0-4): ").strip()
        
        if opcion == '1':
            try:
                pausa = float(input("\nPausa en segundos [2.0]: ") or 2.0)
                self.establecer('android.pausas.entre_mensajes', pausa)
                print(f"✅ Pausa actualizada a {pausa}s")
            except ValueError:
                print("❌ Valor inválido")
        
        elif opcion == '2':
            try:
                reintentos = int(input("\nNúmero de reintentos [2]: ") or 2)
                self.establecer('android.reintentos.cantidad', reintentos)
                print(f"✅ Reintentos actualizados a {reintentos}")
            except ValueError:
                print("❌ Valor inválido")
        
        elif opcion == '3':
            pais = input("\nCódigo de país [ES]: ").strip().upper() or 'ES'
            self.establecer('validacion.pais', pais)
            print(f"✅ País actualizado a {pais}")
        
        elif opcion == '4':
            respuesta = input("\n⚠️  ¿Restaurar configuración por defecto? (s/n): ")
            if respuesta.lower() == 's':
                self._guardar_config(self.CONFIG_DEFECTO.copy())
                self.config = self.CONFIG_DEFECTO.copy()
                print("✅ Configuración restaurada")
        
        elif opcion != '0':
            print("❌ Opción no válida")


def crear_archivo_config_inicial():
    """Crea archivo de configuración inicial si no existe"""
    config = Config()
    
    if not Path(Config.ARCHIVO_CONFIG).exists():
        print("📝 Creando archivo de configuración inicial...")
        print(f"✅ Archivo creado: {Config.ARCHIVO_CONFIG}")


def ejemplo_uso():
    """Ejemplo de cómo usar la configuración"""
    config = Config()
    
    # Obtener valores
    pausa = config.obtener('android.pausas.entre_mensajes')
    reintentos = config.obtener('android.reintentos.cantidad')
    pais = config.obtener('validacion.pais')
    
    print(f"Pausa: {pausa}s")
    print(f"Reintentos: {reintentos}")
    print(f"País: {pais}")
    
    # Establecer nuevos valores
    # config.establecer('android.pausas.entre_mensajes', 3.0)


if __name__ == "__main__":
    import sys
    
    config = Config()
    
    if len(sys.argv) > 1 and sys.argv[1] == 'editar':
        config.editar_config_interactiva()
    else:
        config.mostrar_config()
