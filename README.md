A Post Queue for Publishing at Posterous
=========================================

A Django Project to Queue Posts for Publishing at [Posterous][].

Getting Started
----------------

1. grab the code

        git clone http://github.com/andrewwatts/posterousq.git
        cd posterousq

2. Create a [virtualenv][] (with [virtualenvwrapper][])

        mkvirtualenv posterousq
        workon posterousq
        easy_install pip
        
3. Install dependencies

        pip install -r requirements/requirements.txt
        
4. Configure your settings, an example `settings.py` is included in 
   `settings.py.sample`, copy it to `settings.py` before editing:

        cd posterousq
        cp settings.py.sample settings.py
   At a minimum you'll need to define your posterous username (email address)
   and password, and if you have more than one site, and do not want your
   posts going to your default site, the site id.
   
        POSTEROUS_USERNAME = 'yourname@emailaddress.com'
        POSTEROUS_PASSWORD = 'yourpassword'
        POSTEROUS_SITE_ID = 'optional_site_id'
   and modify your database settings appropriately for your database
   configuration
   
        DATABASE_ENGINE = 'sqllite3'
        DATABASE_NAME = 'posterousq.db'             
        DATABASE_USER = ''             
        DATABASE_PASSWORD = ''         
        DATABASE_HOST = ''             
        DATABASE_PORT = ''   

5. Install and/or sync your database

        cd ..
        ./manage.py syncdb
        
6. Run the celeryd workers, scheduler and server in your environment, for 
   development these commands can be used.

        ./manage.py celeryd -B
        ./manage.py runserver
   For more formal deployment options, you're on your own, but there are 
   plenty of howto's in the [celery cookbook][] and [django docs][]. And 
   remember you could be dealing with some large files, so you'll need to
   configure the webserver properly to handle large file uploads.



[posterous]: http://posterous.com
[celery cookbook]: http://ask.github.com/celery/cookbook/daemonizing.html
[django docs]: http://docs.djangoproject.com/en/dev/howto/deployment/
[virtualenv]: http://pypi.python.org/pypi/virtualenv
[virtualenvwrapper]: http://www.doughellmann.com/projects/virtualenvwrapper/
