clean:
	find . -name \*.pyc -delete
	find . -name __pycache__ -delete
	find . -name .DS_Store -delete
	rm -rf ./chisalary/staticfiles
