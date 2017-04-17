import logging

from flask.views import MethodView
from flask import render_template, url_for

from app import app


class PrayerView(MethodView):

    def get(self):
        title = "I NEED TO PRAY"
        data = url_for('static', filename='js/main.js')
        return render_template('prayer/index.html', title=title, js_script=data)

app.add_url_rule('/prayer', view_func=PrayerView.as_view('prayer'))