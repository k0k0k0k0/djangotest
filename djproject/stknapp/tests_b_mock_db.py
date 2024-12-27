from django.test import TestCase
from django.urls import reverse
from .models import FileInfo


class FileInfoTests(TestCase):
    def setUp(self):
        # сделаем каких-нибудь объектов и добавим в базу
        FileInfo.objects.create(extension="jpg", size=1024, IMG_size=500, PDF_num_pages=None)
        FileInfo.objects.create(extension="png", size=2048, IMG_size=600, PDF_num_pages=None)
        FileInfo.objects.create(extension="pdf", size=4096, IMG_size=None, PDF_num_pages=10)

    def test_extstats_view(self):
        response = self.client.get(reverse('extstats', args=[3]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "jpg")
        self.assertContains(response, "png")
    
    def test_sizetop_view(self):
        response = self.client.get(reverse('sizetop', args=[2]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "4096")  # будет самый большой
        self.assertNotContains(response, "1024")  # а маленького быть не должно, потмоу что 2

    def test_imgtop_view(self):
        response = self.client.get(reverse('imgtop', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "600") 
    
    def test_pagetop_view(self):
        response = self.client.get(reverse('pagetop', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10")

    def test_indexview_get(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<strong>Total File Size:</strong> 0,01 GB")
    
    def test_indexview_post_clear_db(self):
        response = self.client.post(reverse('index'), {'clear_db': 'true'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Database cleared successfully!")
        self.assertEqual(FileInfo.objects.count(), 0)