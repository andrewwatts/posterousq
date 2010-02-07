
from django.db import models


class QueuedPostManager(models.Manager):
    '''Manager for posts that have been Queued'''
    
    def get_query_set(self):
        return super(QueuedPostManager, self).get_query_set().filter(queued=True)
    