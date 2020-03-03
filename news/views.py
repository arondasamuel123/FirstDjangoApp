from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Article, NewsRecipients
import datetime as dt
from .forms import NewsLetterForm
from .email import send_welcome_email

def welcome(request):
    return render(request, 'welcome.html')


def news_of_the_day(request):
    date = dt.date.today()
    news = Article.today_news()
    
    if request.method == 'POST':
        form = NewsLetterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            recipient = NewsRecipients.objects.create(name= name,email= email)
            recipient.save()
            send_welcome_email(name,email)
            HttpResponseRedirect('news_today')
    else:
            form = NewsLetterForm()
    
    return render(request, 'all-news/today-news.html', {"date":date, "news":news, "letterForm":form})
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

    news = Article.days_news(date)
    return render(request, 'all-news/past-news.html', {"date":date, "news":news})

def search_results(request):
    if 'article' in request.GET and request.GET["article"]:
        search_term = request.GET.get("article")
        searched_articles = Article.search_by_title(search_term)
        message = f"{search_term}"
        return render(request, 'all-news/search.html', {"message":message, "articles": searched_articles})
    
    else:
        message = "You haven't searched for any term"
        return render(request, 'all-news/search.html',{"message":message})
    
def article(request, article_id):
    try:
        article = Article.objects.get(id= article_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-news/article.html", {"article":article})