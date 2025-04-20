# 🕹️ Minecraft Controller via Flutter & Python

Control Minecraft on your PC using your **phone as a controller**!  
This project consists of a **Python backend** that listens for commands and sends keyboard/mouse inputs to Minecraft, and a **Flutter mobile app** that acts as the controller interface.

---

## 🚀 Features

- 📱 Control Minecraft from your mobile using a custom Flutter app
- 🎮 Emulates keyboard and mouse input via Python
- 🧠 Auto-detects if Minecraft is running
- 🔄 Auto-installs missing Python packages on first run
- 📡 Communicates over UDP on your local network

---

## 📲 Flutter Mobile Controller App

Use this Flutter app as your game controller.  
**GitHub Repo:** [Minecraft Controller (Flutter App)](https://github.com/Musaddiq625/minecraft_flutter_controller.git)

### How It Works

1. Install the Flutter app on your Android device.
2. Run the Python backend (see below) - it will display your **Local IP address**.
3. Enter that IP address into the Flutter app’s settings.
4. Connect and press 'Start playing'
4. Press buttons or use the joystick in the app to send commands to your PC.

The app sends JSON packets like:

```json
{ "action": "press", "key": "w" }
{ "action": "click" }
{ "action": "move", "x": 1, "y": -1 }
```

---

## 🧰 Python Backend Setup

### Requirements

- **Python 3.8+**  
- Minecraft Java Edition installed and running on your PC  
- Both PC and mobile on the **same local network**  

### Installation & First Run

1. **Clone this repo** (Python backend) and change into its directory:
   ```bash
   git clone https://github.com/Musaddiq625/minecraft_python_controller.git
   cd minecraft_python_controller
   ```

2. **Run the script** (it will verify/install dependencies, then exit if it installed anything):
   ```bash
   python main.py
   ```

3. **Rerun** the script if prompted:
   ```bash
   python main.py
   ```

4. The script will print your **local IP address**. Copy that IP into the Flutter app.

---

## 📦 Building a Standalone EXE (Windows)

Convert your Python script into a single-file `.exe` for easy distribution:

```bash
pyinstaller --onefile -c 'main.py'
```

- Replace `main.py` if your script file is named differently.  
- The generated `.exe` will live in the `dist/` folder.

---

## ⚙️ Configuration

- **UDP Port:** Default is `65432`. Change `UDP_PORT` in `main.py` if needed.  
- **Mouse Sensitivity:** Tweak the `MOUSE_SENSITIVITY` constant to adjust look speed.  
- **Program Name:** By default, checks for processes named like `Minecraft` or `javaw.exe`. Update `minecraft_names` in `is_minecraft_running()` to customize.

---

## 🛠️ Troubleshooting

- **No input registered?**  
  - Run the `.exe` or `python main.py` as **Administrator**.  
  - Ensure Minecraft is in the foreground or allow background input injection.

- **Can’t bind UDP port?**  
  - Verify no other application is using port `65432`, or choose a different port.

- **Dependencies not installing?**  
  - Ensure you have internet access, and `pip` is on your `PATH`.

---


## 🔐 Security

- This app communicates over your local network using UDP and does not use any encryption or authentication.
- **Make sure both devices are on a trusted network.** Avoid using public Wi-Fi for security reasons.

---

## ⚠️ Minecraft Settings

- Make sure Minecraft is running and focused on your PC.
- Go to Options > Controls > Mouse Settings, and **enable Raw Input** to ensure the game accepts movement commands correctly.

---

## 🧑‍💻 Author & Links

- **Author:** [Musaddiq Ahmed Khan (Musaddiq625)](https://github.com/Musaddiq625)  
- **Flutter App:** https://github.com/Musaddiq625/minecraft_controller.git  
- **Python Backend:** https://github.com/Musaddiq625/minecraft_flutter_controller.git  

This is just a basic proof of concept to spark your creativity! If you can improve or extend it, feel free to fork and submit a PR.

Made with ❤️ by Musaddiq625 — contributions welcome!

