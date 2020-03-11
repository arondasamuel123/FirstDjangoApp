from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Article, NewsRecipients
import datetime as dt
from .forms import NewsLetterForm,RegisterForm, NewsArticleForm
from .email import send_welcome_email
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .models import MoringaMerch
from .serializer import MerchSerializer
from .permissions import IsAdminOrReadOnly
def welcome(request):
    return render(request, 'welcome.html')


def news_of_the_day(request):
    date = dt.date.today()
    news = Article.today_news()
    form = NewsLetterForm()
    
    # if request.method == 'POST':
    #     form = NewsLetterForm(request.POST)
    #     if form.is_valid():
    #         name = form.cleaned_data['your_name']
    #         email = form.cleaned_data['email']
    #         recipient = NewsRecipients.objects.create(name= name,email= email)
    #         recipient.save()
    #         send_welcome_email(name,email)
    #         HttpResponseRedirect('news_today')
    # else:
    #         form = NewsLetterForm()
    
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
@login_required(login_url='/accounts/login')    
def article(request, article_id):
    try:
        article = Article.objects.get(id= article_id)
    except DoesNotExist:
        raise Http404()
    return render(request, "all-news/article.html", {"article":article})

def signup(request):
    if request.method =='POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created')
            return redirect(news_of_the_day)
            
    else:
        form = RegisterForm()
    return(request, 'django_registration/registration_form.html',{"form":form})

def login(request):
    if request.method=='POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['Username']
            password = form.cleaned_data['password']
            
            user = authenticate(username, password)
            if user:
                if user.is_active:
                    login(request,user)
                    return redirect(news_of_the_day)
                else:
                    return HttpResponse("Your account is inactive")
    else:
        form = AuthenticationForm()
        
    return render(request,'registration/login.html', {"form":form})
@login_required(login_url='/accounts/login/')
def new_article(request):
    current_user = request.user
    if request.method == 'POST':
        form = NewsArticleForm(request.POST,request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.editor = current_user
            article.save()
            return redirect(news_of_the_day)
    else:
        form = NewsArticleForm()
    return render(request, 'new_article.html', {"form":form})

def newsletter(request):
    name = request.POST.get('your_name')
    email = request.POST.get('email')
    
    recipient = NewsRecipients(name=name, email=email)
    recipient.save()
    send_welcome_email(name, email)
    data = {'success':'You have been successfully added to mailing list'}
    return JsonResponse(data)

class MerchList(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    def get(self, request, format=None):
        all_merch = MoringaMerch.objects.all()
        serializers = MerchSerializer(all_merch, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = MerchSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
class MerchDescription(APIView):
    permission_classes = (IsAdminOrReadOnly,)
    
    def get_merch(self,pk):
        try:
            return MoringaMerch.objects.get(pk=pk)
        except MoringaMerch.DoesNotExist:
            return Http404   
    def get(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch)
        return  Response(serializers.data)
    
    def put(self, request, pk, format=None):
        merch = self.get_merch(pk)
        serializers = MerchSerializer(merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    def delete(self, request,pk, format=None):
        merch = self.get_merch(pk)
        merch.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        
    

def logout_view(request):
    logout(request)
    
    return redirect(news_of_the_day)


            


