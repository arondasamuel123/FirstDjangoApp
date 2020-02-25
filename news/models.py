from django.db import models

class Editor(models.Model):
    first_name = models.CharField(max_length =30)
    last_name = models.CharField(max_length= 30)
    email = models.EmailField()
    
    def __str__(self):
        return self.first_name
    def save_editor(self):
        self.save()
    
    def delete_editor(self):
        self.delete()
    
    class Meta:
        ordering = ['first_name']
    
class Tag(models.Model):
    name = models.CharField(max_length = 30)
    
    
    def __str__(self):
        return self.name
    
class Article(models.Model):
    title = models.CharField(max_length=60)
    editor = models.ForeignKey(Editor,on_delete=models.CASCADE)
    post = models.TextField()
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    
    
