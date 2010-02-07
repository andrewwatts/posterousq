
from django.db.models.query import QuerySet
from django.db.models import Model
from django.http import HttpResponse
from django.utils import simplejson
from django.utils.functional import Promise
from django.utils.encoding import force_unicode

from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder


class LazyEncoder(DjangoJSONEncoder):
    '''
    a json encoder to handle lazy translation objects, as defined at
    http://docs.djangoproject.com/en/dev/topics/serialization/#id2
    
    '''
    def default(self, obj):
        if isinstance(obj, Promise):
            return force_unicode(obj)
        if isinstance(obj, QuerySet):
            return serializers.serialize('python', obj, ensure_ascii=False)
        if isinstance(obj, Model):
            return serializers.serialize('python', [obj], ensure_ascii=False)
        return super(LazyEncoder, self).default(obj)
    
json_encoder = LazyEncoder(ensure_ascii=False)

def python_to_json(obj):
    '''
    function to serialize django query sets and basic python types like:
    dict, list, tuple, str, int, None, True, False, etc...
    
    '''
    return json_encoder.encode(obj)


class JsonHttpResponse(HttpResponse):
    '''
    a http response wrapper to encode the content into json, as well as
    set the mimetype to 'text/javascript' by default
    
    '''
    def __init__(self, content=None, mimetype='text/javascript', status=None, 
                 content_type=None):
        super(JsonHttpResponse, self).__init__(content=python_to_json(content),
                                               mimetype=mimetype,
                                               status=status,
                                               content_type=content_type)
        
        
def coerce_put_post(request):
    '''
    django doesn't support request.PUT functionality, so this method has been
    borrowed from django-piston.
    
    Notes from django-piston:
    
        Django doesn't particularly understand REST.
        In case we send data over PUT, Django won't
        actually look at the data and load it. We need
        to twist its arm here.

        The try/except abominiation here is due to a bug
        in mod_python. This should fix it.
        
    '''
    if request.method == "PUT":
        try:
            request.method = "POST"
            request._load_post_and_files()
            request.method = "PUT"
        except AttributeError:
            request.META['REQUEST_METHOD'] = 'POST'
            request._load_post_and_files()
            request.META['REQUEST_METHOD'] = 'PUT'
            
        request.PUT = request.POST