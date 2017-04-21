from flask.views import MethodView
from flask import render_template, url_for

from app import app
from app.prayer.controller import PrayerController


class PrayerView(MethodView):

    def __init__(self):  # pragma: no cover
        self.controller = PrayerController()

    def get(self):
        title = "I NEED TO PRAY"
        unprayed_prayers = self.controller.get_unprayed_prayers()
        prayed_prayers = self.controller.get_prayed_prayers()
        return render_template('prayer/index.html', title=title,
                               results=unprayed_prayers,
                               prayed_prayers=prayed_prayers)


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