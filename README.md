# Surface Stylus Button Mapper for Linux

This script remaps the buttons of a Microsoft Surface Stylus to specific keyboard shortcuts in Linux. It listens for the events from the Surface Pen and triggers corresponding actions based on the button pressed.

The mapping works as follows:
- **Single-click (Meta+F20)**: Triggers `Ctrl+C` (copy).
- **Double-click (Meta+F19)**: Triggers `Ctrl+PageUp`.
- **Press and hold (Meta+F18)**: Triggers `Ctrl+V` (paste).

A 400ms debounce prevents double-firing on the double-click button.

## Prerequisites

- Python 3
- `evdev` library

```bash
pip install evdev
```

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/4Cjyxbq25Cb/Surface-pen-mapping.git
cd Surface-pen-mapping
```

### 2. Permissions
Add your user to the `input` group to grant access to `/dev/input` devices:

```bash
sudo usermod -aG input $USER
```

Log out and back in for the group change to take effect.

### 3. Running the script
```bash
python3 remap_meta_fx.py
```

### 4. Auto-start on Boot

1. Create a systemd service file:

```bash
sudo nano /etc/systemd/system/pen-remap.service
```

2. Paste the following content, replacing `your_user` and the path:

```ini
[Unit]
Description=Surface Pen Button Mapper
After=bluetooth.target
Wants=bluetooth.target

[Service]
ExecStart=/usr/bin/python3 /path/to/Surface-pen-mapping/remap_meta_fx.py
WorkingDirectory=/path/to/Surface-pen-mapping/
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal
User=your_user
SupplementaryGroups=input
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=default.target
```

3. Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pen-remap.service
sudo systemctl start pen-remap.service
```

## Troubleshooting

- Ensure the Surface Pen is paired and connected via Bluetooth.
- The pen device only appears in `/dev/input` when the pen is awake — the script will automatically detect it once it connects.
- Make sure `SupplementaryGroups=input` is set in the service file, otherwise systemd may not grant the user access to input devices even if they are in the `input` group.
- Check logs with `journalctl -u pen-remap -f`.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Credits
This work builds on the work of
qzed Maximilian Luz,
PhilDevProg PhilProg,
and KTibow Kendell R
and the repo linux-surface-pen-button-remap.
