
from django.db import models
from tagging.fields import TagField

from posterousq.managers import QueuedPostManager


class Post(models.Model):
    '''A post that will be queued and sent to Posterous'''
    
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    tags = TagField()
    autopost = models.BooleanField(default=True)
    private = models.BooleanField(default=False)
    timestamp = models.DateTimeField()
    queued = models.BooleanField(default=True, editable=False)
    # Note: media is last to ensure it is last on the form rendered by the 
    # templates... There appears to be an obscure bug in firefox with file
    # uploads in iframes where form inputs are not sent to the server if they
    # appear in the form after an input of type file is defined.
    media = models.FileField(upload_to='posterousq/uploads', blank=True)
    
    objects = models.Manager()
    queued_objects = QueuedPostManager()
    
    def __unicode__(self):
        return self.title