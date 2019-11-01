from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from client import Client
import os
import re

app = Flask(__name__)


@app.route('/home', methods=['POST'])
def get_user_input():
    newclient = Client()
    usertype = session.get('user')
    httpregex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    url = request.form('url')
    if re.match(httpregex, url) and not request.form.get('private'):
        newclient.handlerequest({'mode': 'geturl', 'url': url})
    if request.form.get('private') and usertype is 'manager':
        pass
    return render_template('home.html',
                           title='Proxy Homepage',
                           invalidurl=True,
                               usertype=usertype)


@app.route('/login', methods=['POST'])
def do_admin_login():

    usertype = session.get('user')
    if request.form['password'] == 'password' and request.form['username'] == 'admin':

        session['logged_in'] = True
        session['user'] = 'admin'
        return redirect(url_for('settings'))
    else:
        flash('wrong password!')
        return home()


@app.route('/login')
def login():

    usertype = session.get('user')
    return render_template('login.html',
                           title='Login Page',
                           usertype=usertype)

@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user'] = None
    usertype = session.get('user')
    return home()


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    newclient = Client()
    # data = newclient.getadmindata()
    usertype = session.get('user')
    if not session.get('logged_in') and usertype is not 'admin':
        flash('Please log in to access this page.')
        return home()

    if request.method == 'GET':
        return render_template('proxy-settings.html',
                               title='Admin Page',
                               usertype=usertype)
    if request.method == 'POST':
        newadmin = request.form.get('newadmin')
        newadminpass = request.form.get('newadminpass')
        newblocked = request.form.get('newblocked')
        clear = request.form.get('clear')
        newadminsite = request.form.get('newadminsite')
        newmanager = request.form.get('newmanager')
        newmanagerpass = request.form.get('newmanagerpass')
        if newadmin is not None and newadminpass is not None:
            newclient.addadmin(newadmin, newadminpass)
        if newblocked is not None:
            newclient.addblocked(newblocked)
        if clear is not None:
            newclient.clear_cache()
        if newadminsite is not None:
            newclient.addadminsite(newadminsite)
        if newmanager is not None and newmanagerpass is not None:
            newclient.addmanager(newmanager, newmanagerpass)

    return render_template('proxy-settings.html',
                               title='Admin Page',
                               usertype=usertype,)


@app.route('/')
def home():
    usertype = session.get('user')
    return render_template('home.html',
                           title='Proxy Homepage',
                               usertype=usertype)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
