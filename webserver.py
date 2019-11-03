from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session, abort
from client import Client
import os
import re

app = Flask(__name__)

newclient = Client()


@app.route('/home', methods=['POST'])
def get_user_input():
    data = {'text': 'error loading page'}
    usertype = session.get('user')
    httpregex = re.compile(
        # r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    url = request.form['url']
    private = request.form.get('private')
    isadminsite = newclient.isadminsite(url)
    if re.match(httpregex, url) and not private:
        if isadminsite and usertype != 'admin':
            data['text'] = 'THIS SITE IS FOR ADMINS ONLY'
        else:
            data = newclient.handlerequest(
                {'mode': 'geturl', 'url': url, 'private': False})
    elif re.match(httpregex, url) and usertype == 'admin':
        data = newclient.handlerequest(
            {'mode': 'geturl', 'url': url, 'private': False})
    elif re.match(httpregex, url) and private:
        if usertype == 'manager' or usertype == 'admin':
            if usertype == 'manager' and isadminsite:
                data['text'] = 'THIS SITE IS FOR ADMINS ONLY'
            data = newclient.handlerequest(
                {'mode': 'geturl', 'url': url, 'private': True})
    else:
        return render_template('home.html',
                               title='Proxy Homepage',
                               invalidurl=True,
                               usertype=usertype,
                               data=data['text'])
    return render_template('home.html',
                           title='Proxy Homepage',
                           invalidurl=False,
                           usertype=usertype,
                           data=data['text'])


@app.route('/login', methods=['POST'])
def do_admin_login():
    username = request.form['username']
    password = request.form['password']
    if password == 'password' and username == 'admin':
        session['logged_in'] = True
        session['user'] = 'admin'
        return redirect(url_for('settings'))
    elif newclient.isadmin(username, password):
        session['logged_in'] = True
        session['user'] = 'admin'
        return redirect(url_for('settings'))
    elif newclient.isman(username, password):
        session['logged_in'] = True
        session['user'] = 'manager'
        return redirect(url_for('home'))
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
    return home()


@app.route('/settings', methods=['GET', 'POST'])
def settings():
    data = newclient.getadmindata()
    usertype = session.get('user')
    listofadmins = data['admins']
    listofmans = data['managers']
    cachedsites = data['cached']
    adminsites = data['adminsites']
    blockedsites = data['blocked']
    if not session.get('logged_in') and usertype is not 'admin':
        flash('Please log in to access this page.')
        return home()
    if request.method == 'GET':
        return render_template('proxy-settings.html',
                               title='Admin Page',
                               usertype=usertype,
                               listofadmins=listofadmins,
                               cachedsites=cachedsites,
                               blockedsites=blockedsites,
                               listofmans=listofmans,
                               adminsites=adminsites)
    if request.method == 'POST':
        newadmin = request.form.get('newadmin')
        newadminpass = request.form.get('newadminpass')
        newblocked = request.form.get('newblocked')
        clear = request.form.get('clear')
        newadminsite = request.form.get('newadminsite')
        newmanager = request.form.get('newman')
        newmanagerpass = request.form.get('newmanpass')
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

    return redirect(url_for('settings'))


@app.route('/')
def home():
    usertype = session.get('user')
    return render_template('home.html',
                           title='Proxy Homepage',
                           usertype=usertype)


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
