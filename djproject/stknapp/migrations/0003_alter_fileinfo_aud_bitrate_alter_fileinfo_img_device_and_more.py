# Generated by Django 5.1.3 on 2024-12-09 19:17

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stknapp", "0002_alter_fileinfo_office_last_mod_time_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="fileinfo",
            name="AUD_bitrate",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="IMG_device",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="IMG_dpi",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="IMG_size",
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="MP3_artist",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="MP3_duration",
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="MP3_track_title",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="Office_last_mod_by",
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="PDF_layout",
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="PDF_num_pages",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="fileinfo",
            name="XLS_num_sheets",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
