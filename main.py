


from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
import urequests as requests
import network
import time
import tm1637
import dht
import gc

def connectionWifi(ssid, password):
  wlan = network.WLAN(network.STA_IF)
  wlan.active(True)
  wlan.connect(ssid, password)
  while True:
    if not wlan.isconnected():
      time.sleep_ms(2000)
    else:
      print('connected to network')
      break

def getJsonInfoFromURL(url):
  response = requests.get(url)
  return response.json()

def tm1637_LED(hours, minutes):
  if hours > 22 or hours < 6:
    tm.brightness(0)
  else:
    tm.brightness(3)
  tm.numbers(hours, minutes)


def buzzer(hours, minutes):
  global bing_last_minutes
  print("bing_last_minutes: "+str(bing_last_minutes))
  print("minutes: "+ str(minutes))
  if hours == 7 and minutes == 0:
    if bing_last_minutes != minutes:
      buzzer_seconds(10)
  elif hours >= 7  :
    if minutes == 0:
      if bing_last_minutes != minutes:
        buzzer_seconds(2)
    elif minutes == 30:
      if bing_last_minutes != minutes:
        buzzer_seconds(1)
  bing_last_minutes = minutes

def buzzer_seconds(seconds):
  
  bing.value(1)
  print("should buzzer")
  time.sleep_ms(seconds*1000)
  print("after sleep")
  bing.value(0)
  print("bing.value(0)")

#def getTHFromDHT11(dht11):
#  dht11.measure()
#  return dht11.temperature(),dht11.humidity()

def getTHFromDHT11(dht11):
  print ("enter into getTHFromFHT11")
  sumT=0
  sumH=0
  repeats=5
  for i in range(repeats):
    dht11.measure()
    sumT += dht11.temperature()
    sumH += dht11.humidity()
    print ("sumT is "+str(sumT))
    print ("sumH is "+str(sumH))
    time.sleep_ms(1000)
  return sumT/repeats, sumH/repeats;  
  
def uploadTempAndHumidity(dht11,url,position):
  temperature, humidity = getTHFromDHT11(dht11)
  url = url+"/"+position+"/"+str(temperature)+"/"+str(humidity)
  print(url)
  requests.get(url)
  
def myDHT11(hours,minutes, dth11, url, position):
  print("Enter into myDHT11")
  global dht11_last_hours
  print("last: "+str(dht11_last_hours))
  print("hours: "+str(hours))
  if hours != dht11_last_hours:
    uploadTempAndHumidity(dht11, dht11_api, "home")
    print("afterUpload")
    dht11_last_hours = hours
    
  
if __name__== '__main__':

  ssid='xxxx'
  password='xxxx'
  time_api="xxxx"
  dht11_api="xxxxx"
  position="home"

  tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
  bing = Pin(12,Pin.OUT)
  bing_last_minutes = 0
  
  dht11 = dht.DHT11(machine.Pin(14))
  dht11_last_hours = 0
  

  connectionWifi(ssid, password)

  while True:
    try:
      print("==================================================================")
      print("enter main")
      result = getJsonInfoFromURL(time_api)
      print(result)
      print("after date")
      tm1637_LED(result['hours'], result['minutes'])
      print("after led")
      buzzer(result['hours'], result['minutes'])
      print("after buzzer")
      myDHT11(result['hours'], result['minutes'], dht11, dht11_api, position)
      print("aftre myDHT11")
      time.sleep_ms(20000)
      gc.collect()
    except:
      gc.collect()
      connectionWifi(ssid, password)
      tm = tm1637.TM1637(clk=Pin(5), dio=Pin(4))
      bing = Pin(12,Pin.OUT)
      dht11 = dht.DHT11(machine.Pin(14))
      bing.value(0)







