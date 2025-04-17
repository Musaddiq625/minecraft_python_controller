import sys
import subprocess

GREEN = '\033[92m'
RED = '\x1b[31;20m'
ORANGE = "\033[38;5;214m"
RESET = '\033[0m' 

def success_text(text):
    return print(f'{GREEN}{text}{RESET}')

def error_text(text):
    return print(f'{RED}{text}{RESET}')

def info_text(text):
    return print(f'{ORANGE}{text}{RESET}')

def verify_and_import():
    required_packages = {
        "socket": None,
        "json": None,
        "time": None,
        "threading": None,
        "ctypes": None,
        "sys": None,
        "pynput": "pynput",
        "psutil": None,
    }

    installed_new_package = False

    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            if package:
                info_text(f"Module '{module}' is missing. Installing '{package}'...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                installed_new_package = True  # Mark that we installed something
            else:
                error_text(f"Module '{module}' is missing and is a built-in module. Check your Python installation.")

    if installed_new_package:
        success_text("\nPackages were installed. Rerun the script please...\n")
        sys.exit(0)

# Run verification before proceeding
verify_and_import()

# Now, safely import the modules
import socket
import json
import time
import psutil
import threading
import ctypes
from pynput.keyboard import Controller as KeyboardController, Key
from pynput.mouse import Button, Controller as MouseController

keyboard_controller = KeyboardController()
mouse = MouseController()
PROGRAM = 'Minecraft'
UDP_IP = '0.0.0.0'
UDP_PORT = 65432
GOOGLE_DNS = '8.8.8.8'

MOUSE_SENSITIVITY = 45.2

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect((GOOGLE_DNS, 80))
            success_text(f'Please enter this IP Address in the Controller App: \n{s.getsockname()[0]}\n')
            return True
    except Exception as e:
        error_text(f'Something went wrong! {str(e)}')
        return False

def is_minecraft_running():
    """Checks if Minecraft is currently running as an active process."""
    minecraft_names = ["minecraft", "javaw.exe", "Minecraft.Windows.exe", "minecraft-launcher.exe"]

    for proc in psutil.process_iter(['pid', 'name']):
        try:
            process_name = proc.info['name'].lower()
            if any(name.lower() in process_name for name in minecraft_names):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return False

def keyboard_press_and_release(action):
    keyboard_controller.press(action)
    time.sleep(0.05)
    keyboard_controller.release(action)

def mouse_press_and_release(action):
    mouse.press(action)
    time.sleep(0.05)
    mouse.release(action)

def process_command(action, command):
    hotbar_mapping = {
        'hotBar1': '1',
        'hotBar2': '2',
        'hotBar3': '3',
        'hotBar4': '4',
        'hotBar5': '5',
        'hotBar6': '6',
        'hotBar7': '7',
        'hotBar8': '8',
        'hotBar9': '9',
    }
    keyboard_mapping = {
        'left': 'a',
        'right': 'd',
        'up': 'w',
        'down': 's',
        'inventory': 'e',
        'drop': 'q',
        'chat': 't',
        'zoom': 'c',
        'jump': Key.space,
        'pause': Key.esc,
        'sneak': Key.shift,
        'sprint': Key.ctrl,
    }
    mouse_mapping = {
        'attack': Button.left,
        'use': Button.right,
    }
    try:
        if command == 'start':
            if action in keyboard_mapping:
                keyboard_controller.press(keyboard_mapping[action])
            elif action in mouse_mapping:
                mouse.press(mouse_mapping[action])
            else:
                error_text(f'Unknown action for start: \'{action}\'')
        elif command == 'stop':
            if action in keyboard_mapping:
                keyboard_controller.release(keyboard_mapping[action])
            elif action in mouse_mapping:
                mouse.release(mouse_mapping[action])
            else:
                error_text(f'Unknown action for stop: \'{action}\'')
        elif command == 'press':
            if action in hotbar_mapping:
                keyboard_press_and_release(hotbar_mapping[action])
            elif action in keyboard_mapping:
                keyboard_press_and_release(keyboard_mapping[action])
            elif action in mouse_mapping:
                mouse_press_and_release(mouse_mapping[action])
            else:
                error_text(f'Unknown action for press: \'{action}\'')
        else:
            error_text(f'Unknown command for \'{action}\': \'{command}\'')
    except Exception as e:
        error_text(f'Error processing command for \'{action}\' with command \'{command}\': {e}')

def process_mouse_movement(mouse_data):
    user32 = ctypes.windll.user32
    steps = 5
    delay = 0.01
    dx = round(mouse_data.get('x', 0) * MOUSE_SENSITIVITY)
    dy = round(mouse_data.get('y', 0) * MOUSE_SENSITIVITY)
    step_x = dx / steps
    step_y = dy / steps

    for _ in range(steps):
        user32.mouse_event(0x0001, int(step_x), int(step_y), 0, 0)
        time.sleep(delay)

def udp_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
        sock.settimeout(300.0)
        success_text('Server started. Press Ctrl+C to exit.')
    except Exception as e: 
        error_text(f'Failed to bind server: {e}')
        return
    
    inactive_time = 0  
    max_inactive_time = 5  

    while True:
        try:
            if not is_minecraft_running():
                info_text(f'{PROGRAM} not running. Exiting server in... {max_inactive_time - inactive_time}')
                inactive_time += 1
                time.sleep(0.5)
                if inactive_time >= max_inactive_time:
                    error_text(f'{PROGRAM} inactive for too long. Server shutting down.')
                    break
                continue
            
            inactive_time = 0
            data, addr = sock.recvfrom(1024)

            message = data.decode()
            info_text(f'Message: {message}')

            try:
                message_data = json.loads(message)
                if 'ping' in message_data and message_data['ping'] == 'musaddiq625':
                    pong_response = json.dumps({'pong': 'musaddiq625'})
                    sock.sendto(pong_response.encode(), addr)
                    success_text(f'Connected to {addr}')
                    continue
                elif 'mouse' in message_data:
                    process_mouse_movement(message_data['mouse'])
                else:
                    for key, value in message_data.items():
                        process_command(key, value)
            except json.JSONDecodeError:
                error_text(f'Failed to decode JSON. Raw message: {data}')
        except Exception as e:
            error_text(f'Error receiving data: {e}')
        time.sleep(0.01)
    sock.close()
    sys.exit(0)

if __name__ == '__main__':
    try:
        if get_local_ip():
            server_thread = threading.Thread(target=udp_server, daemon=True)
            server_thread.start()
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        error_text('Server shutting down.')
        sys.exit(0)
