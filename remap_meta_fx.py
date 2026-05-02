import time
from evdev import InputDevice, ecodes, UInput
from select import select

KEYMAP = {
    ecodes.KEY_F20: [ecodes.KEY_LEFTCTRL, ecodes.KEY_C],
    ecodes.KEY_F19: [ecodes.KEY_LEFTCTRL, ecodes.KEY_V],
    ecodes.KEY_F18: [ecodes.KEY_LEFTCTRL, ecodes.KEY_PAGEUP],
}

DEVICE_PATH = "/dev/input/event20"


def send_keys(keys, ui):
    for k in keys:
        ui.write(ecodes.EV_KEY, k, 1)
    ui.syn()

    time.sleep(0.01)

    for k in reversed(keys):
        ui.write(ecodes.EV_KEY, k, 0)
    ui.syn()


def main():
    print("🔄 Starte Pen-Mapper...")

    try:
        dev = InputDevice(DEVICE_PATH)
        dev.grab()

        all_keys = set()
        for combo in KEYMAP.values():
            all_keys.update(combo)

        ui = UInput({ecodes.EV_KEY: list(all_keys)})

        print("✅ Aktiv:", dev.name)

        while True:
            r, _, _ = select([dev.fd], [], [], 0.1)
            if not r:
                continue

            for event in dev.read():
                if event.type == ecodes.EV_KEY and event.value == 1:

                    if event.code in KEYMAP:
                        print("🔁", event.code)
                        send_keys(KEYMAP[event.code], ui)

    except KeyboardInterrupt:
        print("\n🛑 Beendet")

    except Exception as e:
        print("❌ Fehler:", e)


if __name__ == "__main__":
    main()
