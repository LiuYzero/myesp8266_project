



import network
from machine import Pin, I2C
import time
import urequests as requests
from ssd1306 import SSD1306_I2C
#from logo import wifi_logo
#from logo import ff_arr
import logo


#print ("ligth it")
#for i in range(0,64):
#  for j in range(0,128):
#    oled.pixel(j,i,1)
#    oled.show()


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
  
def light_dot(x,y):
  oled.pixel(x,y,1)
  

def dark_dot(x,y):
  oled.pixel(x,y,0)

def my_str(num):
  if num < 10:
    return "0"+str(num)
  
  return str(num)

def time_str_to_num(time_str, i):
  if time_str[i] == ":":
    return 10
  else:
    return int(time_str[i])

def light_matrix(x,y,mode,len=2):
  for i in range(x,x+len,1):
    for j in range(y,y+len,1):
      #print (i,"",j)
      #time.sleep_ms(100)
      if mode == 1:
        light_dot(i,j)
      else:
        dark_dot(i,j)
  
if __name__ == '__main__':
  
  i2c = I2C(scl=Pin(5), sda=Pin(4))
  oled = SSD1306_I2C(128, 64, i2c)
  
  
  steps = 128 * 64
  direction_mode = 0
  step = 0
  x=0
  y=0
  
  flag  = 1
  while ( step <= 256 ):
    light_dot(x,y)
    
    if (flag==1):
      if ( x >= 127):
        direction_mode = 1
      if ( x>= 127 and y >= 63):
        direction_mode = 2
      if ( x <=0 and y>=63):
        direction_mode = 3
      if ( x == 0 and y == 1 ):
        print ('flag 2')
        flag = 2
        direction_mode = 0
        break

    if(direction_mode == 0):
      x = x+1
    elif (direction_mode == 1):
      y= y+1
    elif (direction_mode == 2):
      x = x-1
    elif (direction_mode == 3):
      y = y-1
  
  oled.show()
  
  line_y = 40
  for x in range(0,128):
    light_dot(x, line_y)
   
  oled.show()
  
  line_x=90
  for y in range (0,line_y):
    light_dot(line_x, line_y-y)
  
  oled.show()
  
  print ("done")

  ssid='FAST_20CC'
  password='409409409'
  
  oled.text("wifi module loading..",5,50)

  print ("connectionWifi")
  ifconfig = connectionWifi(ssid, password)
  
  for i in range(1,127):
    for j in range(line_y+1,63):
      dark_dot(i,j)
  oled.show()  
  
  print ("print ip")
  
  oled.text(""+ifconfig[0],5,50)

#  network logo  
#  for y in range(8, 35,3):
#    for x in range(98, 120,2):
#      if ( (x+y) < 129):
#        light_dot(x,y)
#        oled.show()

# wifi logo
  for i in range (len(logo.wifi_logo)):
    for j in range (len(logo.wifi_logo[i])):
      oled.pixel(j+line_x+5,i+2,logo.wifi_logo[i][j])
    oled.show()
    
  while 1:  
    try:
      result = getJsonInfoFromURL("http://120.79.94.66:8080/bills/ESP8266TimeAPI")
      print (result)

      for x in range(1,89):
        for y in range(1,39):
          dark_dot(x,y)
      oled.show()

      #oled.text(my_str(result['hours'])+":"+my_str(result['minutes']),5,10)

      time_str = my_str(result['hours'])+":"+my_str(result['minutes'])
      time_x = 2
      time_y = 5
      for i in range(len(time_str)):
        current_x = time_x+i*8*2
        #current_x = time_x+i*10
        current_y = time_y

        #print (time_x+i*8, time_y, time_str[i])
        current_num = time_str_to_num(time_str, i)
        num_arr= logo.ff_arr[current_num*16:current_num*16+16]
        #print (num_arr)

        for j in range(len(num_arr)):
          now_x = current_x+j
          now_y = current_y+j*2
          #now_y = current_y+j
          
          #binary_str = bin(int(num_arr[j], 16))
          binary_str = '{:08b}'.format(int(num_arr[j],16))
          #print (binary_str)
          for k in range(0,len(binary_str)):
            if ( binary_str[k] == "0" ):
              #oled.pixel(now_x+k, now_y, 0)
              #oled.pixel(now_x+k+k, now_y, 0)
              light_matrix(now_x+k, now_y, 0)
            else:
              #oled.pixel(now_x+k, now_y, 1)
              light_matrix(now_x+k, now_y, 1)
      oled.show()  


      time.sleep_ms(15000)
      gc.collect()
    except:
      print ("except")



