# ✅ CHECKLIST PASO A PASO - WINDOWS 10 + ANDROID + SMS

## PREPARACIÓN (Haz esto UNA SOLA VEZ)

### ☐ Paso 1: Instalar ADB en Windows (5 minutos)

**Opción A: Automático (RECOMENDADO)**
- ☐ Haz click derecho en: `instalar_adb_windows.bat`
- ☐ Selecciona: "Ejecutar como administrador"
- ☐ Sigue las instrucciones
- ☐ Cuando termines, cierra la ventana

**Opción B: Manual**
- ☐ Ve a: https://developer.android.com/studio/releases/platform-tools
- ☐ Descarga: "Download for Windows"
- ☐ Extrae el ZIP en `C:\`
- ☐ Resultado: `C:\platform-tools\` (con adb.exe dentro)
- ☐ Abre PowerShell como ADMINISTRADOR
- ☐ Ejecuta: `setx PATH "%PATH%;C:\platform-tools"`
- ☐ Cierra PowerShell

### ☐ Paso 2: Preparar Android (3 minutos)

En tu dispositivo Android:
- ☐ Ve a: **Ajustes > Sistema**
- ☐ Busca: **Información del dispositivo**
- ☐ Toca **"Número de compilación" 7 VECES**
- ☐ Aparecerá mensaje "Eres desarrollador"
- ☐ Ve a: **Ajustes > Sistema > Opciones de desarrollador**
- ☐ Busca: **"Depuración por USB"**
- ☐ Actívalo (enciende el switch)

### ☐ Paso 3: Conectar Android (2 minutos)

- ☐ Conecta tu Android a la PC con cable USB
- ☐ En el Android aparecerá un diálogo
- ☐ Selecciona: **"Permitir depuración USB"**
- ☐ Marca: **"Permitir desde esta computadora"** (opcional)
- ☐ Click: **OK**

### ☐ Paso 4: Verificar Conexión (1 minuto)

- ☐ Abre PowerShell o CMD
- ☐ Escribe: `adb devices`
- ☐ Deberías ver:
  ```
  List of attached devices
  XXXXXXXXXXXXXXX    device
  ```
- ☐ Si ves `device` ✅ (si ves `unauthorized`, autoriza de nuevo en Android)

---

## USA EL PROGRAMA

### ☐ Cada vez que quieras enviar SMS:

1. **Asegúrate de que Android esté conectado**
   - ☐ Cable USB conectado
   - ☐ Ejecuta: `adb devices` (debe mostrar `device`)

2. **Abre PowerShell en la carpeta del programa**
   - ☐ Navega a la carpeta o
   - ☐ Shift+Click derecho en la carpeta > "Abrir PowerShell aquí"

3. **Ejecuta el programa**
   ```bash
   python sms_sender_android.py
   ```

4. **Sigue las instrucciones**
   ```
   Número de teléfono: +34123456789
   Mensaje: Tu mensaje aquí
   ```

5. **¡SMS enviado!** ✅

---

## PROBLEMAS COMUNES

### "adb no se reconoce"
- ☐ Cierra PowerShell
- ☐ Abre una NUEVA
- ☐ Intenta: `adb version`

### "No hay dispositivos"
- ☐ Desconecta el cable
- ☐ Espera 3 segundos
- ☐ Reconecta
- ☐ Autoriza en el Android

### "unauthorized"
- ☐ En Android debe aparecer un diálogo
- ☐ Marca: "Permitir desde esta computadora"
- ☐ Click OK
- ☐ Desconecta y reconecta

### "Error al enviar SMS"
- ☐ Verifica que Android esté conectado: `adb devices`
- ☐ Intenta con otro número
- ☐ Reinicia Android

---

## VERIFICACIÓN RÁPIDA

Ejecuta esto para revisar todo:
```bash
python verificar_windows.py
```

---

## EJEMPLOS DE CÓDIGO

### Envío simple
```python
from sms_sender_android import AndroidSMSSender

sender = AndroidSMSSender()
sender.send_sms('+34123456789', 'Hola!')
```

### Envío múltiple
```python
from sms_sender_android import AndroidSMSSender

sender = AndroidSMSSender()

numeros = ['+34111111111', '+34222222222', '+34333333333']
for numero in numeros:
    sender.send_sms(numero, 'Hola a todos!')
```

### Ver ejemplos prácticos
```bash
python ejemplos_uso.py
```

---

## ARCHIVOS QUE TIENES

| Archivo | Descripción |
|---------|-------------|
| `sms_sender_android.py` | 📱 El programa principal (ÚSALO) |
| `instalar_adb_windows.bat` | ⚙️ Instalador automático de ADB |
| `verificar_windows.py` | 🔍 Verifica que todo funcione |
| `ejemplos_uso.py` | 📚 11 ejemplos de código |
| `GUIA_WINDOWS_ADB.md` | 📖 Guía completa (si necesitas ayuda) |
| `README_RAPIDO.md` | ⚡ Resumen rápido |

---

## PRÓXIMAS VECES

Después de la configuración inicial:

1. ☐ Conecta Android por USB
2. ☐ Abre PowerShell
3. ☐ Ejecuta: `python sms_sender_android.py`
4. ☐ ¡Listo!

---

## ¿NECESITAS AYUDA?

**Si algo no funciona:**

1. ☐ Ejecuta: `python verificar_windows.py`
2. ☐ Lee: `GUIA_WINDOWS_ADB.md`
3. ☐ Revisa: Sección "PROBLEMAS COMUNES" arriba

**Si todo está ✅:**

🎉 **¡Felicidades! Ya estás listo para enviar SMS desde Python!**

---

## ÚLTIMOS PASOS

1. ☐ Guarda esta lista de verificación
2. ☐ Sigue los pasos (solo toma 15 minutos)
3. ☐ ¡Empieza a enviar SMS!

**Total de tiempo de instalación: ~15-20 minutos**
