from typing import Tuple, Callable, Union
from enum import IntFlag

class Flags(IntFlag):
    """
    Flags for viewport configuration.

    ### Flags:
        `NO_TITLEBAR`:        int - Dont create the draggable titlebar.
        `TRANSPARENT`:        int - Make viewport fully transparent.
        `CENTERED`:           int - Center the viewport on the screen.
        `CLICK_THROUGH`:      int - Allow mouse clicks to pass through the window. (widgets like buttons wont work when enabled)
        `NO_SETUP`:           int - Skip initial DearPyGui setup.
        `DRAG_ONLY_TITLEBAR`: int - Make only titlebar draggable. 
        `PERCENTAGE_METRICS`: int - Make the window dimensions be a % of the screen dimensions instead of hard coded values.
        `ALWAYS_ON_TOP`:      int - Make the window always on top.
        `NO_SCROLLBAR`:       int - Disable scrollbar.
        `APPLICATION_CLOSE`:  int - Close manual close event.
        `APPLICATION_CRASH`:  int - Error inside main loop.
    """

    NONE:               int
    NO_TITLEBAR:        int
    TRANSPARENT:        int
    CENTERED:           int
    CLICK_THROUGH:      int
    NO_SETUP:           int
    DRAG_ONLY_TITLEBAR: int
    PERCENTAGE_METRICS: int
    ALWAYS_ON_TOP:      int
    NO_SCROLLBAR:       int
    APPLICATION_CLOSE:  int
    APPLICATION_CRASH:  int

class Viewport:
    def __init__( self, title: str, dimensions: Tuple[ Union[ int, float ], ... ], load_layout: Callable, flags: IntFlag = Flags.NONE ) -> None:
        """
        Initialize viewport.

        ### Args:
            `title`:          str               - Window title.
            `dimensions`:     tuple(uint,u int) - (width, height) of the viewport.
            `load_layout`:    callable          - Function that will be called inside the window (contains all dearpygui widgets).
            `frame_callback`: callable(int)     - Optional function called each frame, receives frame count as int.
            `flags`:          IntFlag           - Bitmask of Flags to control viewport behavior.
        """

    def close( self ) -> None:
        """Close the viewport."""

    def start( self, fps: int = 120 ) -> None:
        """
        Start the main loop.

        ### Args:
            `fps`:    int - Frames per second target.
        """

    def setFont( self, path: str, size: int = 20 ) -> None:
        """
        Set custom default font.

        ### Args:
            `path`: str - Path to .ttf file
            `size`: int - Default font size 
        """

    def setFrameCallback( self, callback: Callable ) -> None:
        """
        Set frame callback.

        ### Args:
            `callback`: Callable - Function that will be called every frame (accepts 1 int argument - current frame count)
        """

    def setDestroyCallback( self, callback: Callable ) -> None:
        """
        Set close/destroy callback.

        ### Args:
            `callback`: Calable - Function that will be called when application closes/crashes.
        """