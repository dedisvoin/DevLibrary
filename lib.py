# imports ---------------------------------------

import keyboard
import pygame
import socket
import random
import typing
import types
import math
import sys
import os


from dataclasses import dataclass
from colorama import Fore, Style
from ast import literal_eval
from threading import Thread
from pygame import gfxdraw
from typing import overload
from typing import Iterable
from time import sleep
from typing import Any


# imports ---------------------------------------

# base decorators -------------------------------


def NewProcess(func: typing.Callable):
    def wrapper(*args, **kvargs):
        Thread(target=func, args=args, kwargs=kvargs).start()

    return wrapper


def TimeProcess(func: typing.Callable):
    def wrapper(*args, **kvargs):
        start = pygame.time.get_ticks()
        func(*args, **kvargs)
        end = pygame.time.get_ticks()
        print(f"Time ({func.__name__}): {end - start}")

    return wrapper


# base decorators -------------------------------

# flags -----------------------------------------


@dataclass
class Flags:
    win_full = pygame.FULLSCREEN
    win_resize = pygame.RESIZABLE
    win_scales = pygame.SCALED
    win_noframe = pygame.NOFRAME
    win_anyfull = ["anyfull", pygame.FULLSCREEN]

    cursor_diamond = pygame.cursors.diamond
    cursor_ball = pygame.cursors.ball
    cursor_arrow = pygame.cursors.arrow
    cursor_broken = pygame.cursors.broken_x


# flags -----------------------------------------


# base window class -----------------------------


class Window:
    def __init__(
        self,
        size: list[int, int] = [800, 650],
        win_name: str = "Main",
        flag: typing.Any = None,
        cursor: Any = None,
    ) -> None:
        self.__size = size
        self.__win_name = win_name
        self.__flag = flag
        self._win_opened = False
        self._delta = 0
        self.__delta_velosity = 60

        self.__create_win_with_params(self.__size, self.__win_name, self.__flag)
        if cursor is not None:
            pygame.mouse.set_cursor(cursor)

        self._win_opened = True
        self._fps_surf = Text("Arial", 20, bold=True)
        self._exit_hot_key = "esc"

    def __any_full__(self, _flag: typing.Any) -> bool:
        if type(_flag) == list:
            if _flag[0] == "anyfull":
                return True
        return False

    def __call__(self) -> pygame.Surface:
        return self._win

    def __create_win_with_params(
        self, _p_size: list, _p_win_name: str, _p_flag: typing.Any
    ) -> None:
        pygame.init()
        if self.__any_full__(_p_flag):
            _flag = _p_flag[1]
            _p_size = [pygame.display.Info().current_w, pygame.display.Info().current_h]
        else:
            _flag = 0 if _p_flag is None else _p_flag
        self._win = pygame.display.set_mode(_p_size, _flag)
        pygame.display.set_caption(_p_win_name)
        self._clock = pygame.time.Clock()

    def __mathing_delta(self):
        fps = self.fps
        try:
            self._delta = self.__delta_velosity / fps
        except Exception:
            ...

    @property
    def delta(self) -> float:
        return self._delta

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self._win.get_size()

    @property
    def center(self) -> typing.Tuple[int, int]:
        return self._win.get_rect().center

    @property
    def fps(self):
        return self._clock.get_fps()

    @fps.setter
    def fps(self, _framerate: int):
        if _framerate == "max":
            _framerate = 5000
        elif _framerate == "min":
            _framerate = 30
        else:
            ...
        self._clock.tick(_framerate)

    def __events_handling(self):
        _events = pygame.event.get()
        for event in _events:
            if event.type == pygame.QUIT:
                self._win_opened = False
                os._exit(0)

        if keyboard.is_pressed(self._exit_hot_key):
            self._win_opened = False
            os._exit(0)

    def fps_view(self):
        self._win.blit(
            self._fps_surf.render(f"FPS: {int( self.fps )}", "black")(), (10, 10)
        )

    def update(
        self,
        fps: int = 60,
        base_color: list | str = "white",
        fps_view: bool = True,
        exit_hot_key: str = "esc",
    ) -> None:
        self._exit_hot_key = exit_hot_key
        self.__events_handling()

        self.fps = fps
        self.__mathing_delta()

        pygame.display.flip()
        self._win.fill(base_color)

        if fps_view:
            self.fps_view()

        return self._win_opened

    def get_at(self, x: int, y: int) -> list:
        return self._win.get_at((x, y))


# base window class -----------------------------

# base surface class ----------------------------


class Surface:
    def __init__(self, size: typing.Tuple[int, int] = [1, 1]) -> None:
        self.__size = size
        self._surface = pygame.Surface(self.__size)

    def __call__(self) -> pygame.Surface:
        return self._surface

    def convert(cls, surface: pygame.Surface) -> typing.Self:
        cls._surface = surface
        return cls

    @property
    def size(self) -> typing.Tuple[int, int]:
        return self._surface.get_size()

    def get_at(self, x: int, y: int) -> list:
        return self._surface.get_at((x, y))


# base surface class ----------------------------

# base text class -------------------------------


class Text:
    def __init__(
        self,
        font: pygame.Font,
        font_size: int,
        text: str = None,
        color: list | str = "white",
        bold: bool = False,
    ) -> None:
        pygame.font.init()

        self.__font = font
        self.__font_size = font_size
        self.__bold = bold
        self.__font_object = pygame.font.SysFont(
            self.__font, self.__font_size, self.__bold
        )
        if text is not None:
            self.__text = text
            self.__font_surf = self.__font_object.render(self.__text, True, color)

    def draw(
        self,
        surface: pygame.Surface,
        pos: list[int, int] = [0, 0],
        centering: bool = False,
    ) -> None:
        if centering:
            pos = [
                pos[0] - self.__font_surf.get_width() // 2,
                pos[1] - self.__font_surf.get_height() // 2,
            ]
        surface.blit(self.__font_surf, pos)

    def render(self, text: str, color: list | str = "white") -> Surface:
        self.__text = text
        self.__font_surf = self.__font_object.render(self.__text, True, color)
        return Surface().convert(self.__font_surf)


# base text class -------------------------------

# base math class -------------------------------


class Vector2:
    @overload
    def __init__(self, x_y: typing.Tuple[float, float]) -> "Vector2":
        ...

    @overload
    def __init__(self, x_: float, y_: float) -> "Vector2":
        ...

    def __init__(self, *_args) -> "Vector2":
        self.__args_manager__(*_args)

    def __args_manager__(self, *args):
        if len(args) == 1:
            self._x = args[0][0]
            self._y = args[0][1]
        elif len(args) == 2:
            self._x = args[0]
            self._y = args[1]

    def __str__(self) -> str:
        return f"Vector2 {self._x, self._y}"

    @property
    def lenght(self):
        return vector_lenght(self._x, self._y)

    @lenght.setter
    def lenght(self, _value: int):
        self._x *= _value / self.lenght
        self._y *= _value / self.lenght

    def rotate(self, angle: int):
        angle = math.radians(angle)
        _x = self._x * math.cos(angle) - self._y * math.sin(angle)
        _y = self._x * math.sin(angle) + self._y * math.cos(angle)
        self._x = _x
        self._y = _y

    def set_angle(self, angle: int):
        lenght = self.lenght
        angle = math.radians(angle)
        self._x = math.cos(angle) * lenght
        self._y = math.sin(angle) * lenght

    def get_angle(self) -> float:
        return angle_to_float([0, 0], [self._x, self._y])

    def normalyze(self):
        lenght = self.lenght
        self._x /= lenght
        self._y /= lenght

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @x.setter
    def x(self, value: float) -> None:
        self._x = value

    @y.setter
    def y(self, value: float) -> None:
        self._y = value

    @property
    def xy(self) -> typing.Tuple[int, int]:
        return [self._x, self._y]


def distance(
    point_1: Any | typing.Tuple[int, int], point_2: Any | typing.Tuple[int, int]
):
    dx = point_1[0] - point_2[0]
    dy = point_1[1] - point_2[1]
    _distance = math.sqrt(dx**2 + dy**2)
    return _distance


def vector_lenght(lenght_x: int, lenght_y: int):
    _distance = math.sqrt(lenght_x**2 + lenght_y**2)
    return _distance


def center(rect_size: typing.Tuple[int, int], rect_pos: typing.Tuple[int, int]):
    return [rect_pos[0] + rect_size[0] / 2, rect_pos[1] + rect_size[1] / 2]


def angle_to(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    if isinstance(point_1, Vector2):
        pos1 = point_1.xy
    elif isinstance(point_1, (list, tuple)):
        pos1 = point_1

    if isinstance(point_2, Vector2):
        pos2 = point_2.xy
    elif isinstance(point_2, (list, tuple)):
        pos2 = point_2

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return int(atan / math.pi * 180 + 180)


def angle_to_float(
    point_1: typing.Tuple[int, int] | "Vector2",
    point_2: typing.Tuple[int, int] | "Vector2",
) -> float:
    if isinstance(point_1, Vector2):
        pos1 = point_1.xy
    elif isinstance(point_1, (list, tuple)):
        pos1 = point_1

    if isinstance(point_2, Vector2):
        pos2 = point_2.xy
    elif isinstance(point_2, (list, tuple)):
        pos2 = point_2

    atan = math.atan2(pos1[0] - pos2[0], pos1[1] - pos2[1])
    return atan / math.pi * 180 + 180


def in_rect(
    rect_pos_: typing.Tuple[float, float] | Vector2,
    rect_size_: typing.Tuple[float, float] | Vector2,
    point_: typing.Tuple[float, float] | Vector2,
):
    if isinstance(rect_pos_, Vector2):
        rect_pos = rect_pos_.xy
    elif isinstance(rect_pos_, (list, tuple)):
        rect_pos = rect_pos_

    if isinstance(rect_size_, Vector2):
        rect_size = rect_size_.xy
    elif isinstance(rect_size_, (list, tuple)):
        rect_size = rect_size_

    if isinstance(point_, Vector2):
        point = point_.xy
    elif isinstance(point_, (list, tuple)):
        point = point_

    if (
        point[0] > rect_pos[0]
        and point[0] < rect_pos[0] + rect_size[0]
        and point[1] > rect_pos[1]
        and point[1] < rect_pos[1] + rect_size[1]
    ):
        return True
    else:
        return False


# base math class -------------------------------

# base draw class -------------------------------


class Color:
    def __init__(self, color: list | tuple) -> None:
        self._r = color[0]
        self._g = color[1]
        self._b = color[2]

    @classmethod
    def random(self) -> "Color":
        _r = random.randint(0, 255)
        _g = random.randint(0, 255)
        _b = random.randint(0, 255)
        return Color([_r, _g, _b])

    @property
    def rgb(self):
        return [self._r, self._g, self._b]

    @property
    def chb(self):
        _chb_value = (self._r + self._g + self._b) / 3
        return [_chb_value, _chb_value, _chb_value]

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, _value: int):
        self._r = _value

    @property
    def g(self):
        return self._g

    @g.setter
    def g(self, _value: int):
        self._g = _value

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, _value: int):
        self._b = _value


class Draw:
    @classmethod
    def __outline(self, _color, _width, _type, _surf, **kvargs):
        if _type == "rect":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            size = kvargs["size"]
            Draw.draw_rect(_surf, pos, size, _color, _width, radius=radius)
        elif _type == "circle":
            radius = kvargs["radius"]
            pos = kvargs["pos"]
            Draw.draw_circle(_surf, pos, radius, _color, _width)
        elif _type == "polygone":
            points = kvargs["points"]
            Draw.draw_polygone(_surf, points, _color, _width)

    @classmethod
    def draw_rect(
        self,
        surface: pygame.Surface,
        pos: list[int],
        size: list[int],
        color: list | str | Color = "gray",
        width: int = 0,
        radius: int = -1,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if len(size) == 1:
            size = [size[0], size[0]]
        if isinstance(radius, (list, tuple)):
            lt_rad = radius[0]
            rt_rad = radius[1]
            rb_rad = radius[2]
            lb_rad = radius[3]
            radius = -1
        else:
            lt_rad = radius
            rt_rad = radius
            rb_rad = radius
            lb_rad = radius
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.rect(
            surface, color, (pos, size), width, radius, lt_rad, rt_rad, lb_rad, rb_rad
        )

        if outline is not None:
            Draw.__outline(
                outline[0],
                outline[1],
                "rect",
                surface,
                radius=(lt_rad, rt_rad, rb_rad, lb_rad),
                pos=pos,
                size=size,
            )

    @classmethod
    def draw_circle(
        self,
        surface: pygame.Surface,
        pos: list[int],
        radius: int,
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.circle(surface, color, pos, radius, width)

        if outline is not None:
            Draw.__outline(
                outline[0], outline[1], "circle", surface, pos=pos, radius=radius
            )

    @classmethod
    def draw_polygone(
        self,
        surface: pygame.Surface,
        points: list[list[int]],
        color: list | str | Color = "gray",
        width: int = 0,
        outline: typing.Tuple[list | str | Color, int] = None,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        pygame.draw.polygon(surface, color, points, width)

        if outline is not None:
            Draw.__outline(outline[0], outline[1], "polygone", surface, points=points)

    @classmethod
    def draw_line(
        self,
        surface: pygame.Surface,
        point_1: list | tuple | Vector2,
        point_2: list | tuple | Vector2,
        color: list | str | Color = "gray",
        width: int = 1,
    ) -> None:
        if isinstance(color, Color):
            color = color.rgb
        if isinstance(point_1, Vector2):
            pos1 = point_1.xy
        elif isinstance(point_1, (list, tuple)):
            pos1 = point_1
        if isinstance(point_2, Vector2):
            pos2 = point_2.xy
        elif isinstance(point_2, (list, tuple)):
            pos2 = point_2
        pygame.draw.line(surface, color, pos1, pos2, width)

    @classmethod
    def draw_vline(
        self,
        surface: pygame.Surface,
        x: int,
        y1: int,
        y2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        for i in range(width):
            gfxdraw.vline(surface, x - int(width / 2) + i, y1, y2, color)

    @classmethod
    def draw_hline(
        self,
        surface: pygame.Surface,
        y: int,
        x1: int,
        x2: int,
        width: int = 1,
        color: list | str | Color = (100, 100, 100),
    ) -> None:
        for i in range(width):
            gfxdraw.hline(surface, x1, x2, y - int(width / 2) + i, color)


# base draw class -------------------------------

# base input class ------------------------------


class Mouse:
    left = "_left"
    right = "_right"
    middle = "_middle"

    end_pos = [0, 0]
    pressed = False

    @classmethod
    @property
    def position(self) -> list[int, int]:
        return pygame.mouse.get_pos()

    def set_position(self, pos: typing.Tuple[int, int]) -> None:
        pygame.mouse.set_pos(pos)

    @classmethod
    def press(self, button: str = left):
        if button == Mouse.left:
            return pygame.mouse.get_pressed()[0]
        if button == Mouse.middle:
            return pygame.mouse.get_pressed()[1]
        if button == Mouse.right:
            return pygame.mouse.get_pressed()[2]

    @classmethod
    def click(self, button: str = left):
        p = self.press(button)
        if p:
            if not self.pressed:
                self.pressed = True
                return True
            else:
                return False
        else:
            self.pressed = False
            return False

    @classmethod
    @property
    def speed(self) -> typing.Tuple[int, int]:
        pos = self.position
        dx = pos[0] - self.end_pos[0]
        dy = pos[1] - self.end_pos[1]

        self.end_pos = pos
        return [dx, dy]

    @classmethod
    def set_cursor(self, cursor: Any) -> None:
        pygame.mouse.set_cursor(cursor)


# base input class ------------------------------


# base socket manager ---------------------------


def string_to_list(string_: str) -> list:
    return literal_eval(string_)


def list_to_string(list_: list) -> str:
    return str(list_)


def packing(data_: Iterable, packet_name_: str) -> bytes:
    _inf = [packet_name_, data_]
    convert_data = list_to_string(_inf).encode()
    return convert_data


def unpacking(data_: bytes) -> list:
    convert_data = string_to_list(data_.decode())
    return convert_data


def socket_sleep(sec_: float):
    sleep(sec_)


def packet_with_name(data_: Any, name_: str):
    if data_[0] == name_:
        return data_[1]
    else:
        None


localhost = "localhost"


class Server:
    def __init__(
        self,
        port_: int = 4000,
        host_: str = localhost,
        name_: str = "my server",
        max_client_: int = 2,
    ) -> None:
        self._port = port_
        self._host = host_
        self._name = name_

        self._clients: typing.Tuple[socket.socket] = []

        self._client_connecting = False

        self._max_client = max_client_

        self._end_conn_client = None
        self._end_conn_addr = None

        self.__init()

    def __init(self) -> None:
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self._server.bind((self._host, self._port))
        self._server.setblocking(0)
        self._server.listen(5)

    @property
    def clientcon(self) -> bool:
        return self._client_connecting

    @property
    def max_connected(self) -> bool:
        if len(self._clients) == self._max_client:
            return False
        else:
            return True

    def waitcon(self, sec_: float):
        sleep(sec_)
        self._client_connecting = False
        if len(self._clients) < self._max_client:
            try:
                client, addr = self._server.accept()
                client.setblocking(0)
                self._client_connecting = True
                self._clients.append([client, addr])
                self._end_conn_client = client
                self._end_conn_addr = addr

                print(f"Client {addr} connected!")
            except:
                self._client_connecting = False

    def send_packet(self, packet_: bytes) -> None:
        for client in self._clients:
            try:
                client[0].send(packet_)
            except:
                ...

    def recv_packet(self, buf_size: int = 2048) -> str:
        packets = []
        for client in self._clients:
            packet = client.recv(buf_size)
            _inf = packet.decode()
            _list_inf = string_to_list(_inf)
            packets.append(_list_inf)
        return packets


class Client:
    def __init__(self, port_: int = 4000, host_: str = localhost) -> "Client":
        self._port = port_
        self._host = host_

        self._client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._client.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

        self._client.connect((self._host, self._port))
        print(f"Connected!")

    def recv_packet(self, buf_size: int = 2048) -> str:
        packet = self._client.recv(buf_size)
        _inf = packet.decode()
        return _inf

    def send_packet(self, packet_: bytes) -> None:
        try:
            self._client.send(packet_)
        except:
            ...


# base socket manager ---------------------------
