#!/usr/bin/env python3
"""
EJEMPLOS PRÁCTICOS: Cómo usar sms_sender_android.py
Copia y pega lo que necesites
"""

from sms_sender_android import AndroidSMSSender


# ========== EJEMPLO 1: ENVÍO SIMPLE ==========
def ejemplo_1_envio_simple():
    """El uso más básico: enviar un SMS"""
    
    sender = AndroidSMSSender()
    
    # Enviar un SMS
    resultado = sender.send_sms('+34123456789', 'Hola, esto es un SMS')
    
    if resultado:
        print("✅ SMS enviado!")
    else:
        print("❌ Error al enviar")


# ========== EJEMPLO 2: ENVÍO A MÚLTIPLES NÚMEROS ==========
def ejemplo_2_envio_multiple():
    """Enviar el mismo SMS a varios números"""
    
    sender = AndroidSMSSender()
    
    numeros = [
        '+34111111111',
        '+34222222222',
        '+34333333333',
    ]
    
    mensaje = 'Hola a todos! Este es un mensaje importante'
    
    for numero in numeros:
        print(f"Enviando a {numero}...")
        resultado = sender.send_sms(numero, mensaje)
        
        if resultado:
            print(f"  ✅ Enviado")
        else:
            print(f"  ❌ Error")


# ========== EJEMPLO 3: ENVÍO CON CONFIRMACIÓN ==========
def ejemplo_3_con_confirmacion():
    """Pedir confirmación antes de enviar"""
    
    sender = AndroidSMSSender()
    
    # Obtener datos del usuario
    numero = input("Número de teléfono: ").strip()
    mensaje = input("Mensaje: ").strip()
    
    # Confirmar
    print(f"\n📱 Vas a enviar:")
    print(f"   A: {numero}")
    print(f"   Mensaje: {mensaje}")
    
    confirmacion = input("\n¿Confirmas? (s/n): ").strip().lower()
    
    if confirmacion == 's':
        resultado = sender.send_sms(numero, mensaje)
        
        if resultado:
            print("✅ SMS enviado exitosamente")
        else:
            print("❌ Error al enviar")
    else:
        print("Cancelado")


# ========== EJEMPLO 4: ENVÍO CON LÍMITE DE CARACTERES ==========
def ejemplo_4_con_limite():
    """SMS respeta límites de caracteres"""
    
    sender = AndroidSMSSender()
    
    numero = '+34123456789'
    
    # SMS de 160 caracteres (límite estándar)
    mensaje_largo = "A" * 200  # Mensaje más largo que el límite
    
    # El mensaje será truncado automáticamente
    # o puedes hacerlo tú mismo
    
    if len(mensaje_largo) > 160:
        mensaje_corto = mensaje_largo[:160]
        print("⚠️  Mensaje truncado a 160 caracteres")
    else:
        mensaje_corto = mensaje_largo
    
    sender.send_sms(numero, mensaje_corto)


# ========== EJEMPLO 5: NOTIFICACIONES AUTOMÁTICAS ==========
def ejemplo_5_notificaciones():
    """Enviar notificaciones en tiempo real"""
    
    import time
    
    sender = AndroidSMSSender()
    
    # Simulación: enviar notificaciones cada 5 minutos
    while True:
        try:
            numero = '+34123456789'
            timestamp = time.strftime('%H:%M:%S')
            
            mensaje = f"Notificación: {timestamp} - Sistema funcionando"
            
            print(f"[{timestamp}] Enviando notificación...")
            sender.send_sms(numero, mensaje)
            
            print("✅ Notificación enviada")
            
            # Esperar 5 minutos (300 segundos)
            # Cambia a 60 para 1 minuto (testing)
            print("Esperando 5 minutos para la próxima...")
            time.sleep(300)
            
        except KeyboardInterrupt:
            print("\n⏹️  Notificaciones detenidas")
            break


# ========== EJEMPLO 6: LEER DESDE ARCHIVO ==========
def ejemplo_6_desde_archivo():
    """Leer números y mensajes desde un archivo"""
    
    sender = AndroidSMSSender()
    
    # Crea un archivo llamado "numeros.txt" con:
    # +34111111111,Hola 1
    # +34222222222,Hola 2
    # +34333333333,Hola 3
    
    try:
        with open('numeros.txt', 'r') as f:
            for linea in f:
                linea = linea.strip()
                if not linea or linea.startswith('#'):
                    continue
                
                # Formato: numero,mensaje
                partes = linea.split(',')
                if len(partes) != 2:
                    print(f"❌ Línea inválida: {linea}")
                    continue
                
                numero, mensaje = partes
                numero = numero.strip()
                mensaje = mensaje.strip()
                
                print(f"Enviando a {numero}...")
                resultado = sender.send_sms(numero, mensaje)
                
                if resultado:
                    print("  ✅ Enviado")
                else:
                    print("  ❌ Error")
    
    except FileNotFoundError:
        print("❌ Archivo 'numeros.txt' no encontrado")


# ========== EJEMPLO 7: ENVÍO CON MANEJO DE ERRORES ==========
def ejemplo_7_con_errores():
    """Manejo robusto de errores"""
    
    try:
        sender = AndroidSMSSender()
        
        # Validar entrada
        numero = input("Número: ").strip()
        mensaje = input("Mensaje: ").strip()
        
        # Validaciones
        if not numero:
            print("❌ El número no puede estar vacío")
            return
        
        if not mensaje:
            print("❌ El mensaje no puede estar vacío")
            return
        
        if len(mensaje) > 160:
            print(f"⚠️  Mensaje truncado de {len(mensaje)} a 160 caracteres")
            mensaje = mensaje[:160]
        
        # Enviar
        resultado = sender.send_sms(numero, mensaje)
        
        if resultado:
            print("✅ SMS enviado")
        else:
            print("❌ Error al enviar")
    
    except Exception as e:
        print(f"❌ Error inesperado: {e}")


# ========== EJEMPLO 8: OBTENER DISPOSITIVOS DISPONIBLES ==========
def ejemplo_8_dispositivos():
    """Ver qué dispositivos están disponibles"""
    
    sender = AndroidSMSSender()
    
    dispositivos = sender.get_connected_devices()
    
    if dispositivos:
        print("✅ Dispositivos conectados:")
        for i, device in enumerate(dispositivos, 1):
            print(f"   {i}. {device}")
    else:
        print("❌ No hay dispositivos conectados")


# ========== EJEMPLO 9: MENSAJE PERSONALIZADO ==========
def ejemplo_9_personalizado():
    """Personalizar mensajes para cada número"""
    
    sender = AndroidSMSSender()
    
    # Diccionario de nombres y números
    contactos = {
        'Juan': '+34111111111',
        'María': '+34222222222',
        'Pedro': '+34333333333',
    }
    
    # Enviar mensaje personalizado a cada uno
    for nombre, numero in contactos.items():
        mensaje = f"Hola {nombre}, este es un mensaje personalizado para ti"
        
        print(f"Enviando a {nombre}...")
        resultado = sender.send_sms(numero, mensaje)
        
        if resultado:
            print(f"  ✅ Enviado a {nombre}")
        else:
            print(f"  ❌ Error al enviar a {nombre}")


# ========== EJEMPLO 10: INTEGRACIÓN CON OTRAS APPS ==========
def ejemplo_10_integracion():
    """Usar en una función dentro de otra app"""
    
    def enviar_codigo_verificacion(numero: str, codigo: str) -> bool:
        """Envía un código de verificación por SMS"""
        
        try:
            sender = AndroidSMSSender()
            
            mensaje = f"Tu código de verificación es: {codigo}"
            
            resultado = sender.send_sms(numero, mensaje)
            
            return resultado
        
        except Exception as e:
            print(f"Error: {e}")
            return False
    
    # Uso
    if enviar_codigo_verificacion('+34123456789', '123456'):
        print("✅ Código enviado")
    else:
        print("❌ Error al enviar código")


# ========== EJEMPLO 11: ENVÍO PROGRAMADO ==========
def ejemplo_11_programado():
    """Enviar SMS a una hora específica"""
    
    import time
    from datetime import datetime, timedelta
    
    sender = AndroidSMSSender()
    
    numero = '+34123456789'
    mensaje = 'Este es un SMS programado'
    
    # Enviar en 10 segundos (para testing)
    # Para producción, cambia a 3600 (1 hora), 86400 (1 día), etc.
    
    segundos_espera = 10
    
    print(f"SMS será enviado en {segundos_espera} segundos...")
    
    for i in range(segundos_espera, 0, -1):
        print(f"  Esperando: {i}s", end='\r')
        time.sleep(1)
    
    print("\n✉️  Enviando...")
    resultado = sender.send_sms(numero, mensaje)
    
    if resultado:
        print("✅ SMS enviado")
    else:
        print("❌ Error al enviar")


# ========== MENÚ PRINCIPAL ==========
def menu():
    """Menú para elegir ejemplo"""
    
    ejemplos = {
        '1': ('Envío simple', ejemplo_1_envio_simple),
        '2': ('Envío múltiple', ejemplo_2_envio_multiple),
        '3': ('Con confirmación', ejemplo_3_con_confirmacion),
        '4': ('Con límite de caracteres', ejemplo_4_con_limite),
        '5': ('Notificaciones automáticas', ejemplo_5_notificaciones),
        '6': ('Desde archivo', ejemplo_6_desde_archivo),
        '7': ('Con manejo de errores', ejemplo_7_con_errores),
        '8': ('Ver dispositivos', ejemplo_8_dispositivos),
        '9': ('Mensaje personalizado', ejemplo_9_personalizado),
        '10': ('Integración con apps', ejemplo_10_integracion),
        '11': ('Envío programado', ejemplo_11_programado),
    }
    
    print("\n" + "="*50)
    print("EJEMPLOS DE USO - ENVIAR SMS CON ANDROID")
    print("="*50)
    
    for key, (nombre, _) in ejemplos.items():
        print(f"{key:2}. {nombre}")
    
    print("0. Salir")
    
    choice = input("\nSelecciona un ejemplo (0-11): ").strip()
    
    if choice in ejemplos:
        nombre, func = ejemplos[choice]
        print(f"\n▶️  Ejecutando: {nombre}")
        print("-"*50)
        try:
            func()
        except Exception as e:
            print(f"❌ Error: {e}")
    elif choice == '0':
        print("👋 Adiós!")
    else:
        print("❌ Opción no válida")


if __name__ == "__main__":
    # Descomenta el ejemplo que quieras usar
    
    # ejemplo_1_envio_simple()
    # ejemplo_2_envio_multiple()
    # ejemplo_3_con_confirmacion()
    
    # O usa el menú interactivo
    menu()
