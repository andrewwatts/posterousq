
import os
from django.conf import settings
from django.test import TestCase

from posterousq.tasks import PostTask
from posterousq.models import Post

class PublishPostTestCase(TestCase):
    
    def setUp(self):
        self.uploaded_media_filename = '20100205-the_rural_alberta_advantage-eye_of_the_tiger-cover-survivor.mp3'
        media = open(os.path.join(os.path.dirname(__file__), 'media', self.uploaded_media_filename))
        data = {
            "title": "Day 036: The Rural Alberta Advantage - Eye Of The Tiger",
            "body": "When I started this, I never expected The Rural Alberta Advantage to be the first band posted twice, but I like this cover of Eye Of The Tiger.",
            "media": media,
            "timestamp_0": "2010-02-07",
            "timestamp_1": "04:49:21",
            "tags": "365 mp3 indie cover",
            "autopost": False
        }
        response = self.client.post('/post', data)
        media.close()
    
    def tearDown(self):
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, 'posterousq', 'uploads', self.uploaded_media_filename)
        if os.path.isfile(uploaded_file_path):
            os.remove(uploaded_file_path)
    
    def test_publish_post(self):
        result = PostTask.delay()
        self.assertEquals(result.get(), 1)
        self.assertTrue(result.successful())
        self.assertEquals(len(Post.queued_objects.all()), 0)
        