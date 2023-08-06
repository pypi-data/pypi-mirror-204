from abc import ABC, abstractmethod
from typing import Optional, Tuple, List
from typeguard import typechecked

from .basic_io_error import BasicIOError
from .colors import RGBColor, BLACK

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QColor, QPolygon, QFont, QFontDatabase, QFontMetrics, QTransform, QImage
from PyQt5.QtWidgets import QApplication


class ImageObject(ABC):
    @abstractmethod
    def get_width(self) -> int:
        """
        returns the width of the object in pixel
        :return: width in pixel
        """
        pass

    @abstractmethod
    def get_height(self) -> int:
        """
        returns the height of the object in pixel
        :return: height in pixel
        """
        pass

    @abstractmethod
    def draw(self, painter: QPainter) -> None:
        """
        Draws the object on a "QT Painter" (a device one can draw on such as an image or window)
        Do not use this function from the outside; it is only relevant when defining new image objects.
        :param painter: the target of the drawing operation
        """
        pass

    @staticmethod
    def _setup_colors(fill_color: Optional[RGBColor], border_color: Optional[RGBColor],
                      border_thickness: int, painter: QPainter) -> None:
        """
        Helper method to aid with drawing. Do not use externally
        :param fill_color: fill color to be set. can be None for no fill
        :param border_color: border color to be set. can be None for no fill
        :param border_thickness: size of border in pixel
        :param painter: the paint device to be setup
        """
        if border_color is not None and border_thickness > 0:
            pen = QPen(QColor(border_color[0], border_color[1], border_color[2]))
            pen.setWidth(border_thickness)
        else:
            pen = Qt.NoPen
        painter.setPen(pen)
        if fill_color is not None:
            painter.setBrush(QColor(fill_color[0], fill_color[1], fill_color[2]))
        else:
            painter.setBrush(Qt.NoBrush)


class Rectangle(ImageObject):
    """
    This class represents/draws a rectangle with specified width and height.
    The shape is drawn within a bounding box of [0,width] x [0,height].
    """
    @typechecked
    def __init__(self, width: int, height: int,
                 fill_color: Optional[RGBColor] = BLACK,
                 border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1):
        """
        Create a rectangle object.
        :param width: width of the rectangle
        :param height: height of the rectangle
        :param fill_color: color to fill the interior with
        :param border_color: color of the border
        :param border_thickness: thickness of the border
        """
        self.width: int = width
        self.height: int = height
        self.fill_color: Optional[RGBColor] = fill_color
        self.border_color: Optional[RGBColor] = border_color
        self.border_thickness: int = border_thickness

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        self._setup_colors(self.fill_color, self.border_color, self.border_thickness, painter)
        painter.drawRect(0, 0, self.width, self.height)


class Circle(ImageObject):
    """
    This class represents/draws a circle with specified radius
    The shape is drawn within a bounding box of [0,2*radius] x [0,2*radius].
    """
    @typechecked
    def __init__(self, radius: int,
                 fill_color: Optional[RGBColor] = BLACK,
                 border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1):
        """
        Create a circle object.
        :param radius: radius of the circle (the overall object is two times as large)
        :param fill_color: color to fill the interior with
        :param border_color: color of the border
        :param border_thickness: thickness of the border
        """
        self.radius: int = radius
        self.fill_color: Optional[RGBColor] = fill_color
        self.border_color: Optional[RGBColor] = border_color
        self.border_thickness: int = border_thickness

    @typechecked
    def get_width(self) -> int:
        return self.radius*2

    @typechecked
    def get_height(self) -> int:
        return self.radius*2

    @typechecked
    def draw(self, painter: QPainter) -> None:
        self._setup_colors(self.fill_color, self.border_color, self.border_thickness, painter)
        painter.drawEllipse(0, 0, self.radius, self.radius)


class Ellipse(ImageObject):
    """
    This class represents/draws an ellipse with axis-aligned diameters "width" and "height"
    The shape is drawn within a bounding box of [0,width] x [0,height].
    """
    @typechecked
    def __init__(self, width: int, height: int,
                 fill_color: Optional[RGBColor] = BLACK,
                 border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1):
        """
        Create an ellipse object
        :param width: width of the ellipse (diameter along x-axis)
        :param height: height of the ellipse (diameter along y-axis)
        :param fill_color: color to fill the interior with
        :param border_color: color of the border
        :param border_thickness: thickness of the border
        """
        self.width: int = width
        self.height: int = height
        self.fill_color: Optional[RGBColor] = fill_color
        self.border_color: Optional[RGBColor] = border_color
        self.border_thickness: int = border_thickness

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        self._setup_colors(self.fill_color, self.border_color, self.border_thickness, painter)
        painter.drawEllipse(0, 0, self.width, self.height)


class Polygon(ImageObject):
    """
    This class represents/draws a polygon consisting of a list of points.
    The polygon will be drawn "as is"; the width/height are the maximum x/y coordinates.
    The minimum x/y coordinates should be zero and never be negative (however, this is not checked).
    Container objects will use the bounding box [0, max_x] x [0, max_y] to frame the object.
    """
    @typechecked
    def __init__(self, points: List[Tuple[int, int]],
                 fill_color: Optional[RGBColor] = BLACK,
                 border_color: Optional[RGBColor] = BLACK,
                 border_thickness: int = 1):
        """
        Create a polygon object
        :param points: a list of tuples of integers representing the coordinates of the vertices of the polygon
        :param fill_color: color to fill the interior with
        :param border_color: color of the border
        :param border_thickness: thickness of the border
        """
        self.points: List[Tuple[int, int]] = points
        if len(points) < 1:
            raise BasicIOError('Polygons must contain at least one point.')
        self.max_x = points[0][0]
        self.min_x = points[0][0]
        self.max_y = points[0][1]
        self.min_y = points[0][1]
        for p in points:
            if p[0] < self.min_x:
                self.min_x = p[0]
            if p[0] > self.max_x:
                self.max_x = p[0]
            if p[1] < self.min_y:
                self.min_x = p[1]
            if p[1] > self.max_y:
                self.max_x = p[1]
        self.fill_color: Optional[RGBColor] = fill_color
        self.border_color: Optional[RGBColor] = border_color
        self.border_thickness: int = border_thickness

    @typechecked
    def get_width(self) -> int:
        return self.max_x

    @typechecked
    def get_height(self) -> int:
        return self.max_y

    @typechecked
    def draw(self, painter: QPainter) -> None:
        self._setup_colors(self.fill_color, self.border_color, self.border_thickness, painter)
        n_pts: int = len(self.points)
        q_poly: QPolygon = QPolygon(n_pts)
        for i in range(n_pts):
            q_poly.setPoint(i, self.points[i][0], self.points[i][1])
        painter.drawPolygon(q_poly)


__qt_app_dummy: Optional[QApplication] = None


def _make_sure_we_have_a_qt_app() -> None:
    """
    Helper function -- computing font sizes requires an application object to be initialized.
    This is done on demand (when using text image objects).
    """
    global __qt_app_dummy
    if __qt_app_dummy is None:
        __qt_app_dummy = QApplication([])


class Text(ImageObject):
    """
    This class represents/draws text specified by a string.
    The text can be drawn in different colors and an optional background color
    (rectangle that fills the space behind the text).
    One can choose two font styles (fixed width [default] and proportional),
    as well as bold and italic text.
    """

    @typechecked
    def __init__(self, text: str,
                 color: RGBColor = BLACK,
                 background_color: Optional[RGBColor] = None,
                 font_height: int = 16,
                 bold: bool = False, italic: bool = False, fixed_width: bool = True):
        """
        Create a text object
        :param text: the string to be printed
        :param color: the color of the text (foreground). The color must be point to a valid object
                      (defaults to black) - it is not possible to set it to "None" (unlike most other color options).
        :param background_color: the color of the background. No background is drawn if the parameter is None.
        :param font_height: Height of the font ("font metric"; this corresponds approx. to pixels)
        :param bold: if true, the text is shown in bold
        :param italic: if true, the text is shown in italic
        :param fixed_width: if true, a fixed-width font is used (all characters have the same size)
                            otherwise, the default system font is used, which typically is "proportional"
                            (i.e., the character "i" or "l" is not as wide as "m" or "W")
        """
        self.text: str = text
        self.color: RGBColor = color
        self.background_color: Optional[RGBColor] = background_color
        self.bold: bool = bold
        self.italic: bool = italic
        self.font_height = font_height
        self.fixed_width: bool = fixed_width
        forget_img = QImage(8, 8, QImage.Format_RGB32)
        painter: QPainter = QPainter()
        painter.begin(forget_img)
        _make_sure_we_have_a_qt_app()
        if fixed_width:
            font: QFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        else:
            font = QFontDatabase.systemFont(QFontDatabase.GeneralFont)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setPixelSize(font_height)
        painter.setFont(font)
        metrics: QFontMetrics = QFontMetrics(font)
        self.width: int = metrics.boundingRect(text).width()
        self.height: int = metrics.height()
        painter.end()

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        if self.fixed_width:
            font: QFont = QFontDatabase.systemFont(QFontDatabase.FixedFont)
        else:
            font = QFontDatabase.systemFont(QFontDatabase.GeneralFont)
        font.setBold(self.bold)
        font.setItalic(self.italic)
        font.setPixelSize(self.font_height)
        metrics: QFontMetrics = QFontMetrics(font)
        offset: int = metrics.ascent()  # vertical distance to baseline - for placement in y-direction
        painter.setFont(font)
        if self.background_color is not None:
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(self.background_color[0], self.background_color[1], self.background_color[2]))
            painter.drawRect(0, 0, self.width, self.height)

        pen: QPen = QPen(QColor(self.color[0], self.color[1], self.color[2]))
        painter.setPen(pen)
        painter.drawText(0, offset, self.text)


class VerticalStack(ImageObject):
    """
    This class stores a list of image objects that are stacked vertically on top of each other
    when being drawn. The first object in the list is the top-most (smallest y-coordinate).
    An optional margin parameter leaves a bit of room around the objects (on all sides).
    """
    @typechecked
    def __init__(self, objects: List[ImageObject], margin: int = 0):
        """
        Creates a vertical stack of objects.
        :param objects: a list of objects to be drawn. Can be empty (although that does not do much; empty stacks
                        will have size zero in all directions)
        :param margin: an optional margin added to each object in all directions (left/right/top/bottom).
                       The size of the overall stack increases by len(objects)*2*margin in y-direction,
                       and by 2*margin in x-direction
        """
        self.objects: List[ImageObject] = objects
        self.margin: int = margin

        self.width: int = 0
        for obj in self.objects:
            width_obj = obj.get_width()
            if width_obj > self.width:
                self.width = width_obj
        if len(objects) > 0:
            self.width += 2*self.margin

        self.height: int = 0
        for obj in self.objects:
            self.height += obj.get_height()
            self.height += 2*self.margin

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        old_transform: QTransform = painter.transform()
        y: int = self.margin
        for obj in self.objects:
            x: int = self.margin
            x += (self.width-obj.get_width()) // 2
            transform: QTransform = QTransform()
            transform.translate(x, y)
            painter.setTransform(old_transform, combine=False)
            painter.setTransform(transform, combine=True)
            obj.draw(painter)
            y += obj.get_height()
            y += 2*self.margin
            painter.setTransform(old_transform, combine=False)


class HorizontalStack(ImageObject):
    """
    This class stores a list of image objects that are stacked horizontally next to each other
    when being drawn. The first object in the list is the left-most (smallest x-coordinate).
    An optional margin parameter leaves a bit of room around the objects (on all sides).
    """
    @typechecked
    def __init__(self, objects: List[ImageObject], margin: int = 0):
        """
        Creates a vertical stack of objects.
        :param objects: a list of objects to be drawn. Can be empty (although that does not do much; empty stacks
                        will have size zero in all directions)
        :param margin: an optional margin added to each object in all directions (left/right/top/bottom).
                       The size of the overall stack increases by len(objects)*2*margin in x-direction,
                       and by 2*margin in y-direction
        """
        self.objects: List[ImageObject] = objects
        self.margin: int = margin

        self.width: int = 0
        for obj in self.objects:
            self.width += obj.get_width()
            self.width += 2*self.margin

        self.height: int = 0
        for obj in self.objects:
            height_obj = obj.get_height()
            if height_obj > self.height:
                self.height = height_obj
        if len(objects) > 0:
            self.height += 2*self.margin

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        old_transform: QTransform = painter.transform()
        x: int = self.margin
        for obj in self.objects:
            y: int = self.margin
            y += (self.height-obj.get_height()) // 2
            y = 0
            transform: QTransform = QTransform()
            transform.translate(x, y)
            painter.setTransform(old_transform, combine=False)
            painter.setTransform(transform, combine=True)
            obj.draw(painter)
            x += obj.get_width()
            x += 2*self.margin
            painter.setTransform(old_transform, combine=False)


class Overlay(ImageObject):
    """
    This class stores a list of image objects drawn over each other. The first object in the list is drawn
    first, i.e., it will appear as the back-most.
    """
    @typechecked
    def __init__(self, objects: List[ImageObject]):
        """
        Creates an overlay of objects. The bounding box of the overlay will be set to fit the largest x- and
        y-extends of the contained objects.
        :param objects: a list of objects to be drawn. Can be empty (although that does not do much; empty overlays
                        will have size zero in all directions)
        """
        self.objects: List[ImageObject] = objects
        self.width: int = 0
        self.height: int = 0
        for obj in self.objects:
            width_obj = obj.get_width()
            if width_obj > self.width:
                self.width = width_obj
            height_obj = obj.get_height()
            if height_obj > self.height:
                self.height = height_obj

    @typechecked
    def get_width(self) -> int:
        return self.width

    @typechecked
    def get_height(self) -> int:
        return self.height

    @typechecked
    def draw(self, painter: QPainter) -> None:
        for obj in self.objects:
            obj.draw(painter)


class Translate(ImageObject):
    """
    This class is a container that translates (shifts in space) the position of the contained object.
    It adds the specified offset in x- and y-direction to all coordinates.
    """
    @typechecked
    def __init__(self, obj: ImageObject, offset_x: int, offset_y: int):
        """
        Creates a translation container object that shifts the contained coordinates in space (adds an offset)
        :param obj: the contained object (to be shifted)
        :param offset_x: shift in x-direction
        :param offset_y: shift in y-direction
        """
        self.obj: ImageObject = obj
        self.offset_x = offset_x
        self.offset_y = offset_y

    @typechecked
    def get_width(self) -> int:
        if self.offset_x > 0:
            return self.obj.get_width() + self.offset_x
        else:
            return self.obj.get_width()

    @typechecked
    def get_height(self) -> int:
        if self.offset_y > 0:
            return self.obj.get_height() + self.offset_y
        else:
            return self.obj.get_height()

    @typechecked
    def draw(self, painter: QPainter) -> None:
        old_transform: QTransform = painter.transform()
        transform: QTransform = QTransform()
        transform.translate(self.offset_x, self.offset_y)
        painter.setTransform(transform, combine=True)
        self.obj.draw(painter)
        painter.setTransform(old_transform, combine=False)


class Scale(ImageObject):
    """
    This class is a container that scales the contained object (changes its size by a factor) 
    It multiplies the specified scale factor with all coordinates.
    """
    @typechecked
    def __init__(self, obj: ImageObject, scale: float):
        """
        Creates a scaling container object that scales the contained coordinates (multiplies by a factor)
        :param obj: the contained object (to be scaled)
        :param scale: the scale factor.
        """
        self.obj: ImageObject = obj
        self.scale = scale

    @typechecked
    def get_width(self) -> int:
        return int(self.obj.get_width() * self.scale)

    @typechecked
    def get_height(self) -> int:
        return int(self.obj.get_height() * self.scale)

    @typechecked
    def draw(self, painter: QPainter) -> None:
        old_transform: QTransform = painter.transform()
        transform: QTransform = QTransform()
        w: int = self.obj.get_width()
        h: int = self.obj.get_height()
        transform.translate(w//2, h//2)
        transform.scale(self.scale, self.scale)
        transform.translate(-w//2, -h//2)
        painter.setTransform(transform, combine=True)
        self.obj.draw(painter)
        painter.setTransform(old_transform, combine=False)


class Rotate(ImageObject):
    """
    This class is a container that rotates the contained object counterclockwise
    around the center of its bounding box.
    The rotation angle is given in degree (0..360°).
    """
    @typechecked
    def __init__(self, obj: ImageObject, rotation_angle: float):
        """
        Creates a rotation container object that rotates the contained coordinates counterclockwise.
        :param obj: the contained object (to be rotated)
        :param rotation_angle: the angle in degrees (0...360°)
        """
        self.obj: ImageObject = obj
        self.rotation_angle = rotation_angle

    @typechecked
    def get_width(self) -> int:
        return max(self.obj.get_width(), self.obj.get_height())

    @typechecked
    def get_height(self) -> int:
        return max(self.obj.get_width(), self.obj.get_height())

    @typechecked
    def draw(self, painter: QPainter) -> None:
        old_transform: QTransform = painter.transform()
        transform: QTransform = QTransform()
        w: int = self.obj.get_width()
        h: int = self.obj.get_height()
        transform.translate(w//2, h//2)
        transform.rotate(self.rotation_angle)
        transform.translate(-w//2, -h//2)
        painter.setTransform(transform, combine=True)
        self.obj.draw(painter)
        painter.setTransform(old_transform, combine=False)


__all__ = ['ImageObject', 'Rectangle', 'Circle', 'Ellipse', 'Polygon', 'Text',
           'VerticalStack', 'HorizontalStack', 'Overlay', 'Translate', 'Scale', 'Rotate']
