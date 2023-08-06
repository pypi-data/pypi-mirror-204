import multiprocessing
import sys
from typing import Optional, Tuple, List
from typeguard import typechecked

from multiprocessing import Process, Pipe, current_process

from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication

from ._io_window import IOWindow
from ._io_messages import IOMessage
# noinspection PyUnresolvedReferences
from .colors import BLACK, WHITE, RED, ORANGE, YELLOW, GREEN, TEAL, SKY, BLUE, VIOLET, PINK, RGBColor
from .basic_io_error import BasicIOError
from .image_objects import ImageObject


# ---------------- public API ----------------

# --- start the session (open window)

def start() -> None:
    """
    This function opens the io window and we can start interacting with it.

    This should be the first statement in your code.
    Starting is done implicitly, if needed, but it is cleaner to open
    the window explicitly.
    """
    if current_process().name != "basicio_windowproc":
        if __window_process is None:
            __start_window_process()
        else:
            print("warning: basic_io.start() has been called explicitly "
                  "but the window process is already running. "
                  "This call has been ignored.")

# --- drawing & painting


@typechecked
def draw_line(start_x: int, start_y: int, end_x: int, end_y: int,
              color: RGBColor = BLACK, thickness: int = 1) -> None:
    """
    Draw a line on the currently active image.

    :param start_x: start of the line (x-coordinate) [pixel]
    :param start_y: start of the line (y-coordinate) [pixel]
    :param end_x: end of the line (x-coordinate) [pixel]
    :param end_y: end of the line (y-coordinate) [pixel]
    :param color: color of the line (default: black) [0..255]³
    :param thickness: line thickness, default 1 [pixel]
    """
    _try_post_msg(IOMessage('draw_line',
                            {
                                'start_x': start_x, 'start_y': start_y,
                                'end_x': end_x, 'end_y': end_y,
                                'color': color, 'thickness': thickness
                            })
                  )


@typechecked
def draw_circle(x: int, y: int, radius: int,
                fill_color: Optional[RGBColor] = BLACK, border_color: Optional[RGBColor] = BLACK,
                border_thickness: int = 1) -> None:
    """
    Draw a circle on the currently active image.

    :param x: center of the ellipse, x-coordinate [pixel]
    :param y: center of the ellipse, y-coordinate [pixel]
    :param radius: radius of the circle [pixel]
    :param fill_color: the color for filling the polygon. can be set to None (then, shape is not filled)  [0...255]³
    :param border_color:  the color for the border of the polygon.
                          can be set to None (then, shape is not filled) [0...255]³
    :param border_thickness: the thickness of the border (a value of zero also turns off borders) [pixel]
    """
    draw_ellipse(x, y, radius, radius, fill_color, border_color, border_thickness)


@typechecked
def draw_ellipse(x: int, y: int, radius_x: int, radius_y: int,
                 fill_color: Optional[RGBColor] = BLACK, border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1) -> None:
    """
    Draw an axis-aligned ellipse on the currently active image.

    :param x: center of the ellipse, x-coordinate
    :param y: center of the ellipse, y-coordinate
    :param radius_x: radius in x-direction
    :param radius_y: radius in y-direction
    :param fill_color: the color for filling the polygon. can be set to None (then, shape is not filled)  [0...255]³
    :param border_color:  the color for the border of the polygon.
                          can be set to None (then, shape is not filled) [0...255]³
    :param border_thickness: the thickness of the border (a value of zero also turns off borders) [pixel]
    """
    _try_post_msg(IOMessage('draw_ellipse',
                            {
                                'x': x, 'y': y,
                                'radius_x': radius_x, 'radius_y': radius_y,
                                'fill_color': fill_color, 'border_color': border_color,
                                'border_thickness': border_thickness
                            })
                  )


@typechecked
def draw_rectangle(x: int, y: int, width: int, height: int,
                   fill_color: Optional[RGBColor] = BLACK, border_color: Optional[RGBColor] = BLACK,
                   border_thickness: int = 1) -> None:
    """
    Draw a rectangle on the currently active image.

    :param x: x-coordinate of upper left corner [pixel]
    :param y: y-coordinate of upper left corner [pixel]
    :param width: width of the rectangle [pixel]
    :param height: height of the rectangle [pixel]
    :param fill_color: the color for filling the polygon. can be set to None (then, shape is not filled)  [0...255]³
    :param border_color:  the color for the border of the polygon.
                          can be set to None (then, shape is not filled) [0...255]³
    :param border_thickness: the thickness of the border (a value of zero also turns off borders) [pixel]
    """
    _try_post_msg(IOMessage('draw_rectangle',
                            {
                                'x': x, 'y': y,
                                'width': width, 'height': height,
                                'fill_color': fill_color, 'border_color': border_color,
                                'border_thickness': border_thickness
                            })
                  )


@typechecked
def draw_polygon(points: List[Tuple[int, int]],
                 fill_color: Optional[RGBColor] = BLACK, border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1) -> None:
    """
    Draw a polygon on the currently active image.

    :param points: a list of tuples (x:int, y:int) of x- and y-coordinates of the points of the polygon to be drawn
                   ([pixel] x [pixel])^num_points
    :param fill_color: the color for filling the polygon. can be set to None (then, shape is not filled)  [0...255]³
    :param border_color:  the color for the border of the polygon.
                          can be set to None (then, shape is not filled) [0...255]³
    :param border_thickness: the thickness of the border (a value of zero also turns off borders) [pixel]
    """
    _try_post_msg(IOMessage('draw_polygon',
                            {
                                'points': points,
                                'fill_color': fill_color, 'border_color': border_color,
                                'border_thickness': border_thickness
                            })
                  )


@typechecked
def draw_text(x: int, y: int, text: str,
              color: RGBColor = BLACK, background_color: Optional[RGBColor] = None,
              font_height: int = 16) -> None:
    """
    Draws text at an arbitrary position on the currently active image.

    :param x: x coordinate where the text starts (upper-left corner) [pixel]
    :param y: y coordinate where the text starts (upper-left corner) [pixel]
    :param text: text to be printed [string]
    :param color: the color to be used (optional, default=BLACK) [0...255]³
    :param background_color: optional argument that specifies the background fill color [0...255]³
    :param font_height: the height of the characters in pixel (optional, default=16 pixel) [pixel]
    """
    _try_post_msg(IOMessage('draw_text',
                            {
                                'x': x, 'y': y, 'text': text,
                                'color': color,  'background_color': background_color,
                                'font_height': font_height,
                            })
                  )


@typechecked
def draw_pixel(x: int, y: int, color: RGBColor = BLACK) -> None:
    """
    Changes the color of a single pixel in the active buffer

    :param x: x coordinate of the pixel
    :param y: y coordinate of the pixel
    :param color: the color to be used (optional, default=BLACK) [0...255]³
    """
    _try_post_msg(IOMessage('draw_pixel',
                            {
                                'x': x, 'y': y, 'color': color
                            })
                  )


@typechecked
def read_pixel(x: int, y: int) -> RGBColor:
    """
    Reads the color of the specified pixel from the active buffer.

    :param x: x coordinate of the pixel
    :param y: y coordinate of the pixel
    :result: An RGB Tuple from {0,1,2,...,255}^3 or (-1, -1, -1) if something went wrong
             (in particular, if the specified pixel coordinate was outside the buffer)
    """
    reply: IOMessage = _try_query_msg(IOMessage('read_pixel', {'x': x, 'y': y}))
    if reply.msg_type == 'pixel_color':
        return reply.params['color']
    else:
        return -1, -1, -1


# --- loading and drawing images from files (for sprites/bobs/icons)


def load_image(filename: str) -> int:
    """
    Loads an image into an internal image database from an external file.

    :param filename: the filename of the image file.
                     The function accepts both png and jpg files. png-files with transparency are rendered
                     correctly (with transparent pixels / using the alpha-channel). This can be used for
                     defining sprites for games or icons for UIs or the similar.
    :return: an integer index under which the image has been stored internally.
             In case of errors (such as "file not found"), index -1 is returned.
             Images can only have positive indices 0,1,2,3,...
             Thus, -1 is always an invalid image (and cannot be used to draw on the screen)
    """
    reply: IOMessage = _try_query_msg(IOMessage('load_image', {'filename': filename}))
    if reply.msg_type == 'image_loaded':
        return reply.params['index']
    else:
        return -1


def draw_image(x: int, y: int, index: int) -> None:
    """
    Draws an image to the screen (more precisely, the active buffer).

    :param x: x-coordinate of top-left pixel of the image to be drawn
    :param y: y-coordinate of the top-left pixel of the image to be drawn
    :param index: index of the image in the internal database. Invalid indices will be ignored (no action taken).
    """
    _try_post_msg(IOMessage('draw_image',
                            {
                                'x': x, 'y': y, 'index': index
                            })
                  )

# --- Object oriented API (draw complex objects onto the screen; similar to the "PYRET"-lang "image" library)


@typechecked
def draw_object(obj: ImageObject, x: int = 0, y: int = 0) -> None:
    """
    Draws a (potentially complex/composite) image object onto the screen.
    See module :module: image_objects.py for choices.

    :param obj: The image object to be drawn.
    :param x: (optional) offset in x-direction; by default, the shape is drawn in the top left corner (x-offset 0)
    :param y: (optional) offset in y-direction; by default, the shape is drawn in the top left corner (y-offset 0)
    """
    _try_post_msg(IOMessage('draw_image_object',
                            {
                                'obj': obj, 'x': x, 'y': y,
                            })
                  )


# --- Controlling the images to be drawn to (visibility, size, active images, clearing images)


@typechecked
def clear_image(color: RGBColor = WHITE) -> None:
    """
    This image clears the active image, overwriting all pixels with a fixed color.
    By default, the color is white.

    :param color: the color with which the image is overwritten. Defaults to WHITE if not given.
    """
    draw_rectangle(0, 0, 10001, 10001, color, None, 0)  # we just draw a very big rectangle relying on build-in clipping


@typechecked
def set_active_image(buffer: int) -> None:
    """
    This command chooses which image the draw commands are directed to (which image to draw on).

    basic_io provides 10 "buffers", indexed by 0 to 9.
    Numbers smaller than 0 or larger than 9 cause an exception.
    If the buffer does not yet exist, it will be automatically created (with the default size of 640x480 pixel).
    By default, buffer 0 is active and visible.

    :param buffer: index of the buffer to draw to in the future
    """
    if buffer < 0 or buffer > 9:
        raise BasicIOError("set_active_image can only be called with indices between 0 and 9 "
                           "(there are only ten images available).")
    _try_post_msg(IOMessage('set_active_image',
                            {
                                'buffer': buffer
                            })
                  )


@typechecked
def set_visible_image(buffer: int) -> None:
    """
    This command chooses which image is currently visible.

    By default, this is the same as the active image, that
    we are drawing on. In general, visible and active image can be different (for example, to implement double
    buffering to avoid flicker).
    basic_io provides 10 "buffers", indexed by 0 to 9.
    Numbers smaller than 0 or larger than 9 cause an exception.
    If the buffer does not yet exist, it will be automatically created (with the default size of 640x480 pixel,
    initialized with a white background).
    By default, buffer 0 is active and visible.

    :param buffer: index of the buffer that will be visible from now on.
    """
    if buffer < 0 or buffer > 9:
        raise BasicIOError("set_visible_image can only be called with indices between 0 and 9 "
                           "(there are only ten images available).")
    _try_post_msg(IOMessage('set_visible_image',
                            {
                                'buffer': buffer
                            })
                  )


@typechecked
def copy_image(from_buffer: int, to_buffer: int) -> None:
    """
    This command copies the content of an image from one buffer to another.

    The width/height of the destination will be set to that of the source.

    :param from_buffer: source buffer [0,1,...,9]
    :param to_buffer: destination buffer [0,1,...,9]
    """
    if from_buffer < 0 or from_buffer > 9 or to_buffer < 0 or to_buffer > 9:
        raise BasicIOError("buffers indices must be between 0 and 9 "
                           "(there are only ten images available).")
    _try_post_msg(IOMessage('copy_image',
                            {
                                'from_buffer': from_buffer,
                                'to_buffer': to_buffer
                            })
                  )


@typechecked
def resize_image(width: int, height: int, color: RGBColor = WHITE) -> None:
    """
    This image clears the active image, overwriting all pixels with a fixed color.

    By default, the color is white.

    :param width: new width of the image in pixel, must be in range [1,2,...,10000]
    :param height: new height of the image in pixel, must be in range [1,2,...,10000]
    :param color: the color with which the image is overwritten. Defaults to WHITE if not given.
    """
    if width < 1 or height < 1:
        raise BasicIOError("Width and height of an image must be at least 1")
    if width > 10000 or height > 10000:
        raise BasicIOError("Width and height cannot be larger than 10000 pixels.")
    _try_post_msg(IOMessage('resize_image',
                            {
                                'width': width, 'height': height, 'color': color
                            })
                  )


# --- mouse and keyboard input


@typechecked
def get_last_key_pressed_event() -> str:
    """
    This function handles "buffered" keyboard input

    It works as follows: Whenever a key is pressed on the keyboard, it will be recorded and placed in a list sorted by time of pressing.
    This function returns the earliest key-press event that is found in this list, and removes it from the list.
    Hence, keyboard events arrive in the order of being pressed. Events are also recorded while the program is doing
    other things - you do not need to call this function at the time of the key being pressed down for the event
    to be recorded - it will be reported at a later time when the function is called.
    In case no key had been pressed, an empty string is returned.

    Scope/limitations:
     - Currently, only ascii-characters 'a'-'z', 'A'-'Z' and numbers '0'-'9' are reported, all other letters are ignored
     - Special/control keys: only the space bar ' ', return key 'backslash-n' ,  and the cursor keys are reported.
       cursor keys appear as 'cursor_left', 'cursor_right', 'cursor_up', 'cursor_down'
     - A mouse click onto the current image is also recognized and reported as 'left_mouse_button'
       or 'right_mouse_button'.

    :return: a string containing a single character (' ','a'...'z','A',...,'Z','0'...,'9') or
             the string 'backslash-n' (single character) for the return-key
             a code for a cursor key  ('cursor_left', 'cursor_right', 'cursor_up', 'cursor_down')
             or 'left_mouse_button', 'right_mouse_button' for mouse clicks,
             or '' if nothing has happened (empty buffer)
    """
    reply: IOMessage = _try_query_msg(IOMessage('get_last_key_pressed_event', {}))
    if reply.msg_type == 'key_event':
        return reply.params['last_key']
    else:
        return ''


def clear_key_pressed_event_buffer() -> None:
    """
    Clears the buffer of all key press events recorded so far.
    """
    while True:
        key = get_last_key_pressed_event()
        if key == '':
            break


@typechecked
def get_current_keys_down() -> List[str]:
    """
    This function handles "unbuffered" keyboard input.

    It returns a list of all keys that are pressed down at the
    instance in time when this function is being called (more precisely: when the window process receives the request
    from this call).

    Any call to 'get_current_keys_down()' also clears the buffer for the "buffered" input of
    get_last_key_pressed_event()" to avoid chaos / mixing up events.

    Scope/limitations:
     - Currently, only ascii-characters 'a'-'z', 'A'-'Z' and numbers '0'-'9' are reported, all other letters are ignored
     - Special/control keys: only the space bar ' ', return key 'backslash-n', and the cursor keys are reported.
       cursor keys appear as 'cursor_left', 'cursor_right', 'cursor_up', 'cursor_down'
     - A mouse click onto the current image is also recognized and reported as 'left_mouse_button'
       or 'right_mouse_button'.

    :return: A list of pressed keys.
             Each key is encoded as a a string containing a single character (' ','a'...'z','A',...,'Z','0'...,'9') or
             the string 'backslash-n' (single character) for the return-key
             a code for a cursor key  ('cursor_left', 'cursor_right', 'cursor_up', 'cursor_down')
             or 'left_mouse_button', 'right_mouse_button' for mouse clicks.
             If no key is currently pressed, the return value is an empty list ([]).
    """
    reply: IOMessage = _try_query_msg(IOMessage('get_current_keys_down', {}))
    if reply.msg_type == 'key_list':
        return reply.params['keys']
    else:
        return []


@typechecked
def get_current_mouse_position() -> Tuple[int, int]:
    """
    Queries the current mouse position.

    Mouse positions are only recorded while the mouse is residing
    over the currently visible image; afterwards, the last event might remain.
    Clicks on the image (mouse button down) 'capture' the mouse, i.e., even values outside the image boundaries
    are tracked (negative coordinates or coordinates larger than width-1, height-1 are now possible.
    This is useful for interaction with the mouse such as click & draw on images).

    :return: The current mouse position as Tuple of (x,y) with pixel coordinates for x- and y-axis
    """
    reply: IOMessage = _try_query_msg(IOMessage('get_current_mouse_position', {}))
    if reply.msg_type == 'mouse_coords':
        return reply.params['coords']
    else:
        return -1, -1  # if something goes wrong, return this coordinates (this should not happen in practice)


# --- Console/message commands


@typechecked
def print_message(text: str) -> None:
    """
    Prints a message on the message console of the basic_io window (default: lower part of the window),
    not on the active image/main screen!

    This makes sure the message will be visible (useful for diagnostics, debugging, etc.)

    :param text: a string with the message to be printed
    """
    _try_post_msg(IOMessage('print_msg', {'text': text}))


@typechecked
def print_html(text: str) -> None:
    """
    Prints a message on the message console of the basic_io window (default: lower part of the window),
    not on the active image/main screen!

    This makes sure the message will be visible (useful for diagnostics, debugging, etc.)
    The string will be interpreted as HTML code and displayed formatted accordingly.
    Note: The html-output is not very stable (most likely due to QT limitations).
    Use with caution...

    :param text: a string with the message to be printed
    """
    _try_post_msg(IOMessage('print_html', {'text': text}))


@typechecked
def input_string(question: str) -> str:
    """
    This command opens a small edit box and asks for text to be entered. The result is returned as a string.
    Entering is concluded by pressing the Ok-Button (or by pressing return, i.e., results are on-liners).

    :param question: the message in front of the command-prompt
    :result: the string entered (might be empty)
    """
    reply: IOMessage = _try_query_msg(IOMessage('get_input', {'question': question}), no_timeout=True)
    if reply.msg_type == 'input_str':
        return reply.params['reply']
    else:
        return ''


# --- Program termination / closing the window


def wait_close() -> None:
    """
    This command waits until the window is closed.

    This should typically be the last statement in your program.
    """
    __window_process.join()


def close_and_exit() -> None:
    """
    Closes the io window and exits the main process, too (stops the currently running program immediately).
    """
    _try_post_msg(IOMessage('close', {}))
    __window_process.join()
    sys.exit(0)


# additional - nicer colors


# ---------------- internal stuff - do not use from the outside ----------------

# maximum number of commands buffered in the pipe
__MAX_PIPE_LENGTH: int = 100

# communication pipe used to communicate with subwindow
# do not use directly
__connection_to_window = None   # untyped because of compatbility issues win32/py3.10
__connection_from_window = None # untyped because of compatbility issues win32/py3.10
__window_process: Optional[Process] = None
__channel_capacity_sem: Optional[multiprocessing.Semaphore] = None


@typechecked
def _try_post_msg(msg: IOMessage) -> None:
    """
    Tries to send a message to the child process running the window.
    If the window is no longer open (process terminated), the function terminates the current process, too.
    The function only raises exceptions in cases of inconsistent states - this should not happen in practice.
    """
    if __window_process is None:  # make sure the window is open
        __start_window_process()
    if __connection_to_window is None:
        print("error: pipe to window does not exist")
        raise BasicIOError("basic_io.py: The pipe to the window does not exist yet. This should not happen "
                           "(inconsistent initialization).")
    elif __window_process is None:
        print("error: window process does not exist")
        raise BasicIOError("basic_io.py: The python process object of the subwindow does not exist yet. "
                           "This should not happen "
                           "(inconsistent initialization).")
    elif not __window_process.is_alive():
        print("error: window process does not exist anymore (io operation issued after window has been closed)")
        sys.exit(1)
        # raise BasicIOError("basic_io.py: The subprocess displaying the io_window is not running anymore. "
        #                    "This is usually the case if the window has been closed before the main "
        #                    "program has terminated (and it is still trying to perform io).")
    else:
        if __channel_capacity_sem is None:
            print("error: semaphore for pipe capacity is not initialized yet")
            raise BasicIOError("basic_io.py: The semaphore for limiting pipe capacity is not initialized yet. "
                               "This should not happen "
                               "(inconsistent initialization).")
        # limit number of items in queue at a time
        can_post: bool = False
        while not can_post:
            can_post = __channel_capacity_sem.acquire(block=True, timeout=0.1)
            if not __window_process.is_alive():
                print("error: window process does not exist anymore (io operation issued after window has been closed)")
                sys.exit(1)
        # once there is space, send stuff
        __connection_to_window.send(msg)


@typechecked
def _try_query_msg(msg: IOMessage, no_timeout: bool = False) -> IOMessage:
    """
    Tries to send a message to the child process running the window and waits for a reply (synchronously).
    If the window is no longer open (process terminated), the function terminates the current process, too.
    """
    if __window_process is None:  # make sure the window is open
        __start_window_process()
    _try_post_msg(msg)
    if __connection_from_window is None:
        print("error: pipe back from window does not exist")
        raise BasicIOError("basic_io.py: The pipe back from the  window does not exist yet. This should not happen "
                           "(inconsistent initialization).")

    if no_timeout:
        data_received: bool = False
        while not data_received:
            data_received = __connection_from_window.poll()
            if data_received:
                msg = __connection_from_window.recv()
                return msg
    else:
        # check if answer comes in time, 5sec time-out
        got_data: bool = __connection_from_window.poll(5)
        if got_data:
            msg = __connection_from_window.recv()
            return msg
        else:
            print("IOWindow did not answer to message request within 5 seconds. Terminating program.")
            sys.exit(1)


@typechecked
def __window_process_loop(connection_client_to_window, connection_window_to_client,
                          channel_capacity_sem: multiprocessing.Semaphore) -> None:
    """
    This function runs the child process that handles the window asynchronously.
    Do not call from the outside
    """
    app = QApplication(sys.argv)
    win = IOWindow(parent=None,
                   connection_client_to_window=connection_client_to_window,
                   connection_window_to_client=connection_window_to_client,
                   channel_capacity_sem=channel_capacity_sem)

    desktop_rec: QRect = QApplication.desktop().screenGeometry()
    desktop_height: int = desktop_rec.height()
    desktop_width: int = desktop_rec.width()
    win.move(desktop_width//8, desktop_height//8)
    win.resize(desktop_width//8*6, desktop_height//8*6)

    # def __exit_handler_window_proc() -> None:
    #     """
    #     This function closes the window upon termination of the process.
    #     (private function, not to be called from the outside)
    #     """
    #     print('program shuts down - closing console window')
    #     if win is not None:
    #         win.close()

    # start the main loop
    win.show()
    # atexit.register(__exit_handler_window_proc)
    app.exec()


def __start_window_process() -> None:
    """
    starts the child process that is running the client window
    """
    global __connection_to_window
    global __connection_from_window
    global __channel_capacity_sem
    global __window_process
    main_to_win_main_end, main_to_win_win_end = Pipe()
    win_to_main_win_end, win_to_main_main_end = Pipe()
    __channel_capacity_sem = multiprocessing.Semaphore(__MAX_PIPE_LENGTH)
    __connection_to_window = main_to_win_main_end
    __connection_from_window = win_to_main_main_end
    # Window process
    __window_process = Process(target=__window_process_loop, name="basicio_windowproc",
                               args=(main_to_win_win_end, win_to_main_win_end, __channel_capacity_sem,))
    __window_process.start()


__all__ = ['start', 'draw_line', 'draw_circle', 'draw_ellipse', 'draw_rectangle',
           'draw_polygon', 'draw_text', 'draw_pixel',
           'read_pixel', 'load_image', 'draw_image', 'draw_object', 'clear_image', 'set_active_image',
           'set_visible_image', 'copy_image', 'resize_image', 'get_last_key_pressed_event',
           'clear_key_pressed_event_buffer', 'get_current_keys_down', 'get_current_mouse_position', 'print_message',
           'print_html', 'input_string', 'wait_close', 'close_and_exit']
