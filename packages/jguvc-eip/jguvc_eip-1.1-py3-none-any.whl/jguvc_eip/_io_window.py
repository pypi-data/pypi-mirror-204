"""
This file defines the QT Window that displays text, graphics, etc.

Do not use directly from the outside - you should only import basic_io.py
and use the functional interface defined therein.
"""

import multiprocessing
from typing import List, Optional, Deque, Dict
from multiprocessing.connection import Connection
import threading
from collections import deque
import sys


from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QColor, QPixmap, QPainter, QPen, QFont, QFontDatabase, QFontMetrics, QKeyEvent, \
    QMouseEvent, QTextCursor, QPolygon, QTransform, qRed, qGreen, qBlue
from PyQt5.QtWidgets import QMainWindow, QWidget, QLabel, QFrame

from ._BasicIOWindowUI import Ui_BasicIOWindowUI
from .image_objects import ImageObject
from ._io_messages import IOMessage
from .colors import RGBColor


# configuration: global constants (avoiding 'Final' type annotation for maximum compatibility)
DEFAULT_WIDTH: int = 640
DEFAULT_HEIGHT: int = 480


class IOWindow(QMainWindow, Ui_BasicIOWindowUI):

    def __init__(self, parent: Optional[QWidget],
                 connection_client_to_window,
                 connection_window_to_client,
                 channel_capacity_sem: multiprocessing.Semaphore):
        super().__init__(parent)
        # untyped because of compatibility issues win32/py3.10
        self.connection_client_to_window = connection_client_to_window
        self.connection_window_to_client = connection_window_to_client

        self.channel_capacity_sem: multiprocessing.Semaphore = channel_capacity_sem
        self.shared_data_lock: threading.Lock = threading.Lock()
        self.unprocessed_msgs: Deque[IOMessage] = deque()
        self.keyboard_events: Deque[str] = deque()
        self.keys_down: Dict[str] = {}
        self.loaded_images: List[QImage] = []

        self.setupUi(self)

        self.timer: QTimer = QTimer(self)
        self.timer.setInterval(16)  # 16msec ~~ 60Hz
        self.timer.setSingleShot(False)
        self.images: List[Optional[QImage]] = [None] * 10
        self.changed_images: List[bool] = [True] * 10
        self.images[0] = self._create_image()
        self.visible_image: int = 0
        self.active_image: int = 0
        self.status_time = 60
        self.status_label1: QLabel = QLabel('starting')
        self.status_label1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.status_label1.setContentsMargins(6, 3, 6, 3)
        self.status_label1.setMinimumWidth(200)
        self.statusbar.addWidget(self.status_label1)

        self.timer.timeout.connect(self._timer_triggered)
        self.timer.start()
        self.action_100.toggled.connect(self._invalidate_event)
        self.action_200.toggled.connect(self._invalidate_event)
        self.action_300.toggled.connect(self._invalidate_event)
        self.action_400.toggled.connect(self._invalidate_event)

        self.input_frame.setVisible(False)
        self.input_frame.setEnabled(False)

        self.btn_input_ok.clicked.connect(self._btn_input_ok_clicked)
        self.edit_input.returnPressed.connect(self._btn_input_ok_clicked)

        self.paint_thread = threading.Thread(target=self.__paint_thread_func, daemon=True)
        self.paint_thread.start()

    def __paint_thread_func(self):
        while True:
            # check if parent process is still running
            data_available = self.connection_client_to_window.poll(1)
            if sys.version_info.minor >= 8:  # parent_process is not available in python before 3.8.x
                if not multiprocessing.parent_process().is_alive():
                    break
            if not data_available:
                continue

            obj = self.connection_client_to_window.recv()
            self.channel_capacity_sem.release()

            self.shared_data_lock.acquire()
            if isinstance(obj, IOMessage):
                if obj.msg_type == 'close' \
                        or obj.msg_type == 'print_html' \
                        or obj.msg_type == 'print_msg' \
                        or obj.msg_type == 'print_warning' \
                        or obj.msg_type == 'print_error':
                    self.unprocessed_msgs.append(obj)
                elif obj.msg_type == 'set_active_image':
                    self.set_active_image(obj.params['buffer'])
                elif obj.msg_type == 'set_visible_image':
                    self.set_visible_image(obj.params['buffer'])
                elif obj.msg_type == 'draw_ellipse':
                    self.do_draw_ellipse(obj)
                elif obj.msg_type == 'draw_text':
                    self.do_draw_text(obj)
                elif obj.msg_type == 'draw_rectangle':
                    self.do_draw_rectangle(obj)
                elif obj.msg_type == 'draw_line':
                    self.do_draw_line(obj)
                elif obj.msg_type == 'draw_polygon':
                    self.do_draw_polygon(obj)
                elif obj.msg_type == 'get_last_key_pressed_event':
                    self.do_get_last_key_event()
                elif obj.msg_type == 'get_current_keys_down':
                    self.do_get_current_keys_down()
                elif obj.msg_type == 'get_current_mouse_position':
                    self.do_get_current_mouse_position()
                elif obj.msg_type == 'copy_image':
                    self.do_copy_image(obj)
                elif obj.msg_type == 'resize_image':
                    self.images[self.active_image] = QImage(obj.params['width'], obj.params['height'],
                                                            QImage.Format_RGB32)
                    col = obj.params['color']
                    self.images[self.active_image].fill(QColor(col[0], col[1], col[2]))
                elif obj.msg_type == 'draw_image_object':
                    self.do_draw_object(obj)
                elif obj.msg_type == 'draw_pixel':
                    self.do_draw_pixel(obj)
                elif obj.msg_type == 'read_pixel':
                    self.do_read_pixel(obj)
                elif obj.msg_type == 'get_input':
                    self.unprocessed_msgs.append(obj)
                elif obj.msg_type == 'load_image':
                    self.do_load_image(obj)
                elif obj.msg_type == 'draw_image':
                    self.do_draw_image(obj)
                else:
                    self.unprocessed_msgs.append(IOMessage('print_warning',
                                                           {'text': ('unknown message type: ' + obj.msg_type)}))
            else:
                self.unprocessed_msgs.append(IOMessage('print_error',
                                                       {'text': "IOWindow._timer_triggered() received an object "
                                                                "of wrong type through the connection_to_client "
                                                                "- this should never happen (internal inconsistency)"}))
            self.shared_data_lock.release()

    def do_copy_image(self, obj: IOMessage):
        from_buffer = obj.params['from_buffer']
        to_buffer = obj.params['to_buffer']
        if to_buffer != from_buffer:
            self.images[to_buffer] = QImage(self.images[from_buffer])

    def do_get_current_mouse_position(self):
        scale: int = self.get_scale()
        x_lb: int = self.label_img.mouse_x - self.label_img.pos().x()
        y_lb: int = self.label_img.mouse_y - self.label_img.pos().y()
        x_im: int = x_lb - (self.label_img.width() - self.get_active_image().width()*scale) // 2
        y_im: int = y_lb - (self.label_img.height() - self.get_active_image().height()*scale) // 2

        reply: IOMessage = IOMessage('mouse_coords', {'coords': (x_im // scale, y_im // scale)})

        self.connection_window_to_client.send(reply)

    def do_get_last_key_event(self):
        result: str = ''
        if len(self.keyboard_events) > 0:
            result = self.keyboard_events.popleft()
        reply: IOMessage = IOMessage('key_event', {'last_key': result})
        self.connection_window_to_client.send(reply)

    def do_get_current_keys_down(self):
        reply: IOMessage = IOMessage('key_list', {'keys': list(self.keys_down.keys())})
        self.connection_window_to_client.send(reply)

    def do_draw_text(self, obj):
        img = self.get_active_image()
        x: int = obj.params['x']
        y: int = obj.params['y']
        text: str = obj.params['text']
        color: RGBColor = obj.params['color']
        background_color: Optional[RGBColor] = obj.params['background_color']
        font_height: int = obj.params['font_height']
        painter: QPainter = QPainter()
        painter.begin(img)

        fixed_font: QFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        fixed_font.setPixelSize(font_height)
        metrics: QFontMetrics = QFontMetrics(fixed_font)
        offset: int = metrics.ascent()  # vertical distance to baseline - for placement in y-direction
        painter.setFont(fixed_font)

        if background_color is not None:
            width = metrics.width(text)
            height = metrics.height()
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(background_color[0], background_color[1], background_color[2]))
            painter.drawRect(x, y, width, height)

        pen: QPen = QPen(QColor(color[0], color[1], color[2]))
        painter.setPen(pen)
        painter.drawText(x, y + offset, text)
        painter.end()
        self.changed_images[self.active_image] = True

    @staticmethod
    def setup_colors(obj, painter):
        foreground_col: RGBColor = obj.params['fill_color']
        background_col: RGBColor = obj.params['border_color']
        brad: int = obj.params['border_thickness']
        if background_col is not None and brad > 0:
            pen = QPen(QColor(background_col[0], background_col[1], background_col[2]))
            pen.setWidth(brad)
        else:
            pen = Qt.NoPen
        painter.setPen(pen)
        if foreground_col is not None:
            painter.setBrush(QColor(foreground_col[0], foreground_col[1], foreground_col[2]))
        else:
            painter.setBrush(Qt.NoBrush)

    def do_draw_ellipse(self, obj):
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        self.setup_colors(obj, painter)
        x: int = obj.params['x']
        y: int = obj.params['y']
        radius_x: int = obj.params['radius_x']
        radius_y: int = obj.params['radius_y']
        painter.drawEllipse(x - radius_x // 2, y - radius_y // 2, radius_x, radius_y)
        painter.end()
        self.changed_images[self.active_image] = True

    def do_draw_rectangle(self, obj):
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        self.setup_colors(obj, painter)
        x: int = obj.params['x']
        y: int = obj.params['y']
        width: int = obj.params['width']
        height: int = obj.params['height']
        painter.drawRect(x, y, width, height)
        painter.end()
        self.changed_images[self.active_image] = True

    def do_draw_polygon(self, obj):
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        self.setup_colors(obj, painter)
        poly = obj.params['points']
        n_pts: int = len(poly)
        q_poly: QPolygon = QPolygon(n_pts)
        for i in range(n_pts):
            q_poly.setPoint(i, poly[i][0], poly[i][1])
        painter.drawPolygon(q_poly)
        painter.end()
        self.changed_images[self.active_image] = True

    def do_draw_line(self, obj):
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        color: RGBColor = obj.params['color']
        thickness: int = obj.params['thickness']
        pen = QPen(QColor(color[0], color[1], color[2]))
        pen.setWidth(thickness)
        painter.setPen(pen)
        start_x: int = obj.params['start_x']
        start_y: int = obj.params['start_y']
        end_x: int = obj.params['end_x']
        end_y: int = obj.params['end_y']

        painter.drawLine(start_x, start_y, end_x, end_y)
        painter.end()
        self.changed_images[self.active_image] = True

    def do_draw_pixel(self, obj):
        img = self.get_active_image()
        col = obj.params['color']
        x, y = obj.params['x'], obj.params['y']
        if 0 <= x < img.width() and 0 <= y < img.height():
            img.setPixel(x, y, QColor(col[0], col[1], col[2]).rgb())
            self.changed_images[self.active_image] = True

    def do_read_pixel(self, obj):
        img = self.get_active_image()
        x, y = obj.params['x'], obj.params['y']
        col: RGBColor = (-1, -1, -1)
        if 0 <= x < img.width() and 0 <= y < img.height():
            rgb: int = img.pixel(x, y)
            col = (qRed(rgb), qGreen(rgb), qBlue(rgb))
        reply: IOMessage = IOMessage('pixel_color', {'color': col})
        self.connection_window_to_client.send(reply)

    def do_load_image(self, obj):
        filename: str = obj.params['filename']
        new_img = QImage(filename)
        if new_img.width() <= 0 or new_img.height() <= 0:
            result: int = -1
        else:
            result = len(self.loaded_images)
            self.loaded_images.append(new_img)
        reply: IOMessage = IOMessage('image_loaded', {'index': result})
        self.connection_window_to_client.send(reply)

    def do_draw_image(self, obj):
        x: int = obj.params['x']
        y: int = obj.params['y']
        index: int = obj.params['index']
        if index < 0 or index >= len(self.loaded_images):
            return
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        painter.drawImage(x, y, self.loaded_images[index])
        painter.end()
        self.changed_images[self.active_image] = True

    def do_draw_object(self, obj):
        img = self.get_active_image()
        painter: QPainter = QPainter()
        painter.begin(img)
        transform: QTransform = QTransform()
        transform.translate(obj.params['x'], obj.params['y'])
        painter.setTransform(transform)
        img_obj: ImageObject = obj.params['obj']
        img_obj.draw(painter)
        painter.end()
        self.changed_images[self.active_image] = True

    def _invalidate_event(self):
        self.shared_data_lock.acquire()
        self.changed_images = [True] * 10
        self.shared_data_lock.release()

    def _btn_input_ok_clicked(self):
        reply: IOMessage = IOMessage('input_str', {'reply': self.edit_input.text()})
        self.edit_input.setText('')
        self.input_frame.setEnabled(False)
        self.input_frame.setVisible(False)
        self.connection_window_to_client.send(reply)

    @staticmethod
    def _create_image() -> QImage:
        result: QImage = QImage(DEFAULT_WIDTH, DEFAULT_HEIGHT, QImage.Format_RGB32)
        result.fill(QColor(255, 255, 255))
        return result

    def _timer_triggered(self) -> None:
        self.shared_data_lock.acquire()
        # update graphics
        if self.changed_images[self.visible_image]:
            if self.images[self.visible_image] is not None:
                pixmap: QPixmap = QPixmap()
                pixmap.convertFromImage(self.images[self.visible_image])

                scale: int = self.get_scale()

                pixmap = pixmap.scaled(pixmap.width()*scale, pixmap.height()*scale)
                self.label_img.setPixmap(pixmap)
                self.changed_images[self.visible_image] = False
                self.status_label1.setText('refreshed (image '+str(self.visible_image)+')')
                self.status_time = 60
        else:
            self.status_time -= 1
            if self.status_time == 0:
                self.status_label1.setText('image ' + str(self.visible_image))
            if self.status_time < 0:
                self.status_time = -1

        # check mail
        while len(self.unprocessed_msgs) > 0:
            obj = self.unprocessed_msgs.popleft()
            if isinstance(obj, IOMessage):
                if obj.msg_type == 'close':
                    self.close()
                elif obj.msg_type == 'print_msg':
                    self.print_message(obj.params['text'])
                elif obj.msg_type == 'print_warning':
                    self.print_warning(obj.params['text'])
                elif obj.msg_type == 'print_error':
                    self.print_error(obj.params['text'])
                elif obj.msg_type == 'print_html':
                    self.print_html(obj.params['text'])
                elif obj.msg_type == 'get_input':
                    self.input_frame.setVisible(True)
                    self.input_frame.setEnabled(True)
                    self.edit_input.setText('')
                    self.label_question.setText(obj.params['question'])
                    self.edit_input.setFocus()
                else:
                    self.print_warning('unknown unprocessed message type: ' + obj.msg_type)

        self.shared_data_lock.release()

    def get_scale(self) -> int:
        scale: int = 1
        if self.action_200.isChecked():
            scale = 2
        if self.action_300.isChecked():
            scale = 3
        if self.action_400.isChecked():
            scale = 4
        return scale

    @staticmethod
    def translate_key(ev: QKeyEvent) -> str:
        key: int = ev.key()
        if key == Qt.Key_Return:
            return '\n'
        elif key == Qt.Key_Left:
            return 'cursor_left'
        elif key == Qt.Key_Right:
            return 'cursor_right'
        elif key == Qt.Key_Up:
            return 'cursor_up'
        elif key == Qt.Key_Down:
            return 'cursor_down'
        elif key == Qt.Key_Space:
            return ' '
        elif Qt.Key_A <= key <= Qt.Key_Z:
            if ev.modifiers() == Qt.ShiftModifier:
                return chr(key - Qt.Key_A + ord('A'))
            else:
                return chr(key - Qt.Key_A + ord('a'))
        elif Qt.Key_0 <= key <= Qt.Key_9:
            return chr(key - Qt.Key_0 + ord('0'))
        else:
            return ''

    def keyPressEvent(self, ev: QKeyEvent) -> None:
        super().keyPressEvent(ev)
        if ev.isAccepted():
            return
        key_str: str = self.translate_key(ev)
        self.shared_data_lock.acquire()
        self.keyboard_events.append(key_str)
        self.keys_down[key_str] = 1
        self.shared_data_lock.release()
        ev.setAccepted(True)

    def keyReleaseEvent(self, ev: QKeyEvent) -> None:
        super().keyReleaseEvent(ev)
        if ev.isAccepted():
            return
        key_str: str = self.translate_key(ev)
        self.shared_data_lock.acquire()
        if key_str in self.keys_down:
            del self.keys_down[key_str]
        self.shared_data_lock.release()
        ev.setAccepted(True)

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        super().mousePressEvent(ev)
        if ev.isAccepted():
            return
        key_str: str = ''
        if ev.button() & Qt.LeftButton != 0:
            key_str = 'left_mouse_button'
        elif ev.button() & Qt.RightButton != 0:
            key_str: str = 'right_mouse_button'
        if key_str != '':
            self.keyboard_events.append(key_str)
            self.keys_down[key_str] = 1
        ev.setAccepted(True)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        super().mouseReleaseEvent(ev)
        if ev.isAccepted():
            return
        key_str: str = ''
        if ev.button() & Qt.LeftButton != 0:
            key_str = 'left_mouse_button'
        elif ev.button() & Qt.RightButton != 0:
            key_str: str = 'right_mouse_button'
        if key_str != '':
            if key_str in self.keys_down:
                del self.keys_down[key_str]
        ev.setAccepted(True)

    def get_active_image(self) -> Optional[QImage]:
        return self.images[self.active_image]

    def set_active_image(self, buffer: int) -> None:
        if buffer < 0 or buffer > 9:
            return
        if self.images[buffer] is None:
            self.images[buffer] = self._create_image()
        self.active_image = buffer

    def set_visible_image(self, buffer: int) -> None:
        if buffer < 0 or buffer > 9:
            return
        if self.images[buffer] is None:
            self.images[buffer] = self._create_image()
        self.visible_image = buffer

    def print_html(self, text: str):
        self.messages.moveCursor(QTextCursor.End)
        self.messages.insertHtml(text)

    def print_message(self, text: str):
        self.messages.moveCursor(QTextCursor.End)
        self.messages.insertPlainText(text)
        self.messages.insertPlainText('\n')

    def print_warning(self, text: str):
        self.messages.moveCursor(QTextCursor.End)
        self.messages.setTextColor(QColor(150, 130, 0))
        self.messages.setFontWeight(QFont.Bold)
        self.messages.insertPlainText("warning: ")
        self.messages.setTextColor(QColor(0, 0, 0))
        self.messages.setFontWeight(QFont.Normal)
        self.messages.insertPlainText(text)
        self.messages.insertPlainText('\n')

    def print_error(self, text: str):
        self.messages.moveCursor(QTextCursor.End)
        self.messages.setTextColor(QColor(192, 0, 0))
        self.messages.setFontWeight(QFont.Bold)
        self.messages.insertPlainText("error: ")
        self.messages.setTextColor(QColor(0, 0, 0))
        self.messages.setFontWeight(QFont.Normal)
        self.messages.insertPlainText(text)
        self.messages.insertPlainText('\n')


__all__ = []