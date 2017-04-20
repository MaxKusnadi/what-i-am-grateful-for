from app import db
from app.gratitude.models import Gratitude
from app.prayer.models import Prayer

Gratitude.query.delete()
Prayer.query.delete()

db.session.commit()
