import random
import string
from flask import (
    Flask, render_template,
    request, url_for, redirect,
    flash, jsonify,
    make_response)
from flask import session as login_session
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from oauth2client.client import flow_from_clientsecrets, FlowExchangeError
import httplib2
import json
import requests

CLIENT_ID = json.loads(open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

def createUser(login_session):
    new_user = User(
        name=login_session['username'],
        email=login_session['email'],
        picture=login_session['picture'],
        )
    session.add(new_user)
    session.commit()
    created_user = session.query(User).filter_by(email=login_session['email']).one()
    return created_user.id

def getUserInfo(user_id):
    return session.query(User).filter_by(id=user_id).one()

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


def describe_item(item):
    attributes = r'<br/>'.join([item.name, item.price, item.description])
    return '<p>{}</p>'.format(attributes)

@app.route('/login/')
def login():
    state = ''.join([random.choice(string.ascii_uppercase + string.digits)
        for x in range(32)])
    login_session['state'] = state
    return render_template('login.html', STATE=state)

@app.route('/gconnect', methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter'), 401)
        response.headers['Content-type'] = 'application/json'
        return response
    code = request.data
    # print 'Google obtained code', code
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the authorization code'), 401)
        return response

    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token={}'.format(access_token))
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])

    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-type'] = 'application/json'

    gplus_id = credentials.id_token['sub']

    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps('Token\'s user ID doesnot match given user ID'), 401)
        response.headers['Content-type'] = 'application/json'
        return response

    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps('Token\'s client ID doesnot match app\'s'), 401)
        print 'Token\'s client ID doesnot match app\'s'
        response.headers['Content-type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected'), 200)
        response.headers['Content-type'] = 'application/json'

    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['provider'] = 'google'
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # see if user exists, if not then create
    user_id = getUserID(data['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    exchange_token = request.data

    fb_secrets = json.loads(open('fb_secrets.json', 'r').read())
    app_id = fb_secrets['web']['app_id']
    app_secret = fb_secrets['web']['app_secret']
    url = (
        'https://graph.facebook.com'
            '/oauth/access_token?'
                'grant_type=fb_exchange_token'
                '&client_id={}'
                '&client_secret={}'
                '&fb_exchange_token={}'
        ).format(app_id, app_secret, exchange_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # userinfo_url = 'https://graph.facebook.com/v2.8/me'
    access_token = json.loads(result)['access_token']

    url = (
        'https://graph.facebook.com'
            '/v2.8/me?access_token={}'
                '&fields=name,id,email'
        ).format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    data = json.loads(result)

    login_session['provider'] = 'facebook'
    login_session['username'] = data['name']
    login_session['email'] = data['email']
    login_session['facebook_id'] = data['id']
    login_session['access_token'] = access_token

    url = (
        'https://graph.facebook.com'
            '/v2.8/me/picture?'
                'access_token={}'
                '&redirect=0'
                '&height=200'
                '&width=200'
        ).format(access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data['data']['url']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id


    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output


@app.route('/gdisconnect')
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = (
        'https://graph.facebook.com'
            '/{}/permissions'
                '?access_token={}'
        ).format(facebook_id, access_token)

    result = requests.delete(url)

    if result.json()['success']:
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['facebook_id']
        return make_response(json.dumps("You have been logged out"), 200)
    else:
        return make_response(json.dumps("Error logging out!"), 400)

@app.route('/disconnect')
def disconnect():
    provider = login_session.get('provider')
    if provider:
        if provider == 'google':
            gdisconnect()
        elif provider == 'facebook':
            fbdisconnect()

        del login_session['provider']

        flash('You have successfully been logged out!')
    else:
        flash('Not logged in!')

    return redirect(url_for('showRestaurants'))

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    restaurants = session.query(Restaurant).order_by(asc(Restaurant.name))
    if 'username' not in login_session:
        return render_template('publicrestaurants.html', restaurants=restaurants)
    else:
        return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    creator = getUserInfo(restaurant.user_id)
    # public view
    if 'user_id' not in login_session or login_session['user_id'] != creator.id:
        return render_template('publicmenu.html', restaurant=restaurant, items=items, creator=creator)
    # owner view
    return render_template('menu.html', restaurant=restaurant, items=items, creator=creator)

@app.route('/restaurants/new', methods=['GET', 'POST'])
def newRestaurant():
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        new_restaurant = Restaurant(
            name=request.form['name'],
            user_id=login_session['user_id'],
            )
        session.add(new_restaurant)
        session.commit()
        flash('New restaurant {} successfully created'.format(new_restaurant.name))
        return redirect(url_for('showMenu', restaurant_id=new_restaurant.id))
    else:
        return render_template('newrestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    editedRestaurant = session.query(
        Restaurant).filter_by(id=restaurant_id).one()
    if 'username' not in login_session:
        return redirect('/login')
    if editedRestaurant.user_id != login_session['user_id']:
        return "<script>function myFunction() {alert('You are not authorized to edit this restaurant. Please create your own restaurant in order to edit.');}</script><body onload='myFunction()''>"
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            flash('Restaurant Successfully Edited %s' % editedRestaurant.name)
            return redirect(url_for('showRestaurants'))
    else:
        return render_template('editrestaurant.html', restaurant=editedRestaurant)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
        newItem = MenuItem(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            restaurant_id=restaurant_id,
            user_id=restaurant.user_id
            )
        session.add(newItem)
        session.commit()
        flash('New menu item has been created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)



@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, MenuID):
    editedItem = session.query(MenuItem).filter_by(id = MenuID).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
        #USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template('editmenuitem.html', restaurant_id = restaurant_id, MenuID = MenuID, item = editedItem)

@app.route('/restaurants/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    if 'username' not in login_session:
        return redirect('/login')
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if login_session['user_id'] != restaurant_id.user_id:
        return '''
<script>
    function myFunction() {
        alert("You are not authorized to delete this restaurant.
        Please create your own restaurant to delete!");
    }
</script>
<body onLoad="myFunction()">
</body>
'''
    if request.method == 'POST':
        session.delete(restaurant)
        session.commit()
        flash('Successfully deleted restaurant {}'.format(restaurant.name))


@app.route('/restaurants/<int:restaurant_id>/<int:MenuID>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, MenuID):
    deleted_item = session.query(MenuItem).filter_by(id=MenuID).one()
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html', item=deleted_item)

@app.route('/restaurants/<int:restaurant_id>/menu/JSON/', methods=['GET'])
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

if __name__ == "__main__":
    app.secret_key = 'super secret'
    app.debug = True
    app.run(host='localhost', port=5001)