.. -*- rst -*-

=======
Weather
=======

The weather app is a very simple demonstration of programmatically altered
animated SVG. It provides a small animation of rain and clouds against a
backdrop with the level of clouds and the appearance of the rain user
adjustable.

To achieve this, the image contains all elements that can appear in the final
animation, but most elements are initially hidden. The server side code simply
loads the SVG as an XML file, unhides the requested elements and sends the
resulting SVG back to the client.

The image was drawn in Inkscape and two versions of it are included in the
source: image.svg is the original image, and image_optimized.svg is a version
of the picture with greatly simplified structure and all editor specific tags
removed (cuts the size down from about 300k to 80k even before compression).

The webapp itself is written with the Pyramid framework and can be run locally
if you wish to have a play with the code. Installation instructions are
included below.

Development Installation
========================

Requirements:

 * `Inkscape <http://inkscape.org>`_ (if you wish to edit the image)
 * `Python 2.6+ <http://python.org>`_ (untested on Python 3.x but *might* run)
 * `Python virtualenv <http://www.virtualenv.org/en/latest/>`_
 * `Git <http://git-scm.com/>`_

Instructions::

    # Create a virtualenv to play with
    $ virtualenv --no-site-packages weatherenv

    # Clone the git repo
    $ git clone git://github.com/waveform80/weather.git

    # Activate the previously created virtualenv
    $ source weatherenv/bin/activate

    # Install the application into the vitualenv as a development version
    (weatherenv)$ cd weather
    (weatherenv)$ python setup.py develop

    # Run the application with the development configuration (which will
    # include the debugging toolbar) and automatic reloading of updated
    # modules (to allow live manipulation)
    (weatherenv)$ pserve development.ini --reload

At this point you should have a development copy running locally and you should
be able to visit http://localhost:8080/ to see it. The ``--reload`` option
means that you can edit the code while the server is running and it should
automatically reload the changed modules (although if the newly saved code
doesn't parse correctly you'll most likely find pserve crashes out).

Deployment on Apache
====================

To deploy this application on apache, firstly install the following
pre-requisites:

 * `Python 2.6+ <http://python.org>`_ (untested on Python 3.x but *might* run)
 * `Python virtualenv <http://www.virtualenv.org/en/latest/>`_
 * `Git <http://git-scm.com/>`_
 * `Apache 2.x <http://httpd.apache.org/>`_
 * `mod_wsgi <http://code.google.com/p/modwsgi/>`_

The following these instructions (and yes, you really need to clone the git
repo within the virtualenv - I've no idea why but for some reason it doesn't
work otherwise)::

    # Create a virtualenv to contain the code
    $ virtualenv --no-site-packages weatherenv

    # Clone the git repo into the virtualenv
    $ cd weatherenv
    $ git clone git://github.com/waveform80/weather.git

    # Activate the virtualenv
    $ source ../bin/activate

    # Install the application into the vitualenv
    (weatherenv)$ cd weather
    (weatherenv)$ python setup.py install

Now, in the weatherenv directory that was created by virtualenv, create an
executable weather.wsgi script with the following contents (adjust the path as
necessary)::

    ini_path = '/path/to/weatherenv/weather/production.ini'
    setup_logging(ini_path)
    application = get_app(ini_path, 'main')

Add the following to the relevant Apache config (again, adjust paths as
necessary)::

    WSGIApplicationGroup %{GLOBAL}
    WSGIPassAuthorization On
    WSGIDaemonProcess weather user=dave group=dave threads=4 python-path=/path/to/weatherenv/lib/python2.7/site-packages
    WSGIScriptAlias /weather /path/to/weatherenv/weather.wsgi
    <Directory /path/to/weatherenv>
        WSGIProcessGroup weather
        Order allow,deny
        Allow from all
    </Directory>

Finally, reload the Apache service and visit /weather on the relevant site::

    $ sudo service apache2 reload

