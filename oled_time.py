import network
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import math
import time
import random
import urequests as requests
import gc

def light_dot(x, y, width=4):
    #oled.pixel(x, y, 1)
    for i in range(x,x+width):
      for j in range(y,y+width):
        oled.pixel(i,j,1)


def draw_line(x1, y1, x2, y2, isShow=1):
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
        if (abs(k) <= 1):
          a = y1 - (k * x1)
          step = 1
          if (x1 > x2):
              step *= -1
          while (x1 != x2):
              light_dot(x1, round(k * x1 + a))
              x1 += step
          light_dot(x2, y2)
        else:
          k = (x2-x1)/(y2-y1)
          a = x1-(k*y1)
          step = 1
          if (y1 > y2):
            step *= -1
          while (y1 != y2):
            light_dot(round(k*y1+a),y1)
            y1 += step
          light_dot(x2, y2)



def draw_one(x,y):
  draw_line(x,y,x,y+16)
def draw_two(x,y):
  draw_line(x,y,x+16,y)
def draw_three(x,y):
  draw_line(x+16,y,x+16,y+16)
def draw_four(x,y):
  draw_line(x,y+16,x+16,y+16)
def draw_five(x,y):
  draw_line(x,y+16,x,y+32)
def draw_six(x,y):
  draw_line(x,y+32,x+16,y+32)
def draw_seven(x,y):
  draw_line(x+16,y+16,x+16,y+32)


def draw_number_zero(x,y):
  draw_one(x,y)
  draw_two(x,y)
  draw_three(x,y)
  draw_five(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_one(x,y):
  draw_three(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_two(x,y):
  draw_two(x,y)
  draw_three(x,y)
  draw_four(x,y)
  draw_five(x,y)
  draw_six(x,y)
  oled.show()
def draw_number_three(x,y):
  draw_two(x,y)
  draw_three(x,y)
  draw_four(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_four(x,y):
  draw_one(x,y)
  draw_three(x,y)
  draw_four(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_five(x,y):
  draw_one(x,y)
  draw_two(x,y)
  draw_four(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_six(x,y):
  draw_one(x,y)
  draw_two(x,y)
  draw_four(x,y)
  draw_five(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_seven(x,y):
  draw_two(x,y)
  draw_three(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_eight(x,y):
  draw_one(x,y)
  draw_two(x,y)
  draw_three(x,y)
  draw_four(x,y)
  draw_five(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()
def draw_number_nine(x,y):
  draw_one(x,y)
  draw_two(x,y)
  draw_three(x,y)
  draw_four(x,y)
  draw_six(x,y)
  draw_seven(x,y)
  oled.show()

def draw_clock_char(x,y,char):
  if char == '0':
    draw_number_zero(x,y)
  elif char == '1':
    draw_number_one(x,y)

  elif char =='2':
    draw_number_two(x,y)
  elif char =='3':
    draw_number_three(x,y)
  elif char =='4':
    draw_number_four(x,y)
  elif char =='5':
    draw_number_five(x,y)
  elif char =='6':
    draw_number_six(x,y)
  elif char =='7':
    draw_number_seven(x,y)
  elif char =='8':
    draw_number_eight(x,y)
  elif char =='9':
    draw_number_nine(x,y)

def draw_clock(x,y,str_clock):
  for i in range(4):
    draw_clock_char(x+i*30, y, str_clock[i])



def connectionWifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)
  while True:
    if not wlan.isconnected():
      time.sleep_ms(2000)
    else:
      print('connected to network')
      return wlan.ifconfig()
      break

def getJsonInfoFromURL(url):
  response = requests.get(url)
  return response.json()

def my_str(num):
  if num < 10:
    return "0"+str(num)
  return str(num)

if __name__ == '__main__':
  gc.collect()
  i2c = I2C(scl=Pin(5), sda=Pin(4))
  oled = SSD1306_I2C(128, 64, i2c)


  ssid='FAST_20CC'
  password='409409409'
  ifconfig = connectionWifi(ssid, password)
  while True:
    try:
      result = getJsonInfoFromURL("http://ip/bills/ESP8266TimeAPI")
      str_clock= my_str(result['hours'])+my_str(result['minutes'])
      print(str_clock)
      count = 0
      while (count<5):
          oled.fill(0)
          oled.show()
          time.sleep(1)
          draw_clock(random.getrandbits(4)%10,random.getrandbits(5)%20,str_clock)
          time.sleep(5)
          count = count+1
      gc.collect()
    except :
      print("program get Error")
