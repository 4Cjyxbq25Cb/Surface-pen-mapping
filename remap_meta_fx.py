import time
from evdev import InputDevice, ecodes, list_devices, UInput
from select import select

KEYMAP = {
    ecodes.KEY_F20: [ecodes.KEY_LEFTCTRL, ecodes.KEY_C],
    ecodes.KEY_F19: [ecodes.KEY_LEFTCTRL, ecodes.KEY_PAGEUP],
    ecodes.KEY_F18: [ecodes.KEY_LEFTCTRL, ecodes.KEY_V],
}

DEBOUNCE = 0.4  # seconds

TARGET_VENDOR = 0x045e
TARGET_PRODUCT = 0x0921


def find_device():
    for path in list_devices():
        try:
            dev = InputDevice(path)
            if (
                dev.info.vendor == TARGET_VENDOR and
                dev.info.product == TARGET_PRODUCT and
                'Keyboard' in dev.name
            ):
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


def main():
    print('Starte Pen-Mapper...')
    dev = None
    ui = None
    last_trigger = {}

    try:
        while True:
            if dev is None:
                dev = find_device()
                if dev is None:
                    time.sleep(1)
                    continue
                try:
                    dev.grab()
                except Exception as e:
                    print('grab failed:', e)

                all_keys = set()
                for combo in KEYMAP.values():
                    all_keys.update(combo)
                ui = UInput({ecodes.EV_KEY: list(all_keys)})
                print('Aktiv:', dev.name)

            try:
                r, _, _ = select([dev.fd], [], [], 0.1)
                if not r:
                    continue
                for event in dev.read():
                    if (
                        event.type == ecodes.EV_KEY and
                        event.value == 1 and
                        event.code in KEYMAP
                    ):
                        now = time.monotonic()
                        if now - last_trigger.get(event.code, 0) < DEBOUNCE:
                            continue
                        last_trigger[event.code] = now
                        print('Trigger:', event.code)
                        send_keys(KEYMAP[event.code], ui)
            except (OSError, IOError):
                print('Device getrennt, reconnect...')
                if ui:
                    ui.close()
                    ui = None
                dev = None
                time.sleep(1)

    except KeyboardInterrupt:
        print('Beendet')
        if ui:
            ui.close()


if __name__ == '__main__':
    main()
