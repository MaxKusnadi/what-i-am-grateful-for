from flask.views import MethodView
from flask import render_template, url_for

from app import app
from app.gratitude.controller import GratitudeController


class GratitudeView(MethodView):

    def __init__(self):  # pragma: no cover
        self.controller = GratitudeController()

    def get(self):
        title = "I AM GRATEFUL"
        results = self.controller.get_all_gratitudes()
        return render_template('gratitude/index.html', results=results,
                               title=title)

app.add_url_rule('/', view_func=GratitudeView.as_view('gratitude'))
