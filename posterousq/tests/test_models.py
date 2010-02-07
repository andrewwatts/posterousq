
from datetime import datetime
from django import test
from tagging.models import Tag

from posterousq.models import Post

class BaseTestCase(test.TestCase):
    def assertTagsEqual(self, qs, tags):
        names = map(lambda tag: tag.name, qs)
        names.sort()
        tags.sort()
        self.assertEqual(names, tags)
        
        
class PostTestCase(BaseTestCase):
    fixtures = ['posterousq/test_posts.json']
    
    def test_create_post(self):
        # test create post
        title = 'Day 002: The Golden Filter - The Hardest Button To Button'
        post = Post.objects.create(title=title,
                                   body='',
                                   timestamp=datetime.utcnow())
        self.assertEqual(Post.objects.all().count(), 2)
        self.assertEqual(post.title, title)

        # test tags
        tags = Tag.objects.get_for_object(post)
        self.assertTagsEqual(tags, [])
        post.tags = '365, cover, electronic, mp3'
        post.save()
        tags = Tag.objects.get_for_object(post)
        self.assertTagsEqual(tags, ['365', 'cover', 'electronic', 'mp3'])
        
    def test_read_post(self):
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, 'Day 001: The Walkmen - In The New Year')
        
    def test_update_post(self):
        title = 'Day 001: The Rural Alberta Advantage - Eye Of The Tiger'
        post = Post.objects.get(pk=1)
        post.title = title
        post.save()
        post = Post.objects.get(pk=1)
        self.assertEqual(post.title, title)
        
    def test_delete_post(self):
        post = Post.objects.get(pk=1)
        post.delete()
        self.assertEqual(Post.objects.all().count(), 0)
        
        
class QueuedPostTestCase(BaseTestCase):
    fixtures = ['posterousq/test_posts.json']
    
    def test_read_all_queued_posts(self):
        self.assertEqual(Post.queued_objects.all().count(), 1)
        
    def test_read_not_queued_posts(self):
        post = Post.objects.get(pk=1)
        post.queued = False
        post.save()
        self.assertEqual(Post.queued_objects.all().count(), 0)
        