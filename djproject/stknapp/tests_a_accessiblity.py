from django.test import TestCase, Client
from stknapp.models import FileInfo
from django.urls import reverse

class AccessibilityTestCase(TestCase):
    def setUp(self):
        # тут ничего не готовим
        pass

    def test_empty_database(self):
        self.assertEqual(FileInfo.objects.all().count(), 0)

    def test_empty_pages(self):
        response = self.client.get(reverse('pagetop', args=(10,)))
        self.assertContains(response, "No PDFs found.") # default test db contains no files
    

    def test_all_pages_exist(self):
        c = Client()
        pages = ['imgtop', 'sizetop', 'extstats', 'pagetop']
        for page in pages:
            response = self.client.get(reverse(page, args=(10,)))
            self.assertEqual(response.status_code, 200)
        response2 = self.client.get(reverse('index'))
        self.assertEqual(response2.status_code, 200)
        
        