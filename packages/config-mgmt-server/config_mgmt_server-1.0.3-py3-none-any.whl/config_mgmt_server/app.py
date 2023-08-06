# save this as app.py
from flask import Flask
from celery import current_app
from celery.bin import worker

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
    app = current_app._get_current_object()
    worker = worker.worker(app=app)
    options = {
        'broker': 'redis://localhost:6379/0',
        'loglevel': 'INFO',
        'traceback': True,
    }
    worker.run(**options)

# Make sure there is a newline at the bottom!
