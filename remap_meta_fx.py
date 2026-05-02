import time
from evdev import InputDevice, ecodes, list_devices, UInput
from select import select

KEYMAP = {
    ecodes.KEY_F20: [ecodes.KEY_LEFTCTRL, ecodes.KEY_C],       # Single-click
    ecodes.KEY_F19: [ecodes.KEY_LEFTCTRL, ecodes.KEY_V],       # Double-click
    ecodes.KEY_F18: [ecodes.KEY_LEFTCTRL, ecodes.KEY_PAGEUP],  # Hold
}

TARGET_VENDOR = 0x045e
TARGET_PRODUCT = 0x0921


def find_pen_device():
    for p in list_devices():
        try:
            dev = InputDevice(p)

            if dev.info.vendor == TARGET_VENDOR and dev.info.product == TARGET_PRODUCT:
                print(f"🎯 Pen gefunden: {dev.name} ({dev.path})")
                return dev

        except Exception:
            continue

    return None


def send_keys(keys, ui):
    for k in keys:
        ui.write(ecodes.EV_KEY, k, 1)
    ui.syn()

    time.sleep(0.01)

    for k in reversed(keys):
        ui.write(ecodes.EV_KEY, k, 0)
    ui.syn()


def handle_device(dev):
    try:
        dev.grab()
    except Exception:
        print("⚠️ Konnte Device nicht grabben")
        return

    all_keys = set()
    for combo in KEYMAP.values():
        all_keys.update(combo)

    ui = UInput({ecodes.EV_KEY: list(all_keys)})

    print("✅ Eingabegerät aktiv – warte auf Eingaben…")

    try:
        while True:
            r, _, _ = select([dev.fd], [], [], 0.1)
            if not r:
                continue

            for event in dev.read():

                if event.type != ecodes.EV_KEY:
                    continue

                if event.value != 1:
                    continue

                if event.code in KEYMAP:
                    keys = KEYMAP[event.code]
                    print(f"🔁 {ecodes.KEY.get(event.code, event.code)} -> {keys}")
                    send_keys(keys, ui)

    except (OSError, IOError):
        print("⚠️ Gerät getrennt")
        try:
            dev.ungrab()
        except Exception:
            pass


def main():
    print("🔄 Starte Pen-Mapper. Warte auf Gerät…")

    try:
        while True:
            dev = find_pen_device()

            if dev:
                try:
                    handle_device(dev)
                except Exception as e:
                    print(f"❌ Fehler: {e}")
                    time.sleep(2)
            else:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n🛑 Beendet")


if __name__ == "__main__":
    main()
