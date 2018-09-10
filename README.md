# CS50 CRM

CRM Project for HarvardX's CS50 course

## About

The app lets users keep track of clients demand for quotation, from the initial demand to the offer, up until the actual order.

It allows users to:
* Register
* To log in / logout
* Create a new client
* Create / Edit a project
* View all projects and filter by statuses (open, offered, ordered)
* View statistics (Global and per client number of projects that are open / offered / ordered, conversion rates and mean value of offers / orders)

Coming soon:
* View cancelled projects
* Delete a project
* See late open projects 

## Getting Started

* Clone the repository
* Install the required packages with "pip install -r requirements.txt"
* Set the environment variable FLASK_APP to "application.py"
* Set a SECRET_KEY environment variable
* Start the Development Server with "flask run"
* Login with (Username: **admin**, Password: **admin**)

## Built With

* [Python](https://www.python.org/)
* [Flask](http://flask.pocoo.org/) - The web framework used
* [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database

## Authors

* **Nicolas AMBRY** - *Initial work* - [AmbryN](https://github.com/AmbryN)