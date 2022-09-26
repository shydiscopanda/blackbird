import base64
import io
import os

from flask import Flask, flash, redirect, render_template, request, url_for

from src.charts import create_bar_chart
from src.search import run_fetch, run_query

template_dir = os.path.abspath('src/templates')
app = Flask(__name__, template_folder=template_dir)
app.config['SECRET_KEY'] = 'super-secret-key-this-is-a-demo'

SEARCH_CONFIG = {
    'term': "breast cancer treatment",
    'year_from': "2016",
    "year_to": "2021"
}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/chart/")
def chart():
    """
    Basic bar chart display
    :return: Renders static chart template
    """
    chunk = request.args.get('chunk')
    query_key = request.args.get('query_key')
    web_env = request.args.get('web_env')
    calls = request.args.get("calls")

    records = run_fetch(chunk, query_key, web_env, calls)
    # this ensures that records outside of search date are filtered out before display
    filtered_records = {k: v for (k, v) in records.items() if int(SEARCH_CONFIG["year_to"]) >= k >= int(SEARCH_CONFIG["year_from"])}
    fig = create_bar_chart(filtered_records)
    output = io.BytesIO()
    fig.savefig(output, format="png")
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    return render_template('chart.html', data=data, search_config=SEARCH_CONFIG)


@app.route("/progress/", methods=('GET', 'POST'))
def progress():
    """
    Progress page to inform search is underway
    :return: Renders static progress template
    """
    if request.method == 'POST':
        chunk = request.form['chunk']
        query_key = request.form['query_key']
        web_env = request.form['web_env']
        calls = request.form["calls"]
        return redirect(url_for('chart', chunk=chunk, query_key=query_key, web_env=web_env, calls=calls))

    count, chunk, q_key, web_env, calls = run_query(SEARCH_CONFIG["term"], int(SEARCH_CONFIG["year_from"]), int(SEARCH_CONFIG["year_to"]))
    return render_template('progress.html', count="{:,}".format(count), chunk=chunk, q_key=q_key, web_env=web_env, calls=calls)


@app.route('/search/', methods=('GET', 'POST'))
def search():
    """
    Basic HTML search box
    :return: Renders search template
    """
    if request.method == 'POST':
        term = request.form['term']
        year_from = request.form['year_from']
        year_to = request.form['year_to']

        if not term:
            flash('Search term is required!')
        elif not year_from:
            flash('Start year for search is required!')
        elif not year_to:
            flash('End year for search is required!')
        else:
            SEARCH_CONFIG["term"] = term
            SEARCH_CONFIG["year_from"] = year_from
            SEARCH_CONFIG["year_to"] = year_to
            return redirect(url_for('progress'))

    return render_template('search.html')

