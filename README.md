# PTZ Camera Integration for Home Assistant

Custom Home Assistant integration for controlling **IPC365/360Eye** PTZ cameras using proprietary TCP commands.

## Description

This integration provides Home Assistant services to control PTZ (Pan-Tilt-Zoom) movements for IPC365/360Eye cameras. It uses proprietary TCP commands to communicate directly with the camera, enabling precise movements and complete control from Home Assistant.

## Features

- ✅ **Complete PTZ control**: Movement in all directions (left, right, up, down)
- ✅ **Stop command**: Immediately stops camera movement
- ✅ **TCP communication**: Direct connection using proprietary commands
- ✅ **Configurable port**: Customizable TCP port (default: 23456)
- ✅ **Configurable timeout**: Connection timeout control
- ✅ **Adjustable movement time**: Precise control of movement duration
- ✅ **Native integration**: Services automatically available in Home Assistant
- ✅ **Automation compatible**: Easy integration with scripts and automations

## Compatibility

- **Supported cameras**: IPC365, 360Eye
- **Protocol**: TCP with proprietary commands
- **Default port**: 23456
- **Home Assistant**: Recent versions (tested with 2025.5.3)

## Installation

1. Download or clone this repository
2. Copy the complete `ptz_camera` folder to your Home Assistant `custom_components/` directory:
   ```
   /config/custom_components/ptz_camera/
   ```
3. Restart Home Assistant
4. PTZ services will be automatically available

## Configuration

### Basic Configuration

The integration requires no additional configuration in `configuration.yaml`. Services are automatically registered when Home Assistant starts.

### Optional Configuration

If you want to enable detailed logs for debugging:

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.ptz_camera: debug
```

## Available Services

### ptz_camera.move_left
Moves the camera to the left

```yaml
service: ptz_camera.move_left
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_right
Moves the camera to the right

```yaml
service: ptz_camera.move_right
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_up
Moves the camera upward

```yaml
service: ptz_camera.move_up
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_down
Moves the camera downward

```yaml
service: ptz_camera.move_down
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
  move_time: 1
```

### ptz_camera.move_to_direction
Moves the camera in the specified direction

```yaml
service: ptz_camera.move_to_direction
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
  direction: "right"  # Options: "left", "right", "up", "down"
  move_time: 1
```

### ptz_camera.stop
Stops any camera movement

```yaml
service: ptz_camera.stop
data:
  host: "192.168.1.2"
  camera_type: "IPC365"
```

## Parameters

| Parameter | Type | Required | Description | Default Value |
|-----------|------|----------|-------------|---------------|
| `host` | string | ✅ | Camera IP address | - |
| `camera_type` | string | ✅ | Camera type (use "IPC365") | - |
| `move_time` | float | ❌ | Movement time in seconds | 0.5 |
| `direction` | string | ❌* | Direction for move_to_direction | - |

*Required only for `move_to_direction` service

## Streaming Integration

### RTSP URLs for IPC365

You can use these RTSP URLs to view the camera in Home Assistant:

```yaml
# configuration.yaml
camera:
  - platform: generic
    still_image_url: http://192.168.1.2/snapshot.jpg
    stream_source: rtsp://admin:password@192.168.1.2:554/cam/realmonitor?channel=1&subtype=1
    name: "IPC365 PTZ Camera"
```

**Common RTSP URLs:**
- `rtsp://admin:password@192.168.1.2:554/cam/realmonitor?channel=1&subtype=1`
- `rtsp://admin:password@192.168.1.2:554/live/ch0`

### ONVIF 


## Usage Examples

### Manual Control with Buttons

```yaml
type: picture-elements
camera_image: camera.ipc365_axxon0
camera_view: live
title: Garden
elements:
  - type: icon
    icon: mdi:chevron-up
    style:
      top: 5%
      left: 50%
      transform: translate(-50%, -50%)
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      border-radius: 50%
      padding: 8px
    tap_action:
      action: call-service
      service: ptz_camera.move_up
      service_data:
        host: 192.168.1.2
        camera_type: IPC365
        move_time: 0.5
  - type: icon
    icon: mdi:chevron-down
    style:
      top: 95%
      left: 50%
      transform: translate(-50%, -50%)
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      border-radius: 50%
      padding: 8px
    tap_action:
      action: call-service
      service: ptz_camera.move_down
      service_data:
        host: 192.168.1.2
        camera_type: IPC365
        move_time: 0.5
  - type: icon
    icon: mdi:chevron-left
    style:
      top: 50%
      left: 5%
      transform: translate(-50%, -50%)
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      border-radius: 50%
      padding: 8px
    tap_action:
      action: call-service
      service: ptz_camera.move_left
      service_data:
        host: 192.168.1.2
        camera_type: IPC365
        move_time: 0.5
  - type: icon
    icon: mdi:chevron-right
    style:
      top: 50%
      left: 95%
      transform: translate(-50%, -50%)
      color: white
      background-color: rgba(0, 0, 0, 0.5)
      border-radius: 50%
      padding: 8px
    tap_action:
      action: call-service
      service: ptz_camera.move_right
      service_data:
        host: 192.168.1.2
        camera_type: IPC365
        move_time: 0.5

```

### Automation with Sensors

```yaml
# automation.yaml
- alias: "Follow hallway movement"
  trigger:
    - platform: state
      entity_id: binary_sensor.motion_hallway_left
      to: "on"
  action:
    - service: ptz_camera.move_left
      data:
        host: "192.168.1.2"
        camera_type: "IPC365"
        move_time: 3
    - delay: "00:00:05"
    - service: ptz_camera.stop
      data:
        host: "192.168.1.2"
        camera_type: "IPC365"
```


## Troubleshooting

### Camera doesn't respond
1. **Verify network connection**: Ensure the camera is accessible from Home Assistant
   ```bash
   ping 192.168.1.2
   ```

2. **Confirm TCP port**: Port 23456 must be open on the camera
   ```bash
   telnet 192.168.1.2 23456
   ```

3. **Verify configuration**: Make sure to use `camera_type: "IPC365"`

4. **Check logs**: Enable debug logs and review errors in Home Assistant

### Erratic movements
- Adjust the `move_time` parameter for more precise movements
- Use the `stop` service to halt unwanted movements
- Verify that multiple services aren't running simultaneously

### Connection issues
- Verify the camera isn't being controlled by another application
- Ensure camera firmware is compatible
- Check camera network configuration

## Development and Debugging

### Enable Detailed Logs

```yaml
# configuration.yaml
logger:
  default: warning
  logs:
    custom_components.ptz_camera: debug
```

### Log Structure
Logs include information about:
- Established TCP connections
- Commands sent to camera
- Received responses
- Connection or timeout errors

## Technical Information

- **Protocol**: TCP with IPC365 proprietary commands
- **Default port**: 23456
- **Timeout**: Configurable (default: 5 seconds)
- **Supported commands**: Basic PTZ (pan, tilt, stop)
- **Other camera types**: Other models from the IPC365 family may work, but this integration is primarily tested with IPC365/360Eye (EC107-B3Y2)
- **Other probable models (not tested)**: 360, gesee, Mibao, Other, P450, PW2C1806E-GTY, PW2K2N06E-GTWY, VICTURE, ey-wf0358weus

## Version

**v1.0.0** - Initial release with basic PTZ control features.

## Credits

Developed based on the discovery of IPC365 PTZ commands and protocol documentation available on ipcamtalk.com by the user @RoseGold

**References:**
- PTZ commands discovered on [ipcamtalk.com](https://ipcamtalk.com/threads/url-for-generic-ipc365-ip-camera-to-be-used-with-ispy.44633/)
- IPC365 protocol documentation

---

**Note**: This integration is specifically designed for IPC365/360Eye cameras. For other PTZ camera types, consider using official integrations or compatible alternatives.
