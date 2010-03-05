
import base64
import logging
import os
import urllib2

from datetime import datetime
from datetime import timedelta
from django.conf import settings
from celery.task import PeriodicTask
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
    
from posterousq.libs import simplexml
from posterousq.models import Post
    

class PostTask(PeriodicTask):
    '''a task that to look for new posts and if found sends them to posterous'''
    
    run_every = timedelta(seconds=60)
    
    DATE_FORMAT = '%Y-%m-%d'
    TIME_FORMAT = '%H:%M:%S'
    NEW_POST_URL = 'http://posterous.com/api/newpost'

    def run(self, **kwargs):
        
        posted_count = 0
        
        # Register the streaming http handlers with urllib2
        register_openers()
        
        queued_posts = Post.queued_objects.filter(timestamp__lte=datetime.utcnow())
        for post in queued_posts:
            site_id = settings.POSTEROUS_SITE_ID or None
            data = {
                "site_id": site_id,
                "title": post.title,
                "body": post.body,
                "autopost": int(post.autopost),
                "private": int(post.private),
                "timestamp": post.timestamp.strftime('%s %s' % (self.DATE_FORMAT, self.TIME_FORMAT)),
                "media": open(os.path.join(settings.MEDIA_ROOT, post.media.path), 'rb'),
                "source": "Posterous Q",
                "sourceLink": "http://github.com/andrewwatts/posterousq"
            }
            # headers contains the necessary Content-Type and Content-Length
            # datagen is a generator object that yields the encoded parameters
            datagen, headers = multipart_encode(data)
            request = urllib2.Request(self.NEW_POST_URL, datagen, headers)
            
            credentials = base64.encodestring('%s:%s' % (settings.POSTEROUS_USERNAME, settings.POSTEROUS_PASSWORD))[:-1]
            auth_header = 'Basic %s' % credentials
            request.add_header('Authorization', auth_header)
            
            response = urllib2.urlopen(request).read()
            logging.debug('posterous response:\n\t%s' % response)
            response = simplexml.parsestring(response)
            if response.post.id:
                post.queued = False
                post.save()
                posted_count += 1
        
        return posted_count
    