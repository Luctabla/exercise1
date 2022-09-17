It is a web app made in flask that allows to obtain posts from a third-party API by implementing asynchronous requests with with asyncio and aiohttp libraries.

Documentation
=============

In order to access to the Project's Documentation you can open the index.html file located in /docs/build/html/index.html..

or follow the instructions below

Requirements
************

* Docker
* Docker-Compose

Starting Project
================

Running Server
--------------

   ``docker-compose up``

Go to the Browser ``http://localhost:8000/register`` and create an user.

Running Client
--------------

In order to run the client first make sure the webapp containers are running and then run the following command

``chmod +x ./client.sh``

then run

``./client.sh``