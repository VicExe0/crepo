from typing import Callable, NoReturn, Tuple, Union
from enum import IntFlag

import dearpygui.dearpygui as dpg

import win32gui
import win32con
import win32api
import ctypes
import time

def getHWND(title: str) -> int:
    return win32gui.FindWindow(None, title)

def getScreenDimensions() -> Tuple[ int, int ]:
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()

    width = user32.GetSystemMetrics(0)
    height = user32.GetSystemMetrics(1)

    return width, height

def enableClickThrough( hwnd: int ) -> NoReturn:
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT )

def enableTransparent( hwnd: int ) -> NoReturn:
    dpg.set_viewport_clear_color([ 0.0, 0.0, 0.0, 0.0 ])
    dwm = ctypes.windll.dwmapi
    margins = Margins(-1, -1, -1, -1)
    dwm.DwmExtendFrameIntoClientArea(hwnd, margins)

class Margins(ctypes.Structure):
    _fields_ = [
        ("cxLeftWidth", ctypes.c_int),
        ("cxRightWidth", ctypes.c_int),
        ("cyTopHeight", ctypes.c_int),
        ("cyBottomHeight", ctypes.c_int)
    ]

class WindowNotFoundError(Exception): ...

class Flags(IntFlag):
    NONE               = 0
    NO_TITLEBAR        = 1 << 0  # Dont create the draggable titlebar.
    TRANSPARENT        = 1 << 1  # Make viewport fully transparent.
    CENTERED           = 1 << 2  # Center the viewport on the screen.
    CLICK_THROUGH      = 1 << 3  # Allow mouse clicks to pass through the window. (widgets like buttons wont work when enabled)
    NO_SETUP           = 1 << 4  # Skip initial DearPyGui setup.
    DRAG_ONLY_TITLEBAR = 1 << 5  # Make only titlebar draggable. 
    PERCENTAGE_METRICS = 1 << 6  # Make the window dimensions be a % of the screen dimensions instead of hard coded values.
    ALWAYS_ON_TOP      = 1 << 7  # Make the window always on top
    NO_SCROLLBAR       = 1 << 8  # Disable scrollbar

    APPLICATION_CLOSE  = 1 << 9  # Close manual close event.
    APPLICATION_CRASH  = 1 << 10 # Error inside main loop.

class Viewport:
    def __init__( self, title: str, dimensions: Tuple[ Union[ int, float ], ... ], load_layout: Callable, flags: IntFlag = Flags.NONE ) -> None:
        if len(title) == 0:
            raise ValueError("Title has to be at least 1 character long")
        
        if len(dimensions) != 2:
            raise ValueError("Dimensions requires 2 values (int, int)")
        
        if not all(isinstance(x, (int, float)) and x > 0 for x in dimensions):
            raise ValueError("Dimensions has to be positive.")

        self.width, self.height = dimensions
        self.destroy_callback = lambda x: x
        self.frame_callback = lambda x: x 
        self.load_layout = load_layout
        self.close_event = Flags.NONE
        self.title = title

        self.run = False
        self.dragging = False
        self.begin_mouse_pos = ( 0, 0 )
        self.prev_mouse_pos = ( -1, -1 )
        self.offset = ( 0, 0 )
        self.hwnd = None

        screen_w, screen_h = getScreenDimensions()
        x_pos, y_pos = 100, 100

        if not ( flags & Flags.NO_SETUP ):
            dpg.create_context()
            dpg.setup_dearpygui()
        
        if flags & Flags.PERCENTAGE_METRICS:
            self.width = int(screen_w * self.width)
            self.height = int(screen_h * self.height)

        if flags & Flags.CENTERED:
            x_pos = screen_w // 2 - self.width // 2
            y_pos = screen_h // 2 - self.height // 2

        dpg.create_viewport(title=title, width=self.width, height=self.height, decorated=False, x_pos=x_pos, y_pos=y_pos)
        dpg.show_viewport()
        
        self.hwnd = getHWND(title)

        if not self.hwnd:
            raise WindowNotFoundError("Cannot find window's HWND.")

        if flags & Flags.TRANSPARENT: enableTransparent(self.hwnd)
        if flags & Flags.CLICK_THROUGH: enableClickThrough(self.hwnd)
        if flags & Flags.ALWAYS_ON_TOP: dpg.set_viewport_always_top(True)

        if not ( flags & Flags.NO_TITLEBAR ): 
            self.__createTitleBar(flags)

        else:
            load_layout()

    
    def close( self ) -> None:
        self.run = False

    def start( self, fps: int = 120 ) -> None:
        if fps <= 0:
            raise ValueError("FPS count has to be greater than 0.")

        frame_length = 1 / fps
        next_time = time.perf_counter()
        frame = 0

        self.run = True

        try:
            while dpg.is_dearpygui_running() and self.run:
                frame += 1

                self.__handleDragging()
                dpg.render_dearpygui_frame()

                self.frame_callback(frame)

                next_time += frame_length
                sleep_time = max(0, next_time - time.perf_counter())

                time.sleep(sleep_time)

                if frame >= fps:
                    frame = 0

        except Exception as e:
            print(e)
            self.close_event = Flags.APPLICATION_CRASH

        self.__background_cleanup()


    def setFont( self, path: str, size: int = 20 ) -> None:
        if not dpg.does_item_exist("font_registry"):
            with dpg.font_registry(tag="font_registry"):
                self.font = dpg.add_font(path, size)

        else:
            self.font = dpg.add_font(path, size, parent="font_registry")

        if dpg.does_item_exist("titlebar"):
            dpg.bind_item_font("titlebar", self.font)

        else:
            dpg.bind_font(self.font)

    def setFrameCallback( self, callback: Callable ) -> None:
        self.frame_callback = callback

    def setDestroyCallback( self, callback: Callable ) -> None:
        self.destroy_callback = callback
        

    def __createTitleBar( self, flags: int ) -> None:
        nsb = bool(flags & Flags.NO_SCROLLBAR)
        with dpg.window(label=self.title, tag="titlebar", width=self.width, height=self.height, no_resize=True, no_move=True, no_collapse=True, on_close=lambda: self.__quit(Flags.APPLICATION_CLOSE), no_scrollbar=nsb, no_scroll_with_mouse=nsb):
            
            if flags & Flags.DRAG_ONLY_TITLEBAR:

                with dpg.child_window(label=self.title, tag="content_container", border=False, width=self.width, autosize_y=True, parent="titlebar", menubar=False, no_scrollbar=nsb, no_scroll_with_mouse=nsb):
                    self.load_layout()
            else:
                self.load_layout()

    def __handleDragging( self ) -> None:
        if not dpg.does_item_exist("titlebar"):
            return

        if not dpg.is_mouse_button_down(dpg.mvMouseButton_Left):
            self.dragging = False

            return
        
        mouse_pos = win32api.GetCursorPos()
        
        if dpg.is_item_hovered("titlebar"):
            if not self.dragging:
                self.begin_mouse_pos = mouse_pos

                mouse_x, mouse_y = self.begin_mouse_pos

                rect = win32gui.GetWindowRect(self.hwnd)
                dx, dy, *_ = rect

                self.offset = ( mouse_x - dx, mouse_y - dy )

            self.dragging = True

        if self.dragging: self.__drag(mouse_pos)

    def __drag( self, mouse_pos: Tuple[ int, int ] ) -> None:
        mouse_x, mouse_y = mouse_pos

        if ( mouse_x, mouse_y ) != self.prev_mouse_pos:
            offset_x, offset_y = self.offset

            win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOP, mouse_x - offset_x, mouse_y - offset_y, 0, 0, win32con.SWP_NOSIZE | win32con.SWP_NOZORDER)

            self.prev_mouse_pos = ( mouse_x, mouse_y )

    def __quit( self, quit_event: IntFlag = Flags.NONE ) -> NoReturn:
        if not self.run: return
        
        self.run = False
        self.close_event = quit_event
        dpg.stop_dearpygui()

        if self.hwnd:
            win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)

    def __background_cleanup( self ):
        dpg.destroy_context()
        self.destroy_callback(self.close_event)