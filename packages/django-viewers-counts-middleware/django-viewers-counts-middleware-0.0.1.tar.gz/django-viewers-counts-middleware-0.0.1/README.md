
Django Viewers Count Middleware
================================

Viewers Count is a Django app to collect visitors request counts with path.

Detailed documentation.

Quick start
-----------

1. Add "viewers_count" to your INSTALLED_APPS setting like this::


    INSTALLED_APPS = [

        ...
        'viewers_count',


    ]


2. Add "ViewerCountMiddleware" to your INSTALLED_APPS setting like this::


    MIDDLEWARE = [

    	...
        'viewers_count.middleware.ViewersCountMiddleware',


    ]
    

3. Run to create the viewerscount models.


        python manage.py migrate


