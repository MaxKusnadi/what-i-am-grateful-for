import logging

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_sslify import SSLify
from flask_cors import CORS

logging.basicConfig(level=logging.INFO,
                    format=' %(asctime)s - %(levelname)s - %(message)s')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
CORS(app)
socketio = SocketIO(app)
sslify = SSLify(app)

# Models
from app.gratitude.models import *
from app.prayer.models import *

# Views
from app.gratitude.views import *
from app.prayer.views import *

# Socket
from app.gratitude.controller import *
from app.prayer.controller import *

