
from django import forms
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _

class PostSplitDateTimeWidget(forms.SplitDateTimeWidget):
    '''A SplitDateTime Widget that has specific styling for posts'''
    
    def __init__(self, attrs=None):
        super(PostSplitDateTimeWidget, self).__init__(attrs)
        
    def format_output(self, rendered_widgets):
        return mark_safe(
            u'<div>%s<br/>%s<br/>%s<br/>%s</div>' % \
            (_('Date: '), rendered_widgets[0], _('Time: '), rendered_widgets[1])
        )