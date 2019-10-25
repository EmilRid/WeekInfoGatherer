import requests
from bs4 import BeautifulSoup
import re

foods = []
school = "" #School name without å, ä, ö
SchoolFoodURL ="https://skolmaten.se/" + school
SchoolFoodPage = requests.get(SchoolFoodURL)
SchoolFoodSoup = BeautifulSoup(SchoolFoodPage.text, "html.parser")
weatherURL = "" #weather.com search result 
weatherPage = requests.get(weatherURL) 
weatherSoup = BeautifulSoup(weatherPage.text, "html.parser")

def getWeek(): #prints out food for all days of the week
  for day in SchoolFoodSoup.find_all(class_="row"):
    text = day.get_text().split("\n")
    for line in text:
      if line !="" and "Varje dag" not in line and "Klicka här" not in line:
        print(line)
        foods.append(line)
    print("")

def getTemp(unit): #returns temperature value, unit: celsius or fahrenheit
    farhenheit = int(weatherSoup.find(class_="today_nowcard-temp").get_text()[0:-1])
    if unit == "celsius":
        return round((farhenheit-32)*5/9)
    elif unit == "fahrenheit":
        return farhenheit
    else: 
        print("Check unit for accurate spelling")

def getWeatherType(): #returns Ex. Cloudy, mostly cloudy
    return weatherSoup.find(class_="today_nowcard-phrase").get_text()

def getTable(): #return values with american units coresponding with the RIGHT NOW table on the website
    for obj in weatherSoup.find_all(class_="today_nowcard-sidecar component panel"):
        return str(obj.get_text())

def getWind(unit): #returns wind direction and wind speed, unit: mph or kmh
    if unit == "mph":
        return str(getTable()[13:getTable().index("Hum")])
    elif unit == "kmh":
        return getTable()[13:16] + str(round(int(re.sub("\D", "", str(getTable()[13:getTable().index("mph")])))*1.609)) + " km/h" #gets wind speed in kmh

def getHum(): #returns humidity value
    return getTable()[getTable().index("Humidity")+8:getTable().index("Dew")]

def getDewPoint(unit): #returns dew point value, unit: celsius or fahrenheit
    if unit == "celsius":
        return round((int(getTable()[getTable().index("Point")+5:getTable().index("Pressure")-1])-32)*5/9)
    elif unit == "fahrenheit":
        return getTable()[getTable().index("Point")+5:getTable().index("Pressure")-1]
    else:
        print("Check unit for accurate spelling")