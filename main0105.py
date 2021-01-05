from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math
import time


def light_dot(x, y):
  oled.pixel(x, y, 1)


def draw_circular_arc(x, y, r, start_angle, end_angle, isShow=1):
  '''
  绘制圆弧
  :x,y 圆心坐标
  :r 半径
  :start_angle,end_angle 角度范围
  :isShow 是否显示
  '''
  # 0度的位置有点怪，顺时针转了90度。+90度作为补偿。
  angleList = [math.radians(i+90) for i in range(start_angle, end_angle+1)]
  for i in angleList:
    light_dot(x+round(math.sin(i)*r), y+round(math.cos(i)*r))
  if isShow:
    oled.show()


def draw_circular(x, y, r, fill=0):
  '''
  绘制圆，并决定是否填充
  :x,y 圆心坐标
  :r 半径
  :fill 是否填充 0 否 1 是
  '''
  draw_circular_arc(x, y, r, 0, 360, isShow=0)
  if fill:
    powR = math.pow(r, 2)
    for xx in range(x-r, x+r):
      for yy in range(y-r, y+r):
        if ((math.pow(xx-x, 2)+math.pow(yy-y, 2)) < powR):
          light_dot(xx, yy)
  oled.show()


def draw_wifi_logo(x, y):
  '''
  绘制wifi图标
  :x,y 图标左上角坐标，长宽约为(30,16)
  '''
  x = x+13
  y = y+16
  start_angle = 45
  end_angle = 135
  draw_circular(x, y, 1, 1)
  draw_circular_arc(x, y, 6, start_angle, end_angle)
  draw_circular_arc(x, y, 11, start_angle, end_angle)
  draw_circular_arc(x, y, 16, start_angle, end_angle)

  oled.show()


if __name__ == '__main__':

  i2c = I2C(scl=Pin(5), sda=Pin(4))
  oled = SSD1306_I2C(128, 64, i2c)
  oled.fill(0)

  draw_wifi_logo(20, 20)
