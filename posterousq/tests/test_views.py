
import os

from django import test
from django.conf import settings
from django.utils import simplejson

class CreatePostTestCase(test.TestCase):
    
    def setUp(self):
        self.uploaded_media_filename = '20100205-the_rural_alberta_advantage-eye_of_the_tiger-cover-survivor.mp3'
        
    def tearDown(self):
        uploaded_file_path = os.path.join(settings.MEDIA_ROOT, 'posterousq', 'uploads', self.uploaded_media_filename)
        if os.path.isfile(uploaded_file_path):
            os.remove(uploaded_file_path)

    def test_get_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        
    def test_get_form(self):
        response = self.client.get('/form', {})
        self.assertEqual(response.status_code, 200)
        
    def test_blank_form(self):
        response = self.client.post('/post', {})
        # required fields will fail
        self.assertEquals(response.status_code, 400)
        
    def test_valid_form(self):
        data = {
            "title": "Day 036: The Rural Alberta Advantage - Eye Of The Tiger",
            "body": "When I started this, I never expected The Rural Alberta Advantage to be the first band posted twice, but I like this cover of Eye Of The Tiger.",
            "timestamp_0": "2010-02-07",
            "timestamp_1": "04:49:21",
            "tags": "365 mp3 indie cover",
        }
        response = self.client.post('/post', data)
        self.assertEqual(response.status_code, 201)
        
    def test_media_upload_form(self):
        media = open(os.path.join(os.path.dirname(__file__), 'media', self.uploaded_media_filename))
        data = {
            "title": "Day 036: The Rural Alberta Advantage - Eye Of The Tiger",
            "body": "When I started this, I never expected The Rural Alberta Advantage to be the first band posted twice, but I like this cover of Eye Of The Tiger.",
            "media": media,
            "timestamp_0": "2010-02-07",
            "timestamp_1": "04:49:21",
            "tags": "365 mp3 indie cover",
        }
        response = self.client.post('/post', data)
        media.close()
        self.assertEqual(response.status_code, 201)


class ReadPostTestCase(test.TestCase):
    fixtures = ['posterousq/test_posts.json']

    def test_get_post(self):
        response = self.client.get('/post/1')
        post = simplejson.loads(response.content)['data'][0]['fields']
        self.assertEqual(post['title'], 'Day 001: The Walkmen - In The New Year')
        
    def test_get_post_not_found(self):
        response = self.client.get('/post/100')
        self.assertEqual(response.status_code, 404)
        
    def test_get_all_posts(self):
        response = self.client.get('/post')
        response = simplejson.loads(response.content)['data']
        self.assertEqual(len(response), 1)
        
    
class DeletePostTestCase(test.TestCase):
    fixtures = ['posterousq/test_posts.json']
        
    def test_delete_post(self):
        response = self.client.delete('/post/1')
        self.assertEquals(response.status_code, 204)
        
    def test_delete_post_not_found(self):
        response = self.client.delete('/post/100')
        self.assertEquals(response.status_code, 404)
        
        
class UpdatePostTestCase(test.TestCase):
    fixtures = ['posterousq/test_posts.json']
    
    def test_get_populated_form(self):
        response = self.client.get('/post/1')
        self.assertEqual(response.status_code, 200)
        
    def test_update_post(self):
        response = self.client.get('/post/1')
        response = simplejson.loads(response.content)['data'][0]['fields']
        data = {
            "title": response['title'],
            "body": response['body'],
            "timestamp_0": response['timestamp'].split()[0],
            "timestamp_1": response['timestamp'].split()[1],
            "tags": "365 mp3 indie",
        }
        response = self.client.put('/post/1', data)
        self.assertEquals(response.status_code, 200)
        response = self.client.get('/post/1')
        post = simplejson.loads(response.content)['data'][0]['fields']
        self.assertEquals(post['tags'], '365 mp3 indie')
        
    def test_update_post_not_found(self):
        response = self.client.put('/post/100', {})
        self.assertEquals(response.status_code, 404)