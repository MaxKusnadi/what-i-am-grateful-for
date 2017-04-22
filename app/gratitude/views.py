from flask.views import MethodView
from flask import render_template, url_for

from app import app
from app.gratitude.controller import GratitudeController


class GratitudeView(MethodView):

    def __init__(self):  # pragma: no cover
        self.controller = GratitudeController()

    def get(self):
        results = self.controller.get_all_gratitudes()
        return render_template('gratitude/index.html', results=results)


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


app.add_url_rule('/', view_func=GratitudeView.as_view('gratitude'))
