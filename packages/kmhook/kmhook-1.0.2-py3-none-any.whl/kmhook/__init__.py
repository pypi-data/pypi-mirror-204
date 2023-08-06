import sys

if sys.platform == 'win32':
    from kmhook._kmhook_win import *
else:
    print('kmHook is not supported on this platform.')
    from kmhook._kmhook_other import *
