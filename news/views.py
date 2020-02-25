from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
import datetime as dt

def welcome(request):
    return render(request, 'welcome.html')


def news_of_the_day(request):
    date = dt.date.today()
    day = convert_dates(date)
    html = f'''
        <html>
        <body>
            <h1>News for {day} {date.day}- {date.month}- {date.year}</h1>
        </body>
        </html>
        '''
    return render(request, 'all-news/today-news.html', {"date":date})
def convert_dates(dates):
    
    day_number = dt.date.weekday(dates)
    
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day = days[day_number]
    return day


def past_days_news(request, past_date):
    try:
    # Converts data from the string Url
        date = dt.datetime.strptime(past_date,'%Y-%m-%d').date()

    except ValueError:
        raise Http404
    if date == dt.date.today():
        return redirect(news_of_the_day)

    day = convert_dates(date)
    html = f'''
        <html>
        <body>
            <h1>News for {day} {date.day}- {date.month}- {date.year}</h1>
        </body>
        </html>
            '''
    return render(request, 'all-news/past-news.html', {"date":date})
        
    

    