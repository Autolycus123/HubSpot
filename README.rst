Hubspot Integration
=====

This is a simple Flask application that integrates `Hubspot`_ APIs.
It authenticates using OAuth and pulls Deals data that is saves in a MongoDB database.

.. _Hubspot: https://legacydocs.hubspot.com/docs/overview

Running the application
----------

Create a virtual environment and activate it

.. code-block:: text

    $ python3 -m virtualenv venv
    $ source venv/bin/activate
..

Install the project requirements using `pip`_:

.. code-block:: text

    $ pip install -r requirements.txt

.. _pip: https://pip.pypa.io/en/stable/getting-started/

Source the .env.sh script to add the required environment variables or add them to
your terminal profile

.. code-block:: text

    $ source .env.sh

..


Start a cron job that periodically runs src/cron_jobs/deals.py or manually run it to
pull the deals data from Hubspot and add them to the database:

.. code-block:: text

    $ python src/cron_jobs/deals.py

..

Run the application

.. code-block:: text

    $ python run.py

..

When you first open the application you will be redirected to Hubspot's OAuth page.
The authorization code Hubspot offers in response after a successful login is then
used to obtain the authorization and refresh tokens. These tokens are saved in the database and used when needed.
All endpoints that perform requests to Hubspot should have the hubspot_session decorator so that the tokens would
refresh whenever Hubspot responds with `EXPIRED_AUTHENTICATION`.