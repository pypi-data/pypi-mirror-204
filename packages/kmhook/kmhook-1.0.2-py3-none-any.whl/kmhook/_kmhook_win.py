"""
Small module to fiddle with mouse and keyboard.
- works only with Windows ;
- works only with french AZERTY keyboards ;
"""

import ctypes
from time import sleep, perf_counter_ns

_SendInput = ctypes.windll.user32.SendInput
_GetKeyState = ctypes.windll.user32.GetKeyState
_GetSystemMetrics = ctypes.windll.user32.GetSystemMetrics
_GetCursorPos = ctypes.windll.user32.GetCursorPos

_SCREEN_WIDTH, _SCREEN_HEIGHT = _GetSystemMetrics(0), _GetSystemMetrics(1)

_PUL = ctypes.POINTER(ctypes.c_ulong)


class _POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", _PUL)]


class _HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class _MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", _PUL)]


class _InputI(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", _MouseInput),
                ("hi", _HardwareInput)]


class _Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", _InputI)]


# Output codes are scan codes
_name_to_output_code = {
    'esc': 0x01,
    'escape': 0x01,
    '&': 0x02,
    'é': 0x03,
    '"': 0x04,
    "'": 0x05,
    '(': 0x06,
    '-': 0x07,
    'è': 0x08,
    '_': 0x09,
    'ç': 0x0a,
    'à': 0x0b,
    ')': 0x0c,
    '=': 0x0d,
    'backspace': 0x0e,
    'tab': 0x0f,
    'a': 0x10,
    'z': 0x11,
    'e': 0x12,
    'r': 0x13,
    't': 0x14,
    'y': 0x15,
    'u': 0x16,
    'i': 0x17,
    'o': 0x18,
    'p': 0x19,
    '^': 0x1A,
    '$': 0x1B,
    'enter': 0x1C,
    'lctrl': 0x1D,
    'q': 0x1E,
    's': 0x1F,
    'd': 0x20,
    'f': 0x21,
    'g': 0x22,
    'h': 0x23,
    'j': 0x24,
    'k': 0x25,
    'l': 0x26,
    'm': 0x27,
    'ù': 0x28,
    '²': 0x29,
    'lshift': 0x2a,
    '*': 0x2b,
    'w': 0x2c,
    'x': 0x2d,
    'c': 0x2e,
    'v': 0x2f,
    'b': 0x30,
    'n': 0x31,
    ',': 0x32,
    ';': 0x33,
    ':': 0x34,
    '!': 0x35,
    'rshift': 0x36,
    'num_*': 0x37,
    'lalt': 0x38,
    ' ': 0x39,
    'space': 0x39,
    'capslock': 0x3a,
    'f1': 0x3b,
    'f2': 0x3c,
    'f3': 0x3d,
    'f4': 0x3e,
    'f5': 0x3f,
    'f6': 0x40,
    'f7': 0x41,
    'f8': 0x42,
    'f9': 0x43,
    'f10': 0x44,
    'pause': 0x45,
    'scrolllock': 0x46,
    'num_7': 0x47,
    'num_8': 0x48,
    'num_9': 0x49,
    'num_-': 0x4a,
    'num_4': 0x4b,
    'num_5': 0x4c,
    'num_6': 0x4d,
    'num_+': 0x4e,
    'num_1': 0x4f,
    'num_2': 0x50,
    'num_3': 0x51,
    'num_0': 0x52,
    'num_.': 0x53,
    'printscreen': 0x54,
    '<': 0x56,
    'f11': 0x57,
    'f12': 0x58,
    'lwin': 0xe05c,
    'altgr': 0xe038,
    'rwin': 0xe05c,
    'menu': 0xe05d,
    'rctrl': 0xe01d,
    'up': 0xe048,
    'left': 0xe04b,
    'down': 0xe050,
    'right': 0xe04d,
    'insert': 0xe052,
    'delete': 0xe053,
    'home': 0xe047,
    'end': 0xe04f,
    'pageup': 0xE049,
    'pagedown': 0xe051,
    'num_/': 0xe035,
    'mouse_left': 0x01,
    'mouse_right': 0x02,
    'mouse_middle': 0x04,
    'num_lock': 0x00  # dummy

}

# input codes are VK_CODES
_name_to_input_code = {
    'escape': 0x01b,
    'esc': 0x01b,
    '&': 0x031,
    'é': 0x32,
    '"': 0x33,
    "'": 0x34,
    '(': 0x35,
    '-': 0x36,
    'è': 0x37,
    '_': 0x38,
    'ç': 0x39,
    'à': 0x30,
    ')': 0xdb,
    '=': 0xbb,
    'backspace': 0x08,
    'tab': 0x09,
    'a': 0x41,
    'z': 0x5a,
    'e': 0x45,
    'r': 0x52,
    't': 0x54,
    'y': 0x59,
    'u': 0x55,
    'i': 0x49,
    'o': 0x4f,
    'p': 0x50,
    '^': 0xdd,
    '$': 0xba,
    'enter': 0x0d,
    'q': 0x51,
    's': 0x53,
    'd': 0x44,
    'f': 0x46,
    'g': 0x47,
    'h': 0x48,
    'j': 0x4a,
    'k': 0x4b,
    'l': 0x4c,
    'm': 0x4d,
    'ù': 0xc0,
    '²': 0xde,
    'lshift': 0xa0,
    '*': 0xdc,
    'w': 0x57,
    'x': 0x58,
    'c': 0x43,
    'v': 0x56,
    'b': 0x42,
    'n': 0x4e,
    ',': 0xbc,
    ';': 0xbe,
    ':': 0xbf,
    '!': 0xdf,
    'rshift': 0xa1,
    'num_*': 0x6a,
    'lalt': 0xa4,
    'space': 0x20,
    ' ': 0x20,
    'capslock': 0x14,
    'f1': 0x70,
    'f2': 0x71,
    'f3': 0x72,
    'f4': 0x73,
    'f5': 0x74,
    'f6': 0x75,
    'f7': 0x76,
    'f8': 0x77,
    'f9': 0x78,
    'f10': 0x79,
    'pause': 0x13,
    'scrolllock': 0x91,
    'num_7': 0x67,
    'num_8': 0x68,
    'num_9': 0x69,
    'num_-': 0x6d,
    'num_4': 0x64,
    'num_5': 0x65,
    'num_6': 0x66,
    'num_+': 0x6b,
    'num_1': 0x61,
    'num_2': 0x62,
    'num_3': 0x63,
    'num_0': 0x60,
    'num_.': 0x6e,
    'num_/': 0x6f,
    'num_lock': 0x90,
    'printscreen': 0x2c,
    '<': 0xe2,
    'f11': 0x7a,
    'f12': 0x7b,
    'lwin': 0x5b,
    'lctrl': 0xa2,
    'rwin': 0x5c,
    'menu': 0x5d,
    'rctrl': 0xa3,
    'up': 0x26,
    'left': 0x25,
    'down': 0x28,
    'right': 0x27,
    'insert': 0x2d,
    'delete': 0x2e,
    'home': 0x24,
    'end': 0x23,
    'pageup': 0x21,
    'pagedown': 0x22,
    'altgr': 0xa5,
    'mouse_left': 0x01,
    'mouse_right': 0x02,
    'mouse_middle': 0x04
}

_input_code_to_name = dict()
for e in _name_to_input_code:
    if _name_to_input_code[e] not in _input_code_to_name:
        _input_code_to_name[_name_to_input_code[e]] = e

_output_code_to_name = dict()
for e in _name_to_output_code:
    if _name_to_output_code[e] not in _output_code_to_name:
        _output_code_to_name[_name_to_output_code[e]] = e

_input_code_to_output_code = dict()
for e in _name_to_input_code:
    _input_code_to_output_code[_name_to_input_code[e]] = _name_to_output_code[e]

_output_code_to_input_code = dict()
for e in _name_to_output_code:
    _output_code_to_input_code[_name_to_output_code[e]] = _name_to_input_code[e]

_max_input = max(_name_to_input_code[e] for e in _name_to_input_code)

_is_on = {key_name: False for key_name in _name_to_output_code}

_valid_key_names = tuple(_name_to_input_code)


def _press(key: str) -> None:
    """
    Presses the key
    :param key: str
    :return: None
    """
    try:
        code = _name_to_output_code[key]
    except KeyError:
        raise KeyError(f'{key} is not a valid key.')
    _is_on[key] = True
    if key == 'mouse_right':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 8, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    elif key == 'mouse_left':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 2, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    elif key == 'mouse_middle':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 0x20, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    else:
        extra = ctypes.c_ulong(0)
        inp = _InputI()
        inp.ki = KeyBdInput(0, code % 0x100, 0x0008 | (code >> 15), 0, ctypes.pointer(extra))
        x = _Input(ctypes.c_ulong(1), inp)
        _SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def _release(key: str) -> None:
    """
    Releases the key
    :param key: str
    :return: None
    """
    try:
        code = _name_to_output_code[key]
    except KeyError:
        raise KeyError(f'{key} is not a valid key.')

    _is_on[key] = False
    if key == 'mouse_right':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 0x10, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    elif key == 'mouse_left':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 4, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    elif key == 'mouse_middle':
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.mi = _MouseInput(0, 0, 0, 0x40, 0, ctypes.pointer(extra))
        command = _Input(ctypes.c_ulong(0), ii_)
        _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))
    else:
        extra = ctypes.c_ulong(0)
        ii_ = _InputI()
        ii_.ki = KeyBdInput(0, code % 0x100, 0x0008 | 0x0002 | (code >> 15), 0, ctypes.pointer(extra))
        x = _Input(ctypes.c_ulong(1), ii_)
        _SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def get_valid_key_names() -> tuple:
    """
    Returns all the valid key names to use within kmHook
    """
    return _valid_key_names


def get_mouse_pos() -> tuple[int, int]:
    """
    Returns current mouseposition.
    """
    pos = _POINT()
    _GetCursorPos(ctypes.byref(pos))
    return pos.x, pos.y


def press(key: str | list | tuple) -> None:
    """
    Presses the key (a single str or a sequence of keys) but does not release it
    """
    if isinstance(key, str):
        _press(key)
    else:
        for _key in key:
            _press(_key)


def release(key: str | list | tuple) -> None:
    """
    Releases the key (a single str or a sequence of keys).
    """
    if isinstance(key, str):
        _release(key)
    else:
        for _key in key:
            _release(_key)


def press_and_release(key: str | list | tuple) -> None:
    """
    Presses and releases the key or the sequence of keys.
    """
    press(key)
    sleep(0.01)
    release(key)


def get_key_name() -> str:
    """
    Waits for a key to be pressed and return its name.
    """
    while True:
        for name in _name_to_input_code:
            if is_pressed(name):
                return name


def is_pressed(key: str | tuple[str] | list[str]) -> bool:
    """
    Checks if a key or a sequence of keys is being pressed.
    """
    if isinstance(key, str):
        return bool(_GetKeyState(_name_to_input_code[key]) & 2 ** 15)
    else:
        for k in key:
            if bool(_GetKeyState(_name_to_input_code[k]) & 2 ** 15) is False:
                return False
        return True


def is_pressed_once(key: str | tuple[str] | list[str]) -> bool:
    """
    Checks if a key or a sequence of keys is being pressed but only once :
    if the key was being pressed during the last call and is still being pressed,
    this function returns False... until key is released and pressed again.

    """
    if isinstance(key, str):
        if is_pressed(key):
            if _is_on[key]:
                return False
            else:
                _is_on[key] = True
                return True
        elif _is_on[key]:
            _is_on[key] = False
            return False
    else:
        if is_pressed(key):
            if key in _is_on and _is_on[key]:
                return False
            else:
                _is_on[key] = True
                return True
        elif (key in _is_on and _is_on[key]) or (key not in _is_on):
            _is_on[key] = False
            return False


def move_mouse_relative(x: float | int, y: float | int) -> None:
    """
    Moves mouse relatively to current position.
    """
    extra = ctypes.c_ulong(0)
    ii_ = _InputI()
    ii_.mi = _MouseInput(int(round(x)), int(round(y)), 0, 1, 0, ctypes.pointer(extra))
    command = _Input(ctypes.c_ulong(0), ii_)
    _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def move_mouse_absolute(x: float | int, y: float | int) -> None:
    """
    Moves mouse absolutely to coordinates (x,y).
    """
    extra = ctypes.c_ulong(0)
    ii_ = _InputI()
    ii_.mi = _MouseInput(int(round(x * 65536 / _SCREEN_WIDTH)), int(round(y * 65536 / _SCREEN_HEIGHT)), 0, 0x8001, 0,
                         ctypes.pointer(extra))
    command = _Input(ctypes.c_ulong(0), ii_)
    _SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def continuous_relative_move(x: float | int, y: float | int, time_interval: float | int) -> None:
    """
    Moves mouse relatively and continuously during time_interval.
    Is blocking.
    """
    actual_sum_x = 0
    actual_sum_y = 0
    duration = 0
    start = perf_counter_ns()
    while duration < time_interval:
        theoretic_sum_x = x * duration / time_interval
        theoretic_sum_y = y * duration / time_interval
        delta_x = int(round(theoretic_sum_x - actual_sum_x))
        delta_y = int(round(theoretic_sum_y - actual_sum_y))
        move_mouse_relative(delta_x, delta_y)
        actual_sum_x += delta_x
        actual_sum_y += delta_y
        sleep(0.001)
        now = perf_counter_ns()
        duration = (now - start) / (10 ** 6)
    if actual_sum_x < x:
        move_mouse_relative(x - actual_sum_x, 0)
    if actual_sum_y < y:
        move_mouse_relative(0, y - actual_sum_y)
