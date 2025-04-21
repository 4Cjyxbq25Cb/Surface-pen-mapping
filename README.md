# Surface Pen Button Remapper (Linux)

Dieses Projekt ermöglicht es, die Tasten eines Microsoft Surface Pens unter Linux benutzerdefiniert neu zu belegen – z. B. für Copy-Paste- oder Navigationstasten. Es richtet sich speziell an Geräte, die über Bluetooth verbunden sind und als `Surface Pen Keyboard` erkannt werden (z. B. mit Vendor-ID `0x045e` und Product-ID `0x0921`).

## Funktionsweise

Ein Python-Skript überwacht Eingaben eines bestimmten Eingabegeräts (Surface Pen) und führt beim Drücken bestimmter Tastenkombinationen simulierte Tastensequenzen aus. Standardmäßig sind folgende Kombinationen eingerichtet:

- **Meta + F20** → `Ctrl + C` (Kopieren)
- **Meta + F19** → `Ctrl + V` (Einfügen)
- **Meta + F18** → `Ctrl + PageUp` (z. B. Tab-Wechsel in Browsern)

Diese Zuordnungen können im Skript angepasst werden.

---

## Einrichtung

### Schritt 1: Abhängigkeiten installieren

Stelle sicher, dass `Python 3` installiert ist, und installiere die benötigte Bibliothek:

```bash
pip install evdev
```

### Schritt 2: uinput-Zugriff konfigurieren

Damit das Skript Tasteneingaben simulieren kann, braucht der Benutzer Schreibzugriff auf `/dev/uinput`.

1. **uinput-Gruppe erstellen und Benutzer hinzufügen:**

```bash
sudo groupadd uinput
sudo usermod -aG uinput $USER
```

2. **udev-Regel erstellen:**

```bash
sudo nano /etc/udev/rules.d/90-uinput.rules
```

Inhalt:

```text
KERNEL=="uinput", GROUP="uinput", MODE="0660"
```

3. **udev-Regeln neu laden und ggf. Modul laden:**

```bash
sudo udevadm control --reload-rules
sudo modprobe uinput
```

4. **Neustart oder neue Sitzung starten**, damit Gruppenänderungen wirksam werden.

---

### Schritt 3: Python-Skript einrichten

Erstelle ein Verzeichnis und speichere dort das folgende Skript unter dem Namen `remap_meta_fx.py`, z. B.:

```bash
mkdir -p ~/Surface-pen-mapping
nano ~/Surface-pen-mapping/remap_meta_fx.py
```

(Skript siehe im Repository)

---

### Schritt 4: systemd-Service (für Autostart)

Erstelle eine systemd-Servicedatei:

```bash
sudo nano /etc/systemd/system/pen-remap.service
```

Inhalt:

```ini
[Unit]
Description=Surface Pen Button Mapper
After=default.target

[Service]
ExecStart=/usr/bin/python3 /home/USERNAME/Surface-pen-mapping/remap_meta_fx.py
Restart=always
User=USERNAME
Group=uinput

[Install]
WantedBy=default.target
```

Ersetze `USERNAME` durch deinen tatsächlichen Benutzernamen und passe ggf. den Pfad an.

---

### Schritt 5: Service aktivieren

```bash
sudo systemctl daemon-reexec
sudo systemctl daemon-reload
sudo systemctl enable pen-remap.service
sudo systemctl start pen-remap.service
```

Optional: Log-Ausgabe anzeigen

```bash
sudo journalctl -u pen-remap.service -f
```

---

## Hinweise

- Das Skript erkennt automatisch, wenn der Stift verbunden oder getrennt wird.
- Button-Kombinationen und Tastenzuordnungen lassen sich direkt im Python-Skript anpassen.
- Falls `uinput` beim Systemstart nicht automatisch geladen wird, kann es manuell oder über eine Modulliste hinzugefügt werden.

---

## Lizenz

MIT License
