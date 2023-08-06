ngits-tickets
=============

Base `tickets` application for Django projects

Setup
-----

1. Install using pip:
~~~~~~~~~~~~~~~~~~~~~

::

       pip install ngits-tickets

2. Change your ``settings`` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

        INSTALLED_APPS = [
            ...
            "rest_framework",
            "rest_framework.authtoken",
            "tickets"
        ]

        ...

        REST_FRAMEWORK = {
            "DEFAULT_AUTHENTICATION_CLASSES": [
                "rest_framework.authentication.TokenAuthentication",
            ],
            # Optional path to custom TextChoices class
            "DEFAULT_SCHEMA_CLASS": "myapp.consts.MyTypes",
        }

       ...

        # Optional
        TYPE_CHOICES_PATH = "path.to.MyCustomTypeChoices"

3. Create custom ticket types (optional):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``./consts.py``

::

        from django.db.model import TextChoices

        class MyTypes(TextChoices):
            foo = "foo"
            bar = "bar"

4. Add paths to your `urls.py` file:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       from django.urls import path, include

       urlpatterns = [
           ...
           path("/", include("tickets.urls")),
       ]

5. Run migrations:
~~~~~~~~~~~~~~~~~~

::

       py manage.py migrate


6. Optional `redoc` configuration:
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

       pip install drf-spectacular==0.23.*

``settings.py``:

::

       INSTALLED_APPS = [
           ...
           "drf_spectacular"
       ]

       SPECTACULAR_SETTINGS = {
           "TITLE": "<proj_name> API",
           "VERSION": "1.0.0",
       }

       TEMPLATES = [
           ...
           'DIRS': [ BASE_DIR / "templates"],
           ...
       ]

``../<django_project>/templates/redoc.html``:

::

       <!DOCTYPE html>
       <html>
           <head>
               <title>ReDoc</title>
               <!-- needed for adaptive design -->
               <meta charset="utf-8"/>
               <meta name="viewport" content="width=device-width, initial-scale=1">
               <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
               <!-- ReDoc doesn't change outer page styles -->
               <style>
                   body {
                       margin: 0;
                       padding: 0;
                   }
               </style>
           </head>
           <body>
               <redoc spec-url='{% url schema_url %}'></redoc>
               <script src="https://cdn.jsdelivr.net/npm/redoc@next/bundles/redoc.standalone.js"> </script>
           </body>
       </html>
