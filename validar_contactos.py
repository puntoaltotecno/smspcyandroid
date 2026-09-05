#!/usr/bin/env python3
"""
VALIDADOR Y GENERADOR DE CONTACTOS
Valida números de teléfono y genera archivos de contactos
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


class ValidadorContactos:
    """Valida y procesa números de teléfono"""
    
    # Patrones de validación
    PATRON_ESPAÑA = r'^(\+34|34|0)?[6789]\d{8}$'  # España
    PATRON_GENERICO = r'^\+?[1-9]\d{1,14}$'  # Internacional
    
    def __init__(self, pais: str = 'ES'):
        """
        Inicializa el validador
        
        Args:
            pais: Código del país (ES, MX, AR, etc.) - ahora solo ES
        """
        self.pais = pais
    
    def validar_numero(self, numero: str, agregar_prefijo: bool = True) -> Tuple[bool, str]:
        """
        Valida un número de teléfono
        
        Args:
            numero: Número a validar
            agregar_prefijo: Si debe agregar +34 a números españoles
        
        Returns:
            Tupla (válido, número_formateado)
        """
        numero = numero.strip()
        
        if not numero:
            return False, "Número vacío"
        
        # Limpiar caracteres especiales (excepto +)
        numero_limpio = re.sub(r'[\s\-\(\)\.]+', '', numero)
        
        # Validar según país
        if self.pais == 'ES':
            return self._validar_españa(numero_limpio, agregar_prefijo)
        else:
            return self._validar_generico(numero_limpio, agregar_prefijo)
    
    def _validar_españa(self, numero: str, agregar_prefijo: bool) -> Tuple[bool, str]:
        """Valida números españoles"""
        
        # Remover +34 o 34 al inicio
        if numero.startswith('+34'):
            numero = numero[3:]
        elif numero.startswith('34'):
            numero = numero[2:]
        elif numero.startswith('0'):
            numero = numero[1:]
        
        # Validar que sea un móvil o teléfono español
        if not re.match(r'^[6789]\d{8}$', numero):
            return False, "Formato inválido para España"
        
        # Formatear
        if agregar_prefijo:
            numero_formateado = f"+34{numero}"
        else:
            numero_formateado = numero
        
        return True, numero_formateado
    
    def _validar_generico(self, numero: str, agregar_prefijo: bool) -> Tuple[bool, str]:
        """Valida números internacionales"""
        
        # Debe tener + al inicio
        if not numero.startswith('+'):
            numero = f"+{numero}"
        
        if re.match(self.PATRON_GENERICO, numero):
            return True, numero
        else:
            return False, "Formato internacional inválido"
    
    @staticmethod
    def limpiar_numero(numero: str) -> str:
        """Limpia caracteres especiales de un número"""
        return re.sub(r'[\s\-\(\)\.]+', '', numero)


class GeneradorContactos:
    """Genera archivos de contactos"""
    
    def __init__(self, validador: ValidadorContactos = None):
        self.validador = validador or ValidadorContactos()
        self.contactos_validos = []
        self.contactos_invalidos = []
    
    def procesar_lista(self, lineas: List[str]) -> Tuple[int, int]:
        """
        Procesa una lista de líneas con contactos
        
        Formato esperado:
        - número|mensaje
        - número , mensaje
        - solo número (genera mensaje vacío)
        
        Returns:
            Tupla (válidos, inválidos)
        """
        self.contactos_validos = []
        self.contactos_invalidos = []
        
        for num_linea, linea in enumerate(linea.strip() for linea in lineas if linea.strip()):
            if linea.startswith('#'):
                continue
            
            # Intentar parsear
            if '|' in linea:
                numero, mensaje = linea.split('|', 1)
                numero = numero.strip()
                mensaje = mensaje.strip()
            elif ',' in linea:
                numero, mensaje = linea.split(',', 1)
                numero = numero.strip()
                mensaje = mensaje.strip()
            else:
                numero = linea.strip()
                mensaje = ''
            
            # Validar número
            valido, numero_formateado = self.validador.validar_numero(numero)
            
            if valido:
                self.contactos_validos.append((numero_formateado, mensaje))
            else:
                self.contactos_invalidos.append((numero, numero_formateado))
        
        return len(self.contactos_validos), len(self.contactos_invalidos)
    
    def guardar_contactos(self, archivo: str) -> bool:
        """Guarda los contactos válidos en un archivo"""
        try:
            with open(archivo, 'w', encoding='utf-8') as f:
                # Encabezado
                f.write("# Contactos validados automáticamente\n")
                f.write(f"# Total: {len(self.contactos_validos)} contactos\n\n")
                
                # Datos
                for numero, mensaje in self.contactos_validos:
                    if mensaje:
                        f.write(f"{numero}|{mensaje}\n")
                    else:
                        f.write(f"{numero}|\n")
            
            return True
        except Exception as e:
            print(f"❌ Error al guardar: {e}")
            return False
    
    def mostrar_reporte(self):
        """Muestra un reporte del procesamiento"""
        print("\n" + "="*60)
        print("📊 REPORTE DE VALIDACIÓN")
        print("="*60)
        
        print(f"\n✅ Válidos: {len(self.contactos_validos)}")
        for numero, mensaje in self.contactos_validos[:5]:
            msg_display = mensaje[:30] + "..." if len(mensaje) > 30 else mensaje
            print(f"   • {numero} | {msg_display}")
        
        if len(self.contactos_validos) > 5:
            print(f"   ... y {len(self.contactos_validos) - 5} más")
        
        if self.contactos_invalidos:
            print(f"\n❌ Inválidos: {len(self.contactos_invalidos)}")
            for numero, motivo in self.contactos_invalidos[:5]:
                print(f"   • {numero} ({motivo})")
            
            if len(self.contactos_invalidos) > 5:
                print(f"   ... y {len(self.contactos_invalidos) - 5} más")
        
        print()


def main():
    """Función principal"""
    try:
        print("\n" + "✓ "*20)
        print("VALIDADOR DE CONTACTOS Y GENERADOR")
        print("✓ "*20 + "\n")
        
        # Crear validador y generador
        validador = ValidadorContactos(pais='ES')
        generador = GeneradorContactos(validador)
        
        # Opción 1: Validar archivo existente
        print("Opciones:")
        print("1. Validar contactos.txt")
        print("2. Ingresar números manualmente")
        print("3. Validar un número")
        
        opcion = input("\nSelecciona (1-3): ").strip()
        
        if opcion == '1':
            # Validar archivo existente
            archivo = 'contactos.txt'
            if Path(archivo).exists():
                print(f"\n📂 Leyendo {archivo}...")
                with open(archivo, 'r', encoding='utf-8') as f:
                    lineas = f.readlines()
                
                validos, invalidos = generador.procesar_lista(lineas)
                
                generador.mostrar_reporte()
                
                if invalidos > 0:
                    respuesta = input("¿Guardar solo los válidos en contactos_validados.txt? (s/n): ")
                    if respuesta.lower() == 's':
                        generador.guardar_contactos('contactos_validados.txt')
                        print("✅ Guardado en contactos_validados.txt")
        
        elif opcion == '2':
            # Ingresar manualmente
            print("\nIngresa números (vacío para terminar):")
            print("Formato: numero|mensaje o solo numero")
            
            lineas = []
            while True:
                linea = input("> ").strip()
                if not linea:
                    break
                lineas.append(linea)
            
            if lineas:
                validos, invalidos = generador.procesar_lista(lineas)
                generador.mostrar_reporte()
                
                if validos > 0:
                    respuesta = input("\n¿Guardar en contactos_nuevo.txt? (s/n): ")
                    if respuesta.lower() == 's':
                        generador.guardar_contactos('contactos_nuevo.txt')
                        print("✅ Guardado en contactos_nuevo.txt")
        
        elif opcion == '3':
            # Validar un solo número
            numero = input("\nIngresa un número: ").strip()
            valido, resultado = validador.validar_numero(numero)
            
            if valido:
                print(f"\n✅ Válido: {resultado}")
            else:
                print(f"\n❌ Inválido: {resultado}")
        
        else:
            print("❌ Opción no válida")
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Cancelado")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
