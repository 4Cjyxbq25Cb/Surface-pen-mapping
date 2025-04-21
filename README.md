
# Surface Stylus Button Mapper for Linux

This script remaps the buttons of a Microsoft Surface Stylus to specific keyboard shortcuts in Linux. It listens for the events from the Surface Pen and triggers corresponding actions based on the button pressed. 

The mapping works as follows:
- **Single-click (Meta+F20)**: Triggers `Ctrl+C` (copy).
- **Double-click (Meta+F19)**: Triggers `Ctrl+V` (paste).
- **Press and hold (Meta+F18)**: Triggers `Ctrl+PageUp` (scroll up).

## Prerequisites

Before you can use this script, ensure that the following dependencies are installed:

- Python 3
- `evdev` library (for handling input devices)

You can install the necessary Python library by running:
```bash
pip install evdev
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/Surface-pen-mapping.git
cd Surface-pen-mapping
```

### 2. Ensure you have the correct permissions
The script requires access to input devices, so make sure your user has the necessary permissions. You can add your user to the `input` group to grant access to the `/dev/input` devices.

```bash
sudo usermod -aG input $USER
```

### 3. Running the script
You can run the script directly by using:

```bash
python3 remap_meta_fx.py
```

This will start the script and continuously listen for the Surface Pen device.

### 4. Auto-start on Boot (Optional)

To have this script run automatically when your system boots up, follow these steps:

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/pen-remap.service
```

2. Paste the following content into the service file:

```ini

[Unit]
Description=Surface Pen Button Mapper
After=bluetooth.target
Wants=bluetooth.target

[Service]
ExecStart=/usr/bin/python3 /path/to/your/project/repo/pen-remap.py
WorkingDirectory=/path/to/your/project/repo/
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
User=your_user
Environment=DISPLAY=:0  # Set DISPLAY for graphical applications
Environment=PYTHONUNBUFFERED=1  # Disables output buffering

[Install]
WantedBy=default.target

```

3. Reload systemd to apply the changes:

```bash
sudo systemctl daemon-reload
```

4. Enable and start the service:

```bash
sudo systemctl enable pen-remap.service
sudo systemctl start pen-remap.service
```

The script should now run automatically after a reboot.

## Troubleshooting

- If the script is not working, ensure that your Surface Pen is correctly connected via Bluetooth.
- Ensure that the script has access to the necessary devices (`/dev/input` and `/dev/uinput`).
- If you encounter issues with permissions, check that your user is part of the `input` group.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Yo
This work builds on the work of 
qzed Maximilian Luz,
PhilDevProg PhilProg,
and KTibow Kendell R 
and the repo linux-surface-pen-button-remap.

