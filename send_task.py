from celery_config import add

result = add.delay(4, 4)
print(result.ready())  # It should print False

# Increase the timeout if necessary
print(result.get(timeout=10))  # It should print 8