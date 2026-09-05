# 📱 GUÍA COMPLETA: ANDROID + ADB EN WINDOWS 10

## ✅ Lo que tienes:
- ✅ Windows 10
- ✅ Python instalado
- ✅ Android
- ✅ ADB

## 🎯 Objetivo:
Enviar SMS reales desde Python usando tu dispositivo Android conectado por USB

---

## PASO 1: Instalar ADB en Windows 10

### Opción A: Instalación Manual (Recomendada)

1. **Descargar Platform Tools**
   - Ve a: https://developer.android.com/studio/releases/platform-tools
   - Click en **"Download for Windows"**
   - Se descargará un ZIP (platform-tools-latest-windows.zip)

2. **Extraer el archivo**
   - Haz click derecho en el ZIP
   - Selecciona: **"Extraer aquí"**
   - Se creará una carpeta: `platform-tools`

3. **Cambiar la carpeta a C:**
   - Corta la carpeta `platform-tools`
   - Pégala en: `C:\`
   - Resultado: `C:\platform-tools\`
   - Dentro estarás `adb.exe`, `fastboot.exe`, etc.

4. **Agregar ADB al PATH**

   **Opción 1: Línea de comandos (Rápido)**
   ```bash
   # Abre PowerShell COMO ADMINISTRADOR
   # Pega esto:
   setx PATH "%PATH%;C:\platform-tools"
   ```

   **Opción 2: Variables de entorno (Visual)**
   - Abre: **Panel de Control > Sistema > Configuración avanzada del sistema**
   - Click en: **Variables de entorno**
   - Click en: **Nuevo...** (en variables de usuario)
   - Variable: `PATH`
   - Valor: `C:\platform-tools`
   - Guarda los cambios

5. **Verificar instalación**
   - Abre una nueva **PowerShell** o **CMD**
   - Escribe: `adb version`
   - Deberías ver algo como: `Android Debug Bridge version 1.0.41`

---

## PASO 2: Preparar tu Android

### En tu dispositivo Android:

1. **Habilitar Depuración USB**
   - Ve a: **Ajustes > Sistema**
   - Busca: **"Información del dispositivo"**
   - Busca: **"Número de compilación"**
   - **Toca 7 veces** sobre "Número de compilación"
   - Aparecerá un mensaje: "Eres desarrollador"

2. **Activar opciones de desarrollador**
   - Ve a: **Ajustes > Sistema > Opciones de desarrollador**
   - Busca: **"Depuración por USB"**
   - **Actívala** (enciende el switch)

3. **Conectar el Android**
   - Conecta tu Android a la PC con **cable USB**
   - En el Android aparecerá un diálogo
   - Selecciona: **"Permitir depuración USB"**
   - Marca: **"Permitir desde esta computadora"**
   - Click: **OK**

---

## PASO 3: Verificar conexión ADB

Abre **PowerShell** o **CMD**:

```bash
adb devices
```

Deberías ver:
```
List of attached devices
XXXXXXXXXXXXXXX    device
```

Si ves `device`, está conectado. ¡Bien hecho!

Si ves `unauthorized`:
- Desconecta el cable
- Desconecta el Android en Ajustes
- Vuelve a conectar
- Autoriza nuevamente en el Android

---

## PASO 4: Ejecutar el programa Python

### 1. Abre PowerShell en la carpeta donde esté el programa

```bash
# Opción 1: Navega a la carpeta
cd C:\Users\TuUsuario\Desktop

# Opción 2: O abre la carpeta y presiona Shift+Click derecho > Abrir PowerShell aquí
```

### 2. Verifica que esté conectado
```bash
adb devices
```

### 3. Ejecuta el programa
```bash
python sms_sender_android.py
```

### 4. Sigue las instrucciones
```
=== Dispositivos Android conectados ===
   1. XXXXXXXXXXXXXXX

========================================

📲 ENVIAR SMS
Número de teléfono: +34123456789
Mensaje: Hola, este es un mensaje de prueba

📱 Enviando SMS...
   Dispositivo: XXXXXXXXXXXXXXX
   Número: +34123456789
   Mensaje: Hola, este es un mensaje de prueba
✅ SMS enviado exitosamente
```

---

## PASO 5: Ejemplo de uso desde Python

Si quieres usar el código desde otra aplicación Python:

```python
from sms_sender_android import AndroidSMSSender

# Crear el enviador
sender = AndroidSMSSender()

# Enviar un SMS
sender.send_sms('+34123456789', 'Hola desde Python!')
```

O en un script automatizado:

```python
#!/usr/bin/env python3
from sms_sender_android import AndroidSMSSender

sender = AndroidSMSSender()

# Lista de números a enviar
numeros = [
    '+34111111111',
    '+34222222222',
    '+34333333333'
]

mensaje = 'Notificación importante'

# Enviar a todos
for numero in numeros:
    resultado = sender.send_sms(numero, mensaje)
    if resultado:
        print(f"✅ Enviado a {numero}")
    else:
        print(f"❌ Error en {numero}")
```

---

## SOLUCIÓN DE PROBLEMAS EN WINDOWS

### Error: "adb no reconocido"
```
'adb' no se reconoce como un comando interno o externo
```

**Solución:**
1. Verifica que instalaste ADB en `C:\platform-tools\`
2. Ejecuta: `setx PATH "%PATH%;C:\platform-tools"` (como admin)
3. **Cierra y reabre PowerShell**
4. Intenta de nuevo

### Error: "No hay dispositivos conectados"
```
List of attached devices
(no devices attached)
```

**Solución:**
1. Desconecta el cable USB
2. Habilita Depuración USB nuevamente en el Android
3. Reconecta el cable
4. Autoriza el dispositivo cuando aparezca el diálogo

### Error: "unauthorized"
```
List of attached devices
XXXXXXXXXXXXXXX    unauthorized
```

**Solución:**
1. En el Android, irá un diálogo de autorización
2. Marca: "Permitir desde esta computadora"
3. Click: OK
4. Desconecta y reconecta el cable

### Error: "offline"
```
XXXXXXXXXXXXXXX    offline
```

**Solución:**
1. Desconecta el cable
2. Espera 5 segundos
3. Reconecta
4. Ejecuta: `adb kill-server` y luego `adb devices`

---

## COMANDOS ADB ÚTILES

```bash
# Ver dispositivos conectados
adb devices

# Ver logs en tiempo real
adb logcat

# Instalar una app
adb install C:\ruta\a\app.apk

# Desinstalar una app
adb uninstall com.app.nombre

# Abrir un shell en el Android
adb shell

# Ver lista de SMS (si tienes permisos)
adb shell content query --uri content://sms/

# Reiniciar el dispositivo
adb reboot

# Apagar el dispositivo
adb shell reboot -p
```

---

## SCRIPT PARA VERIFICAR TODO

Crea un archivo llamado `verificar.ps1` en PowerShell:

```powershell
# Verificar ADB
Write-Host "Verificando ADB..." -ForegroundColor Cyan
$adb = adb version
if ($adb) {
    Write-Host "✅ ADB encontrado" -ForegroundColor Green
} else {
    Write-Host "❌ ADB no encontrado" -ForegroundColor Red
    exit
}

# Verificar dispositivos
Write-Host "`nVerificando dispositivos..." -ForegroundColor Cyan
$devices = adb devices
if ($devices -match "device$") {
    Write-Host "✅ Dispositivo conectado" -ForegroundColor Green
    Write-Host $devices
} else {
    Write-Host "❌ No hay dispositivos conectados" -ForegroundColor Red
}

# Verificar Python
Write-Host "`nVerificando Python..." -ForegroundColor Cyan
$python = python --version
if ($python) {
    Write-Host "✅ Python encontrado: $python" -ForegroundColor Green
} else {
    Write-Host "❌ Python no encontrado" -ForegroundColor Red
}
```

Ejecuta: `powershell -ExecutionPolicy Bypass -File verificar.ps1`

---

## PASOS RÁPIDOS (RESUMEN)

```
1. Descargar Platform Tools: https://developer.android.com/studio/releases/platform-tools
2. Extraer en C:\platform-tools\
3. Agregar al PATH (setx PATH "%PATH%;C:\platform-tools")
4. Reiniciar PowerShell
5. Habilitar Depuración USB en Android
6. Conectar Android por USB
7. Autorizar en el diálogo del Android
8. Verificar: adb devices
9. Ejecutar: python sms_sender_android.py
10. ¡Listo! Empieza a enviar SMS
```

---

## EJEMPLO COMPLETO PASO A PASO

```powershell
# 1. Abre PowerShell como administrador
# 2. Instala ADB
setx PATH "%PATH%;C:\platform-tools"

# 3. Cierra y reabre PowerShell
# 4. Verifica
adb version

# 5. Conecta Android por USB
# 6. Autoriza en el diálogo
# 7. Verifica conexión
adb devices

# 8. Navega a donde está el programa
cd C:\Users\TuUsuario\Desktop

# 9. Ejecuta
python sms_sender_android.py

# 10. Sigue las instrucciones en pantalla
```

---

## PREGUNTAS FRECUENTES

**P: ¿Necesito permisos de administrador?**
R: Solo para agregar ADB al PATH. Después no.

**P: ¿Funciona si desconecto el Android?**
R: No, el Android debe estar conectado por USB.

**P: ¿Puedo enviar SMS gratis?**
R: Sí, usa tu plan de datos o SMS del teléfono normalmente.

**P: ¿Puedo automatizar esto?**
R: Sí, ejecuta el script Python en un programador de tareas.

**P: ¿Es seguro?**
R: Sí, solo accede a la funcionalidad de SMS del Android.

---

## SOPORTE

Si tienes problemas:

1. Verifica que ADB esté en PATH: `adb version`
2. Verifica que el Android esté conectado: `adb devices`
3. Verifica que Python esté instalado: `python --version`
4. Revisa los logs del Android: `adb logcat`

¡Estás listo para enviar SMS desde Python! 🚀
