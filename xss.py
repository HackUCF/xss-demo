#!/usr/bin/env python

import sqlite3

from flask import Flask, render_template, redirect, url_for, request


_conn = sqlite3.connect('db.sqlite3')
_conn.execute('create table if not exists comment (id integer primary key, name TEXT, comment TEXT)')
_conn.close()

app = Flask(__name__)


class Comment(object):
    def __init__(self, name, text):
        self.name = name
        self.comment = text


@app.route('/')
def index():
    comments = []

    conn = sqlite3.connect('db.sqlite3')
    c = conn.cursor()
    for row in c.execute('select name, comment from comment'):
        comments.append(Comment(*row))

    conn.close()

    return render_template('index.html', comments=comments)


@app.route('/comment', methods=['POST'])
def comment():
    comment_name = request.form['name']
    comment_text = request.form['comment']

    conn = sqlite3.connect('db.sqlite3')
    with conn:
        # not sqli, just xss :P
        conn.execute('insert into comment(name, comment) values (?, ?)', (comment_name, comment_text))

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


@app.route('/clear-comments', methods=['GET', 'POST'])
def clear_comments():
    conn = sqlite3.connect('db.sqlite3')
    with conn:
        conn.execute('delete from comment')

    conn.commit()
    conn.close()

    return redirect(url_for('index'))


if __name__ == "__main__":
    app.debug = True
    app.run()