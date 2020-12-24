
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

def light_dot(x,y):
  oled.pixel(x,y,1)

def draw_line(x1,y1,x2,y2):
  if ( x1 == x2 ):
    step = 1
    if ( y1 > y2 ) :
      step *= -1
    while ( y1 != y2 ):
      light_dot(x1, y1)
      y1 = y1+step
    light_dot(x2,y2)
    oled.show()
  else :
    # y = kx+a
    k = (y2-y1)/(x2-x1)
    a = y1-(k*x1)
    step = 1
    if ( x1 > x2 ) :
      step *= -1
    while ( x1 != x2 ):
      light_dot(x1, round(k*x1+a))
      x1 += step
    light_dot(x2,y2)
    oled.show()
      
  
if __name__ == '__main__':
    
  i2c = I2C(scl=Pin(5), sda=Pin(4))
  oled = SSD1306_I2C(128, 64, i2c)  
  oled.fill(0)
  oled.show()

  draw_line(0,0, 127,63)
  draw_line(0,63, 127,0)

  draw_line(0,0, 127,0)
  draw_line(0,0, 0,63)
  draw_line(127,0, 127,63)
  draw_line(0,63, 127,63)
