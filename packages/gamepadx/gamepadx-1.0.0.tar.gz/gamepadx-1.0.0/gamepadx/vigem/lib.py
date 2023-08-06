from pathlib import Path
from ctypes import CDLL, c_void_p, c_uint
from gamepadx.commons import XInputGamepad

path = Path(__file__).parent.absolute() / "ViGEmClient.dll"
api = CDLL(str(path))

"""
Allocates an object representing a driver connection
"""
vigem_alloc = api.vigem_alloc
vigem_alloc.argtypes = ()
vigem_alloc.restype = c_void_p

"""
Frees up memory used by the driver connection object
"""
vigem_free = api.vigem_free
vigem_free.argtypes = (c_void_p,)
vigem_free.restype = None

"""
Initializes the driver object and establishes a connection to the emulation bus driver
"""
vigem_connect = api.vigem_connect
vigem_connect.argtypes = (c_void_p,)
vigem_connect.restype = c_uint

"""
Disconnects from the bus device and resets the driver object state
"""
vigem_disconnect = api.vigem_disconnect
vigem_disconnect.argtypes = (c_void_p,)
vigem_disconnect.restype = None

"""
Allocates an object representing an Xbox 360 Controller device
"""
vigem_target_x360_alloc = api.vigem_target_x360_alloc
vigem_target_x360_alloc.argtypes = ()
vigem_target_x360_alloc.restype = c_void_p

"""
Frees up memory used by the target device object
"""
vigem_target_free = api.vigem_target_free
vigem_target_free.argtypes = (c_void_p,)
vigem_target_free.restype = None

"""
Adds a provided target device to the bus driver
"""
vigem_target_add = api.vigem_target_add
vigem_target_add.argtypes = (c_void_p, c_void_p)
vigem_target_add.restype = c_uint

"""
Removes a provided target device from the bus driver
"""
vigem_target_remove = api.vigem_target_remove
vigem_target_remove.argtypes = (c_void_p, c_void_p)
vigem_target_remove.restype = c_uint

"""
Sends a state report to the provided target device
"""
vigem_target_x360_update = api.vigem_target_x360_update
vigem_target_x360_update.argtypes = (c_void_p, c_void_p, XInputGamepad)
vigem_target_x360_update.restype = c_uint
