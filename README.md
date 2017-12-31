# chisalary

[![Build Status](https://travis-ci.org/bradleygolden/chisalary.svg?branch=master)](https://travis-ci.org/bradleygolden/chisalary)
[![Coverage Status](https://coveralls.io/repos/github/bradleygolden/chisalary/badge.svg?branch=master)](https://coveralls.io/github/bradleygolden/chisalary?branch=master)

chisalary is a simple web server that syncs with Chicago's employee salary database. The web server was created using the
Django framework and is written in python.

I'd recommend checking out the dataset [here](https://data.cityofchicago.org/Administration-Finance/Current-Employee-Names-Salaries-and-Position-Title/xzkq-xp2w/data) before getting started.

## Getting Started

### Prerequisites

* python 3.6
* App token from Chicago Data Portal (Optional)

### Installing

The best way to get chisalary up and running is to clone the repo:
```
git clone https://github.com/bradleygolden/chisalary.git
```

Now cd into the project directory, create a virtual environment, and install
the project requirements.
```
cd chisalary
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Running

Now that you have the project dependencies installed and an environment set up, let's set up the data base.

First create an sqlite3 database and perform migrations:
```
python manage.py migrate
```

Now download some employee salary data:
```
python manage.py download_employees --limit 100  # download 100 employees
# or
APP_TOKEN=<token> python manage.py download_employees  # download all employees
```

You're ready to start the server. Run the server with:
```
python manage.py runserver
```

Go to your browser and visit [localhost:8000/api/](localhost:8000/api).

You can see the employees api by visiting [localhost:8000/api/employees/](localhost:8000/api/employees).

API documentation can be found at [localhost:8000/api/docs/](localhost:8000/api/docs/).

Lastly, the django admin panel is available at [localhost:8000/admin/](localhost:8000/admin/). To gain access to the admin panel you must first create a superuser:
```
python manage.py createsuperuser
```


#### Docker

I've also provided a Docker image as an alternative approach to getting up and running quickly.

You run the server using:
```
docker-compose up
```

After running this command, wait about 20-30 seconds after the images have been built and the server should start up.

#### Make

I've alao added a few make commands:
```
make test # run tests
make run # run dev server
make clean # clean up some junk files
```

## Running Tests

After following the [Getting Started](#Getting Started) instructions, you can run unit tests with the following command:
```
coverage run --source=. chisalary/manage.py test api --noinput
```

## TODO

- [ ] Add asynchronous task queue
    * This is for syncing with the Chicago Data Portal at periodic intervals. This can be done with celery and redis.
- [x] Add CI job for testing code on commit
    * Travis CI is a great choice for this
- [ ] Add CD job for deploying code to a remote a server
    * Any docker based platform like kubernetes would be easy. Heroku would be a great option as well.
- [x] Add filtering options through uri parameters to make querying the database simple.
- [ ] Add a pretty UI
- [ ] Covert to pip installable package
