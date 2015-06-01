# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('trees', '0008_notabletree_public_photo_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplementalContent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=200, blank=True)),
                ('subtitle', models.CharField(max_length=255, blank=True)),
                ('slug', models.SlugField(unique=True)),
                ('display_order', models.IntegerField(default=50)),
                ('summary', models.CharField(help_text=b'Used for previews, list presentations, etc.', max_length=255, blank=True)),
                ('article_text', models.TextField(blank=True)),
                ('credit', models.CharField(max_length=255, blank=True)),
                ('license', models.CharField(default=b'CC BY-SA', max_length=20, choices=[(b'CC BY-SA', b'CC Attribution-ShareAlike'), (b'CC BY', b'CC Attribution'), (b'CC BY-NC-SA', b'CC Attribution-NonCommercial-ShareAlike'), (b'Public Domain', b'Public Domain'), (b'Unknown', b'Unknown')])),
                ('copyright_notice', models.CharField(max_length=255, blank=True)),
                ('copyright_notes', models.TextField(help_text=b'Not visible to the public at any time.', blank=True)),
                ('editorial_notes', models.TextField(help_text=b'Not visible to the public at any time.', blank=True)),
                ('workflow_status', models.CharField(default=b'd', max_length=20, choices=[(b'd', b'Draft'), (b'p', b'Pending'), (b'a', b'Approved'), (b'r', b'Rejected'), (b't', b'Testing Only')])),
                ('layout', models.CharField(default=b'T', max_length=1, choices=[(b'T', b'Text'), (b'I', b'Image'), (b'S', b'Sound'), (b'D', b'Document'), (b'U', b'Unknown')])),
                ('photo', models.ImageField(null=True, upload_to=b'supplemental_photos', blank=True)),
                ('photo_title', models.CharField(max_length=100, blank=True)),
                ('photo_caption', models.CharField(max_length=255, blank=True)),
                ('photo_credit', models.CharField(max_length=255, blank=True)),
                ('photo_copyright', models.CharField(max_length=255, blank=True)),
                ('photo_license', models.CharField(default=b'CC BY-SA', max_length=20, choices=[(b'CC BY-SA', b'CC Attribution-ShareAlike'), (b'CC BY', b'CC Attribution'), (b'CC BY-NC-SA', b'CC Attribution-NonCommercial-ShareAlike'), (b'Public Domain', b'Public Domain'), (b'Unknown', b'Unknown')])),
                ('photo_notes', models.TextField(help_text=b'Not visible to the public at any time.', blank=True)),
                ('audio', models.FileField(null=True, upload_to=b'supplemental_audio', blank=True)),
                ('audio_title', models.CharField(max_length=100, blank=True)),
                ('audio_caption', models.CharField(max_length=255, blank=True)),
                ('audio_transcription', models.TextField(blank=True)),
                ('audio_credit', models.CharField(max_length=255, blank=True)),
                ('audio_copyright', models.CharField(max_length=255, blank=True)),
                ('audio_license', models.CharField(default=b'CC BY-SA', max_length=20, choices=[(b'CC BY-SA', b'CC Attribution-ShareAlike'), (b'CC BY', b'CC Attribution'), (b'CC BY-NC-SA', b'CC Attribution-NonCommercial-ShareAlike'), (b'Public Domain', b'Public Domain'), (b'Unknown', b'Unknown')])),
                ('audio_notes', models.TextField(help_text=b'Not visible to the public at any time.', blank=True)),
                ('attached_file', models.FileField(null=True, upload_to=b'supplemental_file', blank=True)),
                ('attached_file_title', models.CharField(max_length=100, blank=True)),
                ('attached_file_caption', models.CharField(max_length=255, blank=True)),
                ('attached_file_type', models.CharField(default=b'none', max_length=20, choices=[(b'pdf', b'PDF'), (b'json', b'JSON'), (b'zip', b'Zip File'), (b'none', b'None')])),
                ('attached_file_credit', models.CharField(max_length=255, blank=True)),
                ('attached_file_copyright', models.CharField(max_length=255, blank=True)),
                ('attached_file_license', models.CharField(default=b'CC BY-SA', max_length=20, choices=[(b'CC BY-SA', b'CC Attribution-ShareAlike'), (b'CC BY', b'CC Attribution'), (b'CC BY-NC-SA', b'CC Attribution-NonCommercial-ShareAlike'), (b'Public Domain', b'Public Domain'), (b'Unknown', b'Unknown')])),
                ('attached_file_notes', models.TextField(help_text=b'Not visible to the public at any time.', blank=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('mod_date', models.DateTimeField(auto_now=True, verbose_name=b'last modified')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
            ],
            options={
                'ordering': ['mod_date'],
            },
        ),
        migrations.AlterField(
            model_name='treephoto',
            name='review_status',
            field=models.CharField(default=b'p', max_length=10, choices=[(b'd', b'Draft'), (b'p', b'Pending'), (b'a', b'Approved'), (b'r', b'Rejected'), (b't', b'Testing Only')]),
        ),
    ]
