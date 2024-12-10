from django.db import models
from datetime import datetime

# Create your models here.

class FileInfo(models.Model):
    path = models.CharField(max_length=200)
    extension = models.CharField(max_length=10, null=True, blank=True)
    is_folder = models.BooleanField(null=True)
    size = models.FloatField()
    last_modified = models.DateTimeField(null=True, blank=True)
    created_time = models.DateTimeField(auto_now_add=True)
    is_container = models.BooleanField(null=True, blank=True)
    parent_object = models.CharField(null=True, blank=True, max_length=200)
    within_container = models.BooleanField(null=True)
    Office_last_mod_time = models.DateTimeField(null=True, blank=True)
    Office_last_mod_by = models.CharField(max_length=50, null=True, blank=True)
    XLS_num_sheets = models.IntegerField(null=True, blank=True)
    PDF_num_pages = models.IntegerField(null=True, blank=True)
    PDF_layout = models.CharField(max_length=20, null=True, blank=True)
    MP3_track_title = models.CharField(max_length=100, null=True, blank=True)
    MP3_artist = models.CharField(max_length=100, null=True, blank=True)
    MP3_duration = models.CharField(max_length=10, null=True, blank=True)
    AUD_bitrate = models.CharField(max_length=10, null=True, blank=True)
    IMG_size = models.FloatField(null=True, blank=True)
    IMG_dpi = models.CharField(max_length=10, null=True, blank=True)
    IMG_device = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.path