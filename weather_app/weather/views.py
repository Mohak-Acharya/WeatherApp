from django.shortcuts import render, redirect
from .models import City
import requests
from .forms import cityform

# Create your views here.
def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=2dde4769ad053e986686e99feefcb489'
    # city = 'Las Vegas'
    cities = City.objects.all()

    msg=''
    message=''
    message_class=''

    if request.method=='POST':
        form = cityform(request.POST)

        if form.is_valid():
            newcity = form.cleaned_data['name']
            if City.objects.filter(name=newcity).count() == 0:
                r = requests.get(url.format(newcity)).json()
                if r['cod'] == 200:
                    form.save()
                else:
                    msg = 'Please enter a valid city name!'
            else:
                msg='City already exists in database!'
    
        if msg:
            message = msg
            message_class = 'is-danger'
        else:
            message='City added successfully!'
            message_class='is-success'
        
    form = cityform()

    weather_data = []
    for city in cities: 
        r = requests.get(url.format(city)).json()
        city_weather = {

            'city' : city.name,
            'temp' : r['main']['temp'],
            'desc' : r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        weather_data.append(city_weather)
    # print(city_weather)

    return render(request, 'weather/weather_base.html', context={'weather_data' : weather_data, 'form' : form, 'message' : message, 'message_class':message_class })

def delete(req,city_name):
    City.objects.get(name=city_name).delete()
    return redirect('weather-home')

