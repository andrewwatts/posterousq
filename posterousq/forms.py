
from django import forms
from django.utils.translation import ugettext as _

from posterousq.models import Post
from posterousq.widgets import PostSplitDateTimeWidget


class PostForm(forms.ModelForm):
    
    timestamp = forms.SplitDateTimeField(label=_('Timestamp'), widget=PostSplitDateTimeWidget)

    class Meta:
        model = Post
