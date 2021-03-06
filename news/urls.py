from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views 

urlpatterns = [
    path('', views.news_of_the_day, name='newsToday'),
    path('archives/<str:past_date>',views.past_days_news, name='pastNews'),
    path('search/', views.search_results, name='search_results'),
    path('article/<int:article_id>',views.article, name='article'),
    path('new/article', views.new_article, name='new-article'),
    path('ajax/newsletter/', views.newsletter, name='newsletter'),
    path('api/merch', views.MerchList.as_view()),
    path('api/merch/<int:pk>', views.MerchDescription.as_view()),
    path('logout/', views.logout_view, name='logout')
    
]
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)