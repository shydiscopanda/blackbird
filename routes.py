import base64
import io

from flask import Flask, flash, redirect, render_template, request, url_for

from charts import create_bar_chart
from search import run_fetch, run_query


app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key'

search_config = {
    'term': None,
    'year_from': "2000",
    "year_to": "2021"
}


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/chart/")
def chart():
    chunk = request.args.get('chunk')
    query_key = request.args.get('query_key')
    web_env = request.args.get('web_env')
    loops = request.args.get("loops")
    records = run_fetch(chunk, query_key, web_env, loops)
    filtered_records = {k: v for (k, v) in records.items() if int(search_config["year_to"]) >= k >= int(search_config["year_from"])}
    fig = create_bar_chart(filtered_records)
    output = io.BytesIO()
    fig.savefig(output, format="png")
    data = base64.b64encode(output.getbuffer()).decode("ascii")
    return render_template('chart.html', data=data, search_config=search_config)


@app.route("/progress/", methods=('GET', 'POST'))
def progress():
    if request.method == 'POST':
        chunk = request.form['chunk']
        query_key = request.form['query_key']
        web_env = request.form['web_env']
        loops = request.form["loops"]
        return redirect(url_for('chart', chunk=chunk, query_key=query_key, web_env=web_env, loops=loops))

    count, chunk, q_key, web_env, loops = run_query(search_config["term"], search_config["year_from"], search_config["year_to"])
    return render_template('progress.html', count="{:,}".format(count), chunk=chunk, q_key=q_key, web_env=web_env, loops=loops)


@app.route('/search/', methods=('GET', 'POST'))
def search():
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
            search_config["term"] = term
            search_config["year_from"] = year_from
            search_config["year_to"] = year_to
            return redirect(url_for('progress'))

    return render_template('search.html')

