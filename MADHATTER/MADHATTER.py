# MADHATTER/MADHATTER.py

import os
from flask import Flask, render_template, g, request, redirect
from sqlite3 import dbapi2 as sqlite3

##### APP SETUP #####
app = Flask(__name__)

##### DB SETUP #####

# Setup the database credentials
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'MADHATTER.db'),
    DEBUG=True,
    SECRET_KEY=b'<SOME HEXADECIMAL SECRET KEY>',
    USERNAME='admin',
    PASSWORD='<SOME PASSWORD>'
))

# Connect to the DB
def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv

# Wrap the helper function so we only open the DB once
def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

# Create the database (we do this via command line!!!)
def init_db():
    """Initializes the database."""
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()

# Command to create the database via command line
# You call it from command line: flask initdb
@app.cli.command('initdb')
def initdb_command():
    """Creates the database tables."""
    init_db()
    print('Initialized the database.')

# Close the database when the request ends
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


## =============================================================================================== ##
##### ROUTES #####
## =============================================================================================== ##
# /GET home (show collection of madlibs)
@app.route('/home') # THIS IS A SINGLE ROUTE
def home_route() :
    db = get_db()
    cur = db.execute('select * from madlibs order by id asc')
    return render_template('home.html', madlibs=cur.fetchall())

# THIS IS 5 ROUTES IN ONE (BUT HTML FORMS ONLY ALLOW GET/POST)
# /GET madlib (create form)
# /POST madlib (create)
# /GET madlib ID (edit form)
# /PUT madlib ID (update)
# /DELETE madlib ID (delete)
@app.route('/madlib', methods=['GET','POST'])
@app.route('/madlib/<an_id>', methods=['GET','POST'])
def madlib_route(an_id=None) :
    if (request.method == 'GET') :
        if (an_id == None) : # /GET madlib (create form)
            return render_template('create_madlib.html')
        else : # /GET madlib ID (edit form)
            db = get_db()
            cur = db.execute('select * from madlibs where id=?', an_id)
            results = cur.fetchall()
            the_madlib = (results[0] if results else None)
            return render_template('edit_madlib.html', madlib=the_madlib)
    else : # POST, PUT, and DELETE
        the_method = request.form['_method']
        if (the_method == 'PUT'): # /PUT madlib ID (update)
            bname = request.form['bus_name']
            btype = request.form['bus_type']
            bmrkt = request.form['market_type']
            bdone = request.form['job_be_done']
            brevm = request.form['rev_model']

            if (bname == '' or btype == '' or bmrkt == '' or bdone == '' or brevm == '') :
                return render_template('create_madlib.html', error_msg='Please fill all input fields')
            else :
                db = get_db()
                cur = db.execute('update madlibs set bus_name=?, bus_type=?, market_type=?, job_be_done=?, rev_model=? where id=?',
                                [bname, btype, bmrkt, bdone, brevm, an_id])
                db.commit()

                return redirect('/home')
        elif (the_method == 'DELETE') :
                db = get_db()
                cur = db.execute('delete from madlibs where id=?', an_id)
                db.commit()

                return redirect('/home')
        else :
            bname = request.form['bus_name']
            btype = request.form['bus_type']
            bmrkt = request.form['market_type']
            bdone = request.form['job_be_done']
            brevm = request.form['rev_model']

            if (bname == '' or btype == '' or bmrkt == '' or bdone == '' or brevm == '') :
                return render_template('create_madlib.html', error_msg='Please fill all input fields')
            else :
                db = get_db()
                db.execute('insert into madlibs (bus_name, bus_type, market_type, job_be_done, rev_model) values (?, ?, ?, ?, ?)',
                            [bname, btype, bmrkt, bdone, brevm])
                db.commit()

                return redirect('/home')
