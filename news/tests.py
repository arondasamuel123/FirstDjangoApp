from django.test import TestCase
from .models import Editor, Article,Tag

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


