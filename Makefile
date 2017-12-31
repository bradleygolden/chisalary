run:
	python chisalary/manage.py runserver

clean:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	find . -name .DS_Store -delete
	rm -rf ./chisalary/staticfiles

test:
	coverage run --source=. chisalary/manage.py test api --noinput
