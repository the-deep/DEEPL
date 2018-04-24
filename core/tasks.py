from celery import task


@task
def test_celery():
    import time
    time.sleep(3)
    with open('/tmp/a.log', 'w') as f:
        f.write('bibek pandey')
        f.close()
