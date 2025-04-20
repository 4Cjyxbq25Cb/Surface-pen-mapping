import time
from evdev import InputDevice, categorize, ecodes, list_devices, InputEvent, UInput
from select import select

# Mapping Meta+Fn → Aktionen
KEYMAP = {
    ecodes.KEY_F20: [ecodes.KEY_LEFTCTRL, ecodes.KEY_C],       # Single-click
    ecodes.KEY_F19: [ecodes.KEY_LEFTCTRL, ecodes.KEY_V],       # Double-click
    ecodes.KEY_F18: [ecodes.KEY_LEFTCTRL, ecodes.KEY_PAGEUP],  # Hold
}

TARGET_VENDOR = 0x045e
TARGET_PRODUCT = 0x0921

def find_pen_device():
    for path in list_devices():
        try:
            dev = InputDevice(path)
            if dev.info.vendor != TARGET_VENDOR or dev.info.product != TARGET_PRODUCT:
                continue

            capabilities = dev.capabilities().get(ecodes.EV_KEY, [])
            if (ecodes.KEY_LEFTMETA in capabilities and
                ecodes.KEY_F18 in capabilities and
                ecodes.KEY_F19 in capabilities and
                ecodes.KEY_F20 in capabilities):
                print(f"🎯 Gerät verbunden: {dev.name} ({path})")
                return dev
        except Exception:
            continue
    return None

def send_keys(keys, ui):
    for k in keys:
        ui.write(ecodes.EV_KEY, k, 1)
    ui.syn()
    time.sleep(0.05)
    for k in reversed(keys):
        ui.write(ecodes.EV_KEY, k, 0)
    ui.syn()

def handle_device(dev):
    dev.grab()
    ui = UInput()
    meta_down = False

    print("✅ Eingabegerät aktiv – warte auf Eingaben…")

    while True:
        try:
            r, _, _ = select([dev.fd], [], [], 0.1)
            if not r:
                continue

            for event in dev.read():
                if event.type != ecodes.EV_KEY:
                    continue

                key_event = categorize(event)
                code = key_event.scancode
                value = key_event.keystate

                if code == ecodes.KEY_LEFTMETA:
                    meta_down = value == 1

                elif code in KEYMAP and meta_down and value == 1:
                    keys_to_send = KEYMAP[code]
                    print(f"🔁 Meta+{ecodes.KEY[code]} → {', '.join(ecodes.KEY[k] for k in keys_to_send)}")
                    send_keys(keys_to_send, ui)

        except (OSError, IOError):
            print("⚠️ Gerät wurde getrennt. Suche erneut…")
            dev.ungrab()
            break

def main():
    print("🔄 Starte Pen-Mapper. Warte auf Verbindung des Geräts…")
    while True:
        dev = find_pen_device()
        if dev:
            try:
                handle_device(dev)
            except Exception as e:
                print(f"❌ Fehler beim Handhaben des Geräts: {e}")
                time.sleep(2)
        else:
            time.sleep(2)

if __name__ == "__main__":
    main()

