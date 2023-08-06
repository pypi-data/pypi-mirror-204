from gamepadx.commons import *
from ctypes import windll, pointer, c_void_p
from ctypes.wintypes import WORD
import gamepadx.vigem.lib as vigem_lib


TRIGGER_MAGNITUDE = 256
THUMB_MAGNITUDE = 32768


class Gamepad:
    """
    Reads the current state of the Xbox 360 Controller
    """

    def __init__(self, index: int | None = 0) -> None:
        self.lib = windll.xinput1_4
        self.index = index
        self.state = XInputState()

    def update(self) -> None:
        """
        Writes the current state of the controller to an internal state
        """
        code: int = self.lib.XInputGetState(WORD(self.index), pointer(self.state))
        if code != 0:
            raise Exception(f"The controller ({self.index}) is not connected.")

    def is_button_pressed(self, button: XInputButtons) -> bool:
        """
        Returns the internal state of the given button
        """
        return bool(button & self.state.Gamepad.wButtons)

    def get_trigger_value(self, trigger: XInputTriggers) -> float:
        """
        Returns the internal state value of the given trigger
        """
        return (getattr(self.state.Gamepad, trigger) & 0xFF) / TRIGGER_MAGNITUDE

    def get_thumb_value(self, thumb: XInputThumbs) -> float:
        """
        Returns the internal state value of the given thumbstick
        """
        return getattr(self.state.Gamepad, thumb) / THUMB_MAGNITUDE


class VBus:
    def __init__(self) -> None:
        self.client: c_void_p = vigem_lib.vigem_alloc()
        exception_wrapper(vigem_lib.vigem_connect(self.client))

    def __del__(self) -> None:
        vigem_lib.vigem_disconnect(self.client)
        vigem_lib.vigem_free(self.client)


class VirtualGamepad:
    """
    Emulates an Xbox 360 Controller device
    """

    def __init__(self) -> None:
        self.bus = VBus()

        self.pad: c_void_p = vigem_lib.vigem_target_x360_alloc()
        exception_wrapper(vigem_lib.vigem_target_add(self.bus.client, self.pad))

        self.vigem_report = XInputGamepad()

    def press_button(self, button: XInputButtons) -> None:
        """
        Presses the virtual button to an internal state
        """
        self.vigem_report.wButtons = self.vigem_report.wButtons | button

    def release_button(self, button: XInputButtons) -> None:
        """
        Releases the virtual button to an internal state
        """
        self.vigem_report.wButtons = self.vigem_report.wButtons & ~button

    def set_trigger_value(self, trigger: XInputTriggers, value: float) -> None:
        """
        Sets the value of the virtual trigger to an internal state
        """
        setattr(self.vigem_report, trigger, round(value * TRIGGER_MAGNITUDE))

    def set_thumb_value(self, thumb: XInputThumbs, value: float) -> None:
        """
        Sets the value of the virtual thumbstick axis to an internal state
        """
        setattr(self.vigem_report, thumb, round(value * THUMB_MAGNITUDE))

    def update(self) -> None:
        """
        Sends the internal state to the virtual device
        """
        exception_wrapper(
            vigem_lib.vigem_target_x360_update(
                self.bus.client, self.pad, self.vigem_report
            )
        )

    def reset(self) -> None:
        """
        Sets the internal state to a default state
        """
        self.vigem_report = XInputGamepad()

    def __del__(self) -> None:
        vigem_lib.vigem_target_remove(self.bus.client, self.pad)
        vigem_lib.vigem_target_free(self.pad)
