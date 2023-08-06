from ctypes import Structure, c_uint
from ctypes.wintypes import WORD, BYTE, SHORT, DWORD
from enum import IntFlag, StrEnum, IntEnum


class XInputGamepad(Structure):
    """
    Describes the current state of the Xbox 360 Controller
    """

    _fields_ = [
        ("wButtons", WORD),
        ("bLeftTrigger", BYTE),
        ("bRightTrigger", BYTE),
        ("sThumbLX", SHORT),
        ("sThumbLY", SHORT),
        ("sThumbRX", SHORT),
        ("sThumbRY", SHORT),
    ]


class XInputState(Structure):
    """
    Represents the state of a controller
    """

    _fields_ = [("dwPacketNumber", DWORD), ("Gamepad", XInputGamepad)]


class XInputButtons(IntFlag):
    """
    Bitmask of the device digital buttons
    """

    DPAD_UP = 0x0001
    DPAD_DOWN = 0x0002
    DPAD_LEFT = 0x0004
    DPAD_RIGHT = 0x0008
    START = 0x0010
    BACK = 0x0020
    LEFT_THUMB = 0x0040
    RIGHT_THUMB = 0x0080
    LEFT_SHOULDER = 0x0100
    RIGHT_SHOULDER = 0x0200
    A = 0x1000
    B = 0x2000
    X = 0x4000
    Y = 0x8000


class XInputTriggers(StrEnum):
    """
    Mapping of the device analog triggers
    """

    LEFT = "bLeftTrigger"
    RIGHT = "bRightTrigger"


class XInputThumbs(StrEnum):
    """
    Mapping of the device analog thumbsticks
    """

    LEFT_X = "sThumbLX"
    LEFT_Y = "sThumbLY"
    RIGHT_X = "sThumbRX"
    RIGHT_Y = "sThumbRY"


class ViGEmErrors(IntEnum):
    """
    Values that represent ViGEm errors
    """

    NONE = 0x20000000
    BUS_NOT_FOUND = 0xE0000001
    NO_FREE_SLOT = 0xE0000002
    INVALID_TARGET = 0xE0000003
    REMOVAL_FAILED = 0xE0000004
    ALREADY_CONNECTED = 0xE0000005
    TARGET_UNINITIALIZED = 0xE0000006
    TARGET_NOT_PLUGGED_IN = 0xE0000007
    BUS_VERSION_MISMATCH = 0xE0000008
    BUS_ACCESS_FAILED = 0xE0000009
    CALLBACK_ALREADY_REGISTERED = 0xE0000010
    CALLBACK_NOT_FOUND = 0xE0000011
    BUS_ALREADY_CONNECTED = 0xE0000012
    BUS_INVALID_HANDLE = 0xE0000013
    XUSB_USERINDEX_OUT_OF_RANGE = 0xE0000014
    INVALID_PARAMETER = 0xE0000015
    NOT_SUPPORTED = 0xE0000016
    WINAPI = 0xE0000017
    TIMED_OUT = 0xE0000018
    IS_DISPOSING = 0xE0000019


def exception_wrapper(code: c_uint):
    """
    Handle possible ViGEm errors
    """
    if code != ViGEmErrors.NONE:
        raise Exception(ViGEmErrors(code).name)
