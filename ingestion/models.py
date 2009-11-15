import mimetypes
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User, Group


status_choices = (
        ('pending' , 'pending'),
        ('uploaded' , 'uploaded'),
        ('available' , 'available'),
        )
license_choices = (
        ('bsd' , 'bsd'),
        ('cc-a' , 'cca'),
        )
source_choices = (
        ('wms' , 'wms'),
        ('file' , 'file'),
        )
        
mime_choices = ((k,v) for k,v in mimetypes.types_map.items())

    
class Source(models.Model):
    """
    this is a server
    """
    path = models.CharField(max_length=255)
    source_type = models.CharField(max_length=255, choices=source_choices)
    disk_space_bytes = models.CharField(max_length=255, help_text="donated space in GB")
    
    def __unicode__(self): return '%s' % self.path

class Layer(models.Model):
    name = models.CharField(max_length=255)
    guid = models.CharField(max_length=255)
    description = models.TextField()
    uploader = models.ForeignKey(User)
    date_uploaded_utc = models.DateTimeField(null=True, blank=True)
    file_format = models.CharField(max_length=255, choices=mime_choices)
    license = models.CharField(max_length=255, choices=license_choices)
    status = models.CharField(max_length=255, choices=status_choices)
    source = models.ForeignKey(Source)
    
    def __unicode__(self): return '%s' % self.name
    