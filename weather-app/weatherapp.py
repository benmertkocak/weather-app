from tkinter import *
from PIL import ImageTk,Image
import geocoder
import requests

url = 'http://api.openweathermap.org/data/2.5/weather'
api_key = 'YOUR_API_KEY'
iconURl =  'http://openweathermap.org/img/wn/{}@2x.png'

def getWeather(city):
    params = {'q':city, 'appid':api_key,'lang':'tr'}
    data = requests.get(url,params=params).json()
    if data:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp'] - 273.15)
        icon = data['weather'][0]['icon']
        condition = data['weather'][0]['description']
        return (city,country,temp,icon,condition)

def search():
    city = cityEntry.get()
    weather = getWeather(city)
    if weather:
        locationLabel['text'] = '{},{}'.format(weather[0],weather[1])
        tempLabel['text'] = '{}°C'.format(weather[2])
        conditionLabel['text'] = weather[4]
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconURl.format(weather[3]),stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon

def main():
    g = geocoder.ip('me')
    lat, lng = g.latlng
    params = {'lat': lat, 'lon': lng, 'appid': api_key, 'lang': 'tr'}
    data = requests.get(url, params=params).json()
    if data:
        city = data['name'].capitalize()
        country = data['sys']['country']
        temp = int(data['main']['temp'] - 273.15)
        icon = data['weather'][0]['icon']
        condition = data['weather'][0]['description']
        locationLabel['text'] = '{},{}'.format(city, country)
        tempLabel['text'] = '{}°C'.format(temp)
        conditionLabel['text'] = condition
        icon = ImageTk.PhotoImage(Image.open(requests.get(iconURl.format(icon), stream=True).raw))
        iconLabel.configure(image=icon)
        iconLabel.image = icon

app = Tk()
app.geometry('325x510')
app.title('Hava Durumu')
app.configure(bg='lightblue')

cityEntry = Entry(app,justify='center') 
cityEntry.pack(fill=BOTH,ipady=10,padx=18,pady=5)
cityEntry.focus()

useLocationButton = Button(app, text='Arama', font=('Arial', 15), command=search, bg='#bfe5df')
useLocationButton.pack(fill=BOTH, ipady=10, padx=20)

searchButton = Button(app,text='Konum Kullanarak Bul', font=('Arial',15),command=main, bg='#bfe5df')
searchButton.pack(fill=BOTH,ipady=10,padx=20)


iconLabel = Label(app, bg='lightblue')
iconLabel.pack()

locationLabel = Label(app,font=('Arial',40), bg='lightblue')
locationLabel.pack()

tempLabel = Label(app,font=('Arial',40,'bold'), bg='lightblue')
tempLabel.pack()

conditionLabel = Label(app,font=('Arial',20), bg='lightblue')
conditionLabel.pack() 

app.mainloop()
