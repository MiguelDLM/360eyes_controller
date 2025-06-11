# PTZ Camera Integration para Home Assistant

Integración personalizada para cámaras PTZ que soporta múltiples tipos de cámara:
- YOOSEE
- YCC365
- Y05
- **IPC365/360Eye** (NUEVO)

## Características

### Soporte IPC365/360Eye
- ✅ Comandos PTZ propietarios via TCP
- ✅ Movimientos: izquierda, derecha, arriba, abajo
- ✅ Comando stop
- ✅ Puerto configurable (por defecto: 23456)
- ✅ Timeout configurable

## Instalación

1. Copia la carpeta `ptz_camera` a `custom_components/ptz_camera/`
2. Reinicia Home Assistant
3. Los servicios estarán disponibles automáticamente

## Configuración

### Para cámaras IPC365

```yaml
# En configuration.yaml
ptz_camera:
```

## Servicios Disponibles

### ptz_camera.move_left
Mueve la cámara hacia la izquierda

```yaml
service: ptz_camera.move_left
data:
  host: "192.168.1.68"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_right
Mueve la cámara hacia la derecha

```yaml
service: ptz_camera.move_right
data:
  host: "192.168.1.68"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_up
Mueve la cámara hacia arriba

```yaml
service: ptz_camera.move_up
data:
  host: "192.168.1.68"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_down
Mueve la cámara hacia abajo

```yaml
service: ptz_camera.move_down
data:
  host: "192.168.1.68"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_to_direction
Mueve la cámara en la dirección especificada

```yaml
service: ptz_camera.move_to_direction
data:
  host: "192.168.1.68"
  camera_type: "IPC365"
  direction: "right"
  move_time: 1
```

## Parámetros

- **host**: IP de la cámara (requerido)
- **camera_type**: Tipo de cámara. Para IPC365 usar "IPC365"
- **move_time**: Tiempo de movimiento en segundos (opcional, por defecto: 0.5)

## URLs RTSP para IPC365

Las siguientes URLs RTSP funcionan con cámaras IPC365:

```
rtsp://admin:password@192.168.1.68:554/cam/realmonitor?channel=1&subtype=1
rtsp://admin:123456@192.168.1.68:554/live/ch0
rtsp://admin:123456@192.168.1.68:554/cam/realmonitor?channel=1&subtype=1
```

## Ejemplo de Automatización

```yaml
automation:
  - alias: "Control PTZ con botones"
    trigger:
      - platform: state
        entity_id: input_button.camera_left
    action:
      - service: ptz_camera.move_left
        data:
          host: "192.168.1.68"
          camera_type: "IPC365"
          move_time: 2
```

## Troubleshooting

### La cámara no se mueve
1. Verifica que la IP sea correcta
2. Asegúrate de que el puerto 23456 esté abierto
3. Confirma que `camera_type: "IPC365"` esté configurado
4. Revisa los logs de Home Assistant

### Verificar conexión
Ejecuta el script de prueba:
```bash
python test_integration.py
```

## Logs

Para habilitar logs detallados, agrega a `configuration.yaml`:

```yaml
logger:
  default: warning
  logs:
    custom_components.ptz_camera: debug
```

## Versión

- **v1.0.3**: Soporte para cámaras IPC365/360Eye
- v1.0.2: Soporte para YOOSEE, YCC365, Y05

## Créditos

Basado en el trabajo original de:
- @fjramirez1987
- @carvalr  
- @wire67

Adaptación IPC365 realizada con comandos descubiertos en el foro ipcamtalk.com
