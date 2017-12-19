# chisalary

## Contributing

```
cd chisalary
```

Start the server:
```python
python manage.py runserver
```

Start rabbit mq:
```
rabbitmq-server
```

Start celery workers:
```
celery -A chisalary worker -l info
```

Start celery beat:
```
celery -A chisalary beat -l info
```
