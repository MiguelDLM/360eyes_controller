#!/usr/bin/env python3
"""
Controlador PTZ Final para Cámaras IPC365
Basado en hallazgos exitosos del foro ipcamtalk.com
"""
import socket
import time
import sys

# Configuración de la cámara
CAMERA_IP = '192.168.1.68'
CAMERA_USER = 'admin'
CAMERA_PASS = 'password'
PTZ_PORT = 23456  # Puerto que funciona

# Comandos PTZ completos para IPC365 (hexadecimal)
PTZ_COMMANDS = {
    'right': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                   0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                   0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                   0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                   0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    'left': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                  0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                  0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0xfb, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    'up': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x05, 0x00, 0x00, 0x00, 
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    'down': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                  0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                  0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xfb, 0xff, 0xff, 0xff, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
    
    'stop': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                  0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                  0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                  0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                  
    # Comandos de zoom (experimentales)
    'zoom_in': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                     0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                     0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                     0x05, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                     0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]),
                     
    'zoom_out': bytes([0xcc, 0xdd, 0xee, 0xff, 0x77, 0x4f, 0x00, 0x00, 0xe3, 0x12, 0x69, 0x00, 
                      0x48, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xaf, 0x93, 0xc6, 0x3b, 
                      0x09, 0xf7, 0x4b, 0x01, 0x01, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                      0xfb, 0xff, 0xff, 0xff, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
                      0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
}

class IPC365PTZController:
    def __init__(self, ip, port, timeout=5):
        self.ip = ip
        self.port = port
        self.timeout = timeout
        
    def send_command(self, command_name, duration=0.5):
        """Envía un comando PTZ a la cámara"""
        if command_name not in PTZ_COMMANDS:
            print(f"❌ Comando '{command_name}' no válido")
            return False
            
        try:
            # Conectar y enviar comando
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(self.timeout)
            sock.connect((self.ip, self.port))
            
            command_bytes = PTZ_COMMANDS[command_name]
            bytes_sent = sock.send(command_bytes)
            
            print(f"  ✅ Comando '{command_name}' enviado ({bytes_sent} bytes)")
            
            # Para comandos de movimiento, enviar stop después de la duración
            if command_name in ['right', 'left', 'up', 'down', 'zoom_in', 'zoom_out'] and duration > 0:
                time.sleep(duration)
                # Enviar comando stop
                stop_bytes = PTZ_COMMANDS['stop']
                sock.send(stop_bytes)
                print(f"  🛑 Comando STOP enviado")
            
            sock.close()
            return True
            
        except Exception as e:
            print(f"❌ Error enviando comando '{command_name}': {e}")
            return False
    
    def test_all_commands(self):
        """Prueba todos los comandos PTZ disponibles"""
        print("🧪 Probando todos los comandos PTZ...")
        
        test_commands = ['right', 'left', 'up', 'down', 'zoom_in', 'zoom_out', 'stop']
        
        for cmd in test_commands:
            print(f"\n🎯 Probando comando: {cmd}")
            success = self.send_command(cmd, duration=1.0)
            
            if success and cmd != 'stop':
                response = input(f"  ❓ ¿Viste movimiento {cmd}? (s/n): ").lower()
                if response == 's':
                    print(f"  ✅ Comando {cmd} funcional")
                else:
                    print(f"  ❌ Comando {cmd} no funcional")
            
            time.sleep(1)  # Pausa entre comandos
    
    def interactive_control(self):
        """Control interactivo de la cámara PTZ"""
        print(f"\n🎮 Control PTZ Interactivo")
        print("=" * 40)
        print("Comandos disponibles:")
        print("  🔄 Movimiento: right, left, up, down")
        print("  🔍 Zoom: zoom_in, zoom_out")
        print("  🛑 Parar: stop")
        print("  🚪 Salir: quit")
        print("=" * 40)
        
        while True:
            try:
                command = input("\n🎯 Comando PTZ: ").lower().strip()
                
                if command == 'quit':
                    print("👋 Saliendo del control PTZ...")
                    break
                elif command in PTZ_COMMANDS:
                    if command == 'stop':
                        self.send_command(command)
                    else:
                        # Para comandos de movimiento, preguntar duración
                        try:
                            duration_str = input(f"  ⏱️ Duración en segundos (enter=0.5): ").strip()
                            duration = float(duration_str) if duration_str else 0.5
                        except ValueError:
                            duration = 0.5
                        
                        self.send_command(command, duration)
                else:
                    print("❌ Comando no válido")
                    print("Comandos: right, left, up, down, zoom_in, zoom_out, stop, quit")
                    
            except KeyboardInterrupt:
                print("\n👋 Saliendo...")
                break

def main():
    print("🎥 Controlador PTZ Final IPC365")
    print("=" * 50)
    print(f"📡 Cámara: {CAMERA_IP}:{PTZ_PORT}")
    print(f"👤 Usuario: {CAMERA_USER}")
    print("=" * 50)
    
    # Verificar conectividad
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((CAMERA_IP, PTZ_PORT))
        sock.close()
        
        if result == 0:
            print(f"✅ Puerto {PTZ_PORT} accesible")
        else:
            print(f"❌ Puerto {PTZ_PORT} no accesible")
            return
    except Exception as e:
        print(f"❌ Error de conectividad: {e}")
        return
    
    # Crear controlador
    controller = IPC365PTZController(CAMERA_IP, PTZ_PORT)
    
    # Menú principal
    while True:
        print("\n🎯 Opciones:")
        print("1. 🧪 Probar todos los comandos")
        print("2. 🎮 Control interactivo") 
        print("3. 🏃 Prueba rápida (derecha)")
        print("4. 🚪 Salir")
        
        try:
            choice = input("\nElige una opción (1-4): ").strip()
            
            if choice == '1':
                controller.test_all_commands()
            elif choice == '2':
                controller.interactive_control()
            elif choice == '3':
                print("🧪 Prueba rápida: movimiento derecha por 1 segundo...")
                controller.send_command('right', duration=1.0)
            elif choice == '4':
                print("👋 ¡Hasta luego!")
                break
            else:
                print("❌ Opción no válida")
                
        except KeyboardInterrupt:
            print("\n👋 Saliendo...")
            break

if __name__ == "__main__":
    main()
