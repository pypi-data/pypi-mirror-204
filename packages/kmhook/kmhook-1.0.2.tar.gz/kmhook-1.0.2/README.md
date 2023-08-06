# `kmHook`


`kmHook` only works on Windows, is pure Python using only `ctypes`, `time` and no other dependencies.

`kmHook` currently, only french AZERTY keyboards are supported.

`kmHook` allows you to detect, synthesize keyboard & mouse events.

`kmHook` also implements various related functions, see below.


# Example

```python
import kmhook as km

while not km.is_pressed('pause'):
    km.sleep(0.001) # recommended so that you don't consume CPU
    if km.is_pressed_once('space'):
        km.continuous_relative_move(600, 400, 500) # moves mouse smoothly during 500ms
```


`get_valid_key_names() -> tuple`

Returns all the valid key names to use within kmHook

    
`is_pressed(key: str | tuple[str] | list[str]) -> bool`

Checks if a key or a sequence of keys is being pressed.
    
`is_pressed_once(key: str | tuple[str] | list[str]) -> bool`

Checks if a key or a sequence of keys is being pressed but only once :
if the key was being pressed during the last call and is still being pressed,
this function returns False... until key is released and pressed again.
    
`press(key: str | list | tuple) -> None`

Presses the key (a single str or a sequence of keys) but does not release it
    
`press_and_release(key: str | list | tuple) -> None`

Presses and releases the key or the sequence of keys.
    
`release(key: str | list | tuple) -> None`

Releases the key (a single str or a sequence of keys).
    
`get_key_name() -> str`
        
Waits for a key to be pressed and return its name.
    
`get_mouse_pos() -> tuple[int, int]`

Returns current mouseposition.
        
`move_mouse_absolute(x: float | int, y: float | int) -> None`

Moves mouse absolutely to coordinates (x,y).
    
`move_mouse_relative(x: float | int, y: float | int) -> None`

Moves mouse relatively to current position.

`continuous_relative_move(x: float | int, y: float | int, time_interval: float | int) -> None`

Moves mouse relatively, smoothly and continuously during time_interval. Is blocking.
