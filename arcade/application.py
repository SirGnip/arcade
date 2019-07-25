"""
The main window class that all object-oriented applications should
derive from.
"""
from numbers import Number
from typing import Tuple

import pyglet.gl as gl

from arcade.monkey_patch_pyglet import *
from arcade.window_commands import (get_viewport, get_window, schedule,
                                    set_background_color, set_viewport,
                                    set_window, unschedule)

MOUSE_BUTTON_LEFT = 1
MOUSE_BUTTON_MIDDLE = 2
MOUSE_BUTTON_RIGHT = 4


class Window(pyglet.window.Window):
    """
    The Window class forms the basis of most advanced games that use Arcade.
    It represents a window on the screen, and manages events.
    """

    def __init__(self, width: float = 800, height: float = 600,
                 title: str = 'Arcade Window', fullscreen: bool = False,
                 resizable: bool = False, update_rate=1/60,
                 antialiasing=True):
        """
        Construct a new window

        :param float width: Window width
        :param float height: Window height
        :param str title: Title (appears in title bar)
        :param bool fullscreen: Should this be full screen?
        :param bool resizable: Can the user resize the window?
        :param float update_rate: How frequently to update the window.
        :param bool antialiasing: Should OpenGL's anti-aliasing be enabled?
        """
        if antialiasing:
            config = pyglet.gl.Config(major_version=3,
                                      minor_version=3,
                                      double_buffer=True,
                                      sample_buffers=1,
                                      samples=4)
        else:
            config = pyglet.gl.Config(major_version=3,
                                      minor_version=3,
                                      double_buffer=True)

        super().__init__(width=width, height=height, caption=title,
                         resizable=resizable, config=config)

        if antialiasing:
            try:
                gl.glEnable(gl.GL_MULTISAMPLE_ARB)
            except pyglet.gl.GLException:
                print("Warning: Anti-aliasing not supported on this computer.")

        if update_rate:
            from pyglet import compat_platform
            if compat_platform == 'darwin' or compat_platform == 'linux':
                # Set vsync to false, or we'll be limited to a 1/30 sec update rate possibly
                self.context.set_vsync(False)
            self.set_update_rate(update_rate)

        super().set_fullscreen(fullscreen)
        self.invalid = False
        set_window(self)
        set_viewport(0, self.width, 0, self.height)
        self._screen_registry = {}

    def update(self, delta_time: float):
        """
        Move everything. For better consistency in naming, use ``on_update`` instead.

        :param float delta_time: Time interval since the last time the function was called.

        """
        pass

    def on_update(self, delta_time: float):
        """
        Move everything. Perform collision checks. Do all the game logic here.

        :param float delta_time: Time interval since the last time the function was called.

        """
        pass

    def set_update_rate(self, rate: float):
        """
        Set how often the screen should be updated.
        For example, self.set_update_rate(1 / 60) will set the update rate to 60 fps

        :param float rate: Update frequency in seconds
        """
        self._update_rate = rate
        unschedule(self.update)
        schedule(self.update, self._update_rate)
        unschedule(self.on_update)
        schedule(self.on_update, self._update_rate)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        """
        Override this function to add mouse functionality.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        """
        pass

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x: x position of the mouse
        :param float y: y position of the mouse
        :param int button: What button was hit. One of: arcade.MOUSE_BUTTON_LEFT, arcade.MOUSE_BUTTON_RIGHT, arcade.MOUSE_BUTTON_MIDDLE
        :param int modifiers: Shift/click, ctrl/click, etc.
        """
        pass

    def on_mouse_drag(self, x: float, y: float, dx: float, dy: float, buttons: int, modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x: x position of mouse
        :param float y: y position of mouse
        :param float dx: Change in x since the last time this method was called
        :param float dy: Change in y since the last time this method was called
        :param int buttons: Which button is pressed
        :param int modifiers: Ctrl, shift, etc.
        """
        self.on_mouse_motion(x, y, dx, dy)

    def on_mouse_release(self, x: float, y: float, button: int,
                         modifiers: int):
        """
        Override this function to add mouse button functionality.

        :param float x:
        :param float y:
        :param int button:
        :param int modifiers:
        """

        pass

    def on_mouse_scroll(self, x: int, y: int, scroll_x: int, scroll_y: int):
        """
        User moves the scroll wheel.

        :param int x:
        :param int y:
        :param int scroll_x:
        :param int scroll_y:
        """
        pass

    def set_mouse_visible(self, visible: bool=True):
        """
        If true, user can see the mouse cursor while it is over the window. Set false,
        the mouse is not visible. Default is true.

        :param bool visible:
        """
        super().set_mouse_visible(visible)

    def on_key_press(self, symbol: int, modifiers: int):
        """
        Override this function to add key press functionality.

        :param int symbol: Key that was hit
        :param int modifiers: If it was shift/ctrl/alt
        """
        pass

    def on_key_release(self, symbol: int, modifiers: int):
        """
        Override this function to add key release functionality.

        :param int symbol: Key that was hit
        :param int modifiers: If it was shift/ctrl/alt
        """
        pass

    def on_draw(self):
        """
        Override this function to add your custom drawing code.
        """

        pass

    def on_resize(self, width: float, height: float):
        """
        Override this function to add custom code to be called any time the window
        is resized.

        :param float width: New width
        :param float height: New height
        """
        original_viewport = self.get_viewport()

        # unscaled_viewport = self.get_viewport_size()
        # scaling = unscaled_viewport[0] / width

        self.set_viewport(original_viewport[0],
                          original_viewport[0] + width,
                          original_viewport[2],
                          original_viewport[2] + height)

    def set_min_size(self, width: float, height: float):
        """ Wrap the Pyglet window call to set minimum size

        :param float width: width in pixels.
        :param float height: height in pixels.
        """

        if self._resizable:
            super().set_minimum_size(width, height)
        else:
            raise ValueError('Cannot set min size on non-resizable window')

    def set_max_size(self, width: float, height: float):
        """ Wrap the Pyglet window call to set maximum size

        :param float width: width in pixels.
        :param float height: height in pixels.
        :Raises ValueError:

        """

        if self._resizable:
            super().set_maximum_size(width, height)
        else:
            raise ValueError('Cannot set max size on non-resizable window')

    def set_size(self, width: float, height: float):
        """
        Ignore the resizable flag and set the size

        :param float width:
        :param float height:
        """

        super().set_size(width, height)

    def get_size(self) -> Tuple[int, int]:
        """
        Get the size of the window.

        :returns: (width, height)
        """

        return super().get_size()

    def get_location(self) -> Tuple[int, int]:
        """
        Return the X/Y coordinates of the window

        :returns: x, y of window location
        """

        return super().get_location()

    def set_visible(self, visible=True):
        """
        Set if the window is visible or not. Normally, a program's window is visible.

        :param bool visible:
        """
        super().set_visible(visible)

    def set_viewport(self, left: Number, right: Number, bottom: Number, top: Number):
        """
        Set the viewport. (What coordinates we can see.
        Used to scale and/or scroll the screen.)

        :param Number left:
        :param Number right:
        :param Number bottom:
        :param Number top:
        """
        set_viewport(left, right, bottom, top)

    def get_viewport(self) -> (float, float, float, float):
        """ Get the viewport. (What coordinates we can see.) """
        return get_viewport()

    def test(self, frames: int = 10):
        """
        Used by unit test cases. Runs the event loop a few times and stops.

        :param int frames:
        """
        for i in range(frames):
            self.switch_to()
            self.dispatch_events()
            self.dispatch_event('on_draw')
            self.flip()
            self.update(1/60)


def open_window(width: Number, height: Number, window_title: str, resizable: bool = False,
                antialiasing=True) -> Window:
    """
    This function opens a window. For ease-of-use we assume there will only be one window, and the
    programmer does not need to keep a handle to the window. This isn't the best architecture, because
    the window handle is stored in a global, but it makes things easier for programmers if they don't
    have to track a window pointer.

    :param Number width: Width of the window.
    :param Number height: Height of the window.
    :param str window_title: Title of the window.
    :param bool resizable: Whether the window can be user-resizable.
    :param bool antialiasing: Smooth the graphics?

    :returns: Handle to window
    :rtype arcade.Window:
    """

    global _window
    _window = Window(width, height, window_title, resizable, update_rate=None,
                     antialiasing=antialiasing)
    return _window


def set_screen(screen_class: Window, reset=False):
    """
    - Create a registry of pointers for each view.
    - If reset=True or the view doesnt exist in registry, create a new object
    - else (exists), use the pointer from the registry

    TODO:Thoughts:
    - should reset be True by default?

    TODO:
    - Passing data between screens (using global variables or object data fields?)
        - arcade.pass_data_to_screen(GameScreen, {'foo': 1, 'bar', 2}) ??
    - Screen inheritance (Multiple levels) sharing keybinds and draw (whatever needed)
    """

    class DefaultWindow(Window):
        """Inherit the methods without actually spinning up a new pyglet window"""
        def __init__(self):
            pass

    default_window = DefaultWindow()
    window = get_window()

    if reset or screen_class.__name__ not in window._screen_registry.keys():
        screen = screen_class()
        window._screen_registry[screen_class.__name__] = screen
    else:
        screen = window._screen_registry[screen_class.__name__]

    overridable_methods = ['on_draw', 'on_hide', 'on_key_press',
                           'on_key_release', 'on_mouse_drag', 'on_mouse_enter',
                           'on_mouse_leave', 'on_mouse_motion', 'on_mouse_press',
                           'on_mouse_release', 'on_mouse_scroll', 'on_move',
                           'on_resize', 'on_text', 'on_text_motion',
                           'on_text_motion_select', 'on_update', 'update']

    # unschedule the previous screen's update methods
    unschedule(window.update)
    unschedule(window.on_update)

    # set the screen's background color
    try:
        set_background_color(screen.__class__.background_color)
    except AttributeError:
        pass  # no background color specified, keeping current
    except TypeError:
        # Not a valid color argument
        raise TypeError(f"'{screen.__class__.background_color}'"
                        " is not a valid color.") from None

    # Copy over the methods from the new screen
    for method_name in overridable_methods:
        try:
            # override current window method with the one
            # in the new screen
            setattr(window, method_name, getattr(screen, method_name))
            # print(f"Set window.{method_name} to {screen_class.__name__}.{method_name}")
        except AttributeError:
            # Use original version of the method from
            # the Window class if not found in the new screen.

            # print(f"'{method_name}' not found in {screen_class.__name__}")

            if hasattr(default_window, method_name):
                # There are pyglet window methods that can be overridden
                # that are not part of the arcade.Window class
                setattr(window, method_name, getattr(default_window, method_name))

    # schedule the new screen's update methods
    schedule(window.update, window._update_rate)
    schedule(window.on_update, window._update_rate)
