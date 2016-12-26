from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import requests, json
import random
import actions


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def start_page(query="start_page", page=1):
    results, pages, total = actions.search(query)
    return render_template('home.html', results=results, total=total, query_text=query, page=page, pages=pages)


@app.route('/<query>/<page>', methods=['GET', 'POST'])
def show_entries(query="", page=1):
    if request.method == 'POST':
        query = request.form["search-text"]
    results, pages, total = actions.search(query)
    return render_template('search.html', results=results, total=total, query_text=query, page=page, pages=pages)


@app.route('/search', methods=['POST'])
def search():
    if request.method == 'POST':
        query = request.form["search-text"]
        results, pages, total = actions.search(query)
        return render_template('search.html', results=results, total=total, query_text=query, page=1)


@app.route('/page', methods=['POST'])
def get_page():
    if request.method == 'POST':
        page = int(request.form["page"])
        query_text = request.form["query_name"]
        print query_text
        return redirect('/'+query_text+'/'+int(page))


if __name__ == '__main__':
    app.run()
