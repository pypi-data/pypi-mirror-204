
Quick Start
===========

1. Add "account" to your INSTALLED_APPS setting like this:

    INSTALLED_APPS = [

        ...
        'account',


    ]

2. Include the polls URLconf in your project urls.py like this:
    path('', include('account.urls')),

3. Run ``python manage.py migrate`` to create the user models

4. Start the development server and visit http://127.0.0.1:8000/ to create a new user login register