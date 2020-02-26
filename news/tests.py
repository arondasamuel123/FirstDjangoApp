from django.test import TestCase
from .models import Editor, Article,Tag
import datetime as dt

class EditorTestClass(TestCase):
    def setUp(self):
        self.sam = Editor(first_name='Samuel', last_name='Aronda', email='samuel@moringaschool.com')
        
    def test_instance(self):
        self.assertTrue(isinstance(self.sam, Editor))
        
    def test_save_method(self):
        self.sam.save_editor()
        editors = Editor.objects.all()
        self.assertTrue(len(editors) > 0)
        
    # def test_geteditors_method(self):
    #     eds= self.get_editors()
    #     self.assertEquals(len(editors) == 1)
        
    def test_delete_method(self):
        self.sam.save_editor()
        self.sam.delete_editor()
        editors = Editor.objects.all()
        
        self.assertTrue(len(editors) == 0)
        
        
class ArticleTestClass(TestCase):
    
    def setUp(self):
        self.james= Editor(first_name = 'James', last_name ='Muriuki', email ='james@moringaschool.com')
        self.james.save_editor()
        
        self.new_tag = Tag(name='testing')
        self.new_tag.save()
        
        self.new_article = Article(title= 'Test Article post', post='This is random test post', editor = self.james)
        self.new_article.save()
        
        
        self.new_article.tags.add(self.new_tag)
    
    def tearDown(self):
        Editor.objects.all().delete()
        Tag.objects.all().delete()
        Article.objects.all().delete()
        
        
    def test_get_news(self):
        today_news = Article.today_news()
        self.assertTrue(len(today_news)> 0)
    
    def test_get_news_by_date(self):
        test_date = '2017-03-17'
        date = dt.datetime.strptime(test_date, '%Y-%m-%d').date()
        news_by_date = Article.days_news(date)
        self.assertTrue(len(news_by_date) == 0)
    


