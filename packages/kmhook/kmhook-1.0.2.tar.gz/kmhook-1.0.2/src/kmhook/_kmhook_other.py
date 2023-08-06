
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
    ...


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
    ...


def get_valid_key_names() -> tuple:
    """
    Returns all the valid key names to use within kmHook
    """
    ...


def get_mouse_pos() -> tuple[int, int]:
    """
    Returns current mouseposition.
    """
    ...


def press(key: str | list | tuple) -> None:
    """
    Presses the key (a single str or a sequence of keys) but does not release it
    """
    ...

def release(key: str | list | tuple) -> None:
    """
    Releases the key (a single str or a sequence of keys).
    """
    ...


def press_and_release(key: str | list | tuple) -> None:
    """
    Presses and releases the key or the sequence of keys.
    """
    ...


def get_key_name() -> str:
    """
    Waits for a key to be pressed and return its name.
    """
    ...


def is_pressed(key: str | tuple[str] | list[str]) -> bool:
    """
    Checks if a key or a sequence of keys is being pressed.
    """
    ...


def is_pressed_once(key: str | tuple[str] | list[str]) -> bool:
    """
    Checks if a key or a sequence of keys is being pressed but only once :
    if the key was being pressed during the last call and is still being pressed,
    this function returns False... until key is released and pressed again.

    """
    ...

def move_mouse_relative(x: float | int, y: float | int) -> None:
    """
    Moves mouse relatively to current position.
    """
    ...

def move_mouse_absolute(x: float | int, y: float | int) -> None:
    """
    Moves mouse absolutely to coordinates (x,y).
    """
    ...

def continuous_relative_move(x: float | int, y: float | int, time_interval: float | int) -> None:
    """
    Moves mouse relatively and continuously during time_interval.
    Is blocking.
    """
    ...
