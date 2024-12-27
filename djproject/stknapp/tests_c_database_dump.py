from django.test import TestCase, Client
from stknapp.models import FileInfo
from django.urls import reverse
from pprint import pprint
from django.conf import settings
from django.core.management import call_command


class DatabaseTestCase(TestCase):
    def setUp(self):
        call_command('loaddata', 'dump.json', format='JSON')
        
        

    def dump_content(self):
        self.assertEqual(FileInfo.objects.all().count(), 9534) # в дампе 9534 записи


    def dump_extstats_view(self):
        response = self.client.get(reverse('extstats', args=[8]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "woff")
        self.assertContains(response, "eot") # там есть редкие расширения
    
    def dump_sizetop_view(self):
        response = self.client.get(reverse('sizetop', args=[10]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "3345") 
        self.assertNotContains(response, "3211")  # по тому же принципу, но на выдаче из дампа

    def dump_imgtop_view(self):
        response = self.client.get(reverse('imgtop', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "9766086") 
    
    def dump_pagetop_view(self):
        response = self.client.get(reverse('pagetop', args=[100]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No PDFs found.") # в дампе нет пдф

    def dump_indexview_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>Total File Size:</strong> 0,14 GB")
    
    def dump_indexview_post_clear_db(self):
        response = self.client.post(reverse('index'), {'clear_db': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Database cleared successfully!")
        self.assertEqual(FileInfo.objects.count(), 0)
        

