from lxml import html
import requests
"""needs update"""
page = requests.get("https://weather.com/weather/today/l/PLXX0012:1:PL")
tree = html.fromstring(page.text)
temp = tree.xpath('//div[@clsudo apt-get install python-lxmlass="today_nowcard-temp"]//span[@class]/text()')

page1 = requests.get("https://pogoda.interia.pl/prognoza-szczegolowa-krakow,cId,4970")
tree1 = html.fromstring(page1.text)
opis = tree1.xpath('//div[@class="weather-currently-middle-pollution-right"]//div[@class="desc"]/text()')
wartosc = tree1.xpath('//div[@class="weather-currently-middle-pollution-right"]//div[@class="value"]/text()')

print ("Aktualna temperatura w Krakowie to ", float(temp[0])-40, "C")
z = str(wartosc[1]).replace("% normy", "")

for i in range(3):
    print (opis[i],"=",wartosc[i])

z = str(wartosc[1]).replace("% normy", "")
h=int(z)*50/100
print ("pm10 =", h)

z1 = str(wartosc[2]).replace("% normy", "")
h1=int(z1)*50/100
print ("pm25 =", h1)
input()