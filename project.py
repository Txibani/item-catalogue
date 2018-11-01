from flask import Flask, render_template, request, \
    redirect, jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# import CRUD operations
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem, User

# Login imports
from flask import session as login_session
import random
import string

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']

app = Flask(__name__)

# Create session and connect to DB
engine = create_engine(
    'sqlite:///itemcataloguewithusers.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# Create anti-forgery state token
@app.route(
    '/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template('login.html', STATE=state)


@app.route(
    '/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    print(data)

    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['email']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += '''
        " style = "width: 300px; height: 300px;border-radius: 150px;
        -webkit-border-radius: 150px;-moz-border-radius: 150px;"> '''
    return output


@app.route(
    '/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    url = '''https://accounts.google.com/
        o/oauth2/revoke?token=%s''' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect('/')
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response


# User
def createUser(login_session):
    newUser = User(
        name=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


# Json endpoint
@app.route(
    '/catalog/json')
def restaurantsJSON():
    categories = session.query(Category).all()
    return jsonify(categories=[r.serialize for r in categories])


# Show all categories
@app.route(
    '/')
@app.route(
    '/catalog')
def categoryItems():
    categories = session.query(Category).all()
    latest_items = session.query(CategoryItem).order_by(
        CategoryItem.id.desc()).limit(5).all()

    if 'email' not in login_session:
        return render_template(
            'publicCategories.html', categories=categories, items=latest_items)
    else:
        return render_template(
            'categories.html', categories=categories, items=latest_items)


# Show a category and list of items
@app.route(
    '/catalog/<category_name>')
@app.route(
    '/catalog/<category_name>/items')
def showCategory(category_name):
    categories = session.query(Category).all()
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(
        category_name=category_name).all()

    if 'email' not in login_session:
        return render_template(
            'publicCategory.html', categories=categories,
            items=items, category=category)
    else:
        return render_template(
            'category.html', categories=categories,
            items=items, category=category)


# Show item description
@app.route(
    '/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name=category_name).one()
    items = session.query(CategoryItem).filter_by(name=item_name).all()
    for item in items:
        if item.category_name == category.name:
            item_show = item

    if 'email' not in login_session:
        return render_template(
            'publicItem.html', item=item_show, category=category)
    else:
        return render_template('item.html', item=item_show, category=category)


# Add new item to a category
@app.route('/catalog/<category_name>/new/', methods=['GET', 'POST'])
def addItem(category_name):
    if 'email' not in login_session:
        return redirect('login')

    category = session.query(Category).filter_by(name=category_name).one()

    if request.method == 'POST':
        newItem = CategoryItem(
            name=request.form['name'],
            description=request.form['description'],
            category=category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template('addItem.html', category=category)


# Edit category item
@app.route(
    '/catalog/<category_name>/<item_name>/edit/', methods=['GET', 'POST'])
def editItem(category_name, item_name):
    if 'email' not in login_session:
        return redirect('login')
    category = session.query(Category).filter_by(name=category_name).one()
    editedItem = session.query(CategoryItem).filter_by(name=item_name).all()

    for item in editedItem:
        if item.category_name == category.name:
            item_show_edit = item

    if request.method == 'POST':
        if request.form['name']:
            item_show_edit.name = request.form['name']
        if request.form['description']:
            item_show_edit.description = request.form['description']
        session.add(item_show_edit)
        session.commit()
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template(
            'editItem.html', category=category, item=item_show_edit)


# Delete category item
@app.route(
    '/catalog/<category_name>/<item_name>/delete/', methods=['GET', 'POST'])
def deleteItem(category_name, item_name):
    if 'email' not in login_session:
        return redirect('login')
    editedItem = session.query(CategoryItem).filter_by(name=item_name).all()
    category = session.query(Category).filter_by(name=category_name).one()

    for item in editedItem:
        if item.category_name == category.name:
            item_delete_edit = item

    if request.method == 'POST':
        session.delete(item_delete_edit)
        session.commit()
        return redirect(url_for('showCategory', category_name=category.name))
    else:
        return render_template(
            'deleteItem.html', category=category, item=item_delete_edit)


if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
