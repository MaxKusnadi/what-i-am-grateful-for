import json

from flask.views import MethodView
from flask import render_template

from app import app
from app.prayer.controller import PrayerController


class PrayerView(MethodView):

    def __init__(self):  # pragma: no cover
        self.controller = PrayerController()

    def get(self):
        unprayed_prayers = self.controller.get_unprayed_prayers()
        prayed_prayers = self.controller.get_prayed_prayers()
        return render_template('prayer/index.html',
                               results=unprayed_prayers,
                               prayed_prayers=prayed_prayers)


class PrayerAPIView(MethodView):

    def __init__(self):  # pragma: no cover
        self.controller = PrayerController()

    def get(self):
        unprayed_prayers = self.controller.get_unprayed_prayers_api()
        return json.dumps(unprayed_prayers)



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


app.add_url_rule('/prayer', view_func=PrayerView.as_view('prayer'))
app.add_url_rule('/api/prayer', view_func=PrayerAPIView.as_view('prayer_api'))
