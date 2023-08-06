=====
wtb-fincharts
=====

Wtb-fincharts is a app to create pie charts of weekly and monthly transactions.

Quick start
-----------

1. Add "wtb-fincharts" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wtb-fincharts',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('wtb-fincharts/', include('charts.urls')),

3. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

4. Visit http://127.0.0.1:8000/charts/weekly to view pie charts of weekly and monthly transactions.