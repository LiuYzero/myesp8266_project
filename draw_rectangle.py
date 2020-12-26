from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math
import time


def light_dot(x, y):
    oled.pixel(x, y, 1)


def draw_line(x1, y1, x2, y2, isRectangle=0):
    '''
    绘制线段
    :param: x1 y1 x2 y2 线段两端
    :param: isRetangle 是否为矩形
    :return: None
    '''
    if (x1 == x2):
        step = 1
        if (y1 > y2):
            step *= -1
        while (y1 != y2):
            light_dot(x1, y1)
            y1 = y1 + step
        light_dot(x2, y2)
    else:
        # y = kx+a
        k = (y2 - y1) / (x2 - x1)
        a = y1 - (k * x1)
        step = 1
        if (x1 > x2):
            step *= -1
        while (x1 != x2):
            light_dot(x1, round(k * x1 + a))
            x1 += step
        light_dot(x2, y2)
    if not isRectangle:
        oled.show()


def draw_rectangle(x, y, length, width, isFill=0):
    '''
    绘制矩形
    :param: x y 矩形左上角
    :param: length width 长和宽
    :isFill: 是否填充 0 否 1 是
    :return: None
    '''
    point_upper_left = (x, y)
    point_upper_right = (x + length, y)
    point_bottom_left = (x, y + width)
    point_bottom_right = (x + length, y + width)

    draw_line(point_upper_left[0], point_upper_left[1],
              point_upper_right[0], point_upper_right[1], 1)
    draw_line(point_upper_left[0], point_upper_left[1],
              point_bottom_left[0], point_bottom_left[1], 1)
    draw_line(point_bottom_left[0], point_bottom_left[1],
              point_bottom_right[0], point_bottom_right[1], 1)
    draw_line(point_upper_right[0], point_upper_right[1],
              point_bottom_right[0], point_bottom_right[1], 1)

    if isFill:
        for xx in range(x, x + length + 1):
            draw_line(xx, y, xx, y + width, 1)

    oled.show()


def draw_diamond(x, y, side_length, angle):
    '''
    绘制菱形
    有点BUG -_- 勉强能用
    :param: x y 菱形顶点
    :param: side_length 边长
    :angle: 顶角 [0,90]
    :return: None
    '''
    xx = abs(round(math.sin(angle / 2) * side_length))
    yy = abs(round(math.cos(angle / 2) * side_length))

    point_upper = (x, y)
    point_left = (x - xx, y + yy)
    point_right = (x + xx, y + yy)
    point_bottom = (x, y + yy * 2)

    draw_line(point_upper[0], point_upper[1], point_left[0], point_left[1])
    draw_line(point_upper[0], point_upper[1], point_right[0], point_right[1])
    draw_line(point_bottom[0], point_bottom[1], point_left[0], point_left[1])
    draw_line(point_bottom[0], point_bottom[1], point_right[0], point_right[1])


if __name__ == '__main__':
    i2c = I2C(scl=Pin(5), sda=Pin(4))
    oled = SSD1306_I2C(128, 64, i2c)
    oled.fill(0)

    draw_rectangle(10, 10, 30, 20)
    draw_rectangle(10, 40, 60, 20, 1)
    draw_diamond(90, 10, 30, 45)
