## /truedat Quality Engine

TdQE is a back-end service developed as part of True Dat project to execute quality rules.

## Getting Started

These instructions will get you a copy of the service up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing

  * Install virtualenv with `pip install virtualenv`
  * Create virtualenv under the project folder with `virtualenv -p python3 venv && source venv/bin/activate`
  * Install dependencies with `pip install -e .`
  * Install dependencies in enviroment develop with `pip install -e .[dev]`
  * Create database: python commands/create_db.py
  * Drop database: python commands/drop_db.py
  * Init migrations: python commands/manage.py db init
  * Create migrations: python commands/manage.py db migrate
  * Upgrade migrations: python commands/manage.py db upgrade
  * Launch server with `python run.py`

## Built With

* [Flask](https://www.palletsprojects.com/p/flask/) - Python micro framework for building web applications
* [Tornado](http://www.tornadoweb.org/) - Tornado is a Python web framework and asynchronous networking library, originally developed at FriendFeed
* [Flask-cors](https://flask-cors.corydolphin.com/) - Cross Origin Resource Sharing ( CORS ) support for Flask
* [healthcheck](https://github.com/Runscope/healthcheck) - Write simple healthcheck functions for your Flask apps.
* [Pyjwt](https://pyjwt.readthedocs.io) - JSON Web Token implementation in Python
* [Requests](http://python-requests.org) - Python HTTP Requests for Humans™ ✨🍰✨
* [Glom](https://glom.readthedocs.io) - Python's nested data operator
* [Hvac](https://github.com/ianunruh/hvac) - Python 2/3 client for HashiCorp Vault
* [Boto3](http://aws.amazon.com/sdk-for-python/) - AWS SDK for Python
* [Gunicorn](http://www.gunicorn.org) - WSGI HTTP Server for UNIX
* [Fabric3](http://fabfile.org) - Pythonic remote execution and deployment

## Authors

* **Bluetab Solutions Group, SL** - *Initial work* - [Bluetab](http://www.bluetab.net)

See also the list of [contributors](https://github.com/bluetab/td-qe) who participated in this project.

## License

This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with this program. If not, see https://www.gnu.org/licenses/.

In order to use this software, it is necessary that, depending on the type of functionality that you want to obtain, it is assembled with other software whose license may be governed by other terms different than the GNU General Public License version 3 or later. In that case, it will be absolutely necessary that, in order to make a correct use of the software to be assembled, you give compliance with the rules of the concrete license (of Free Software or Open Source Software) of use in each case, as well as, where appropriate, obtaining of the permits that are necessary for these appropriate purposes.
