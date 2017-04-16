import logging

from flask.views import MethodView
from flask import render_template

from app import app


class GratitudeView(MethodView):

    def get(self):
        return render_template('gratitude/index.html')

app.add_url_rule('/', view_func=GratitudeView.as_view('gratitude'))
