FROM python:latest

COPY requirements.txt /chisalary/requirements.txt
COPY chisalary/ /chisalary/

WORKDIR /chisalary/

RUN pip install -r requirements.txt
