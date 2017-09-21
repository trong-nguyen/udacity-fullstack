from flask import (
	Flask, render_template,
	request, url_for, redirect,
	flash, jsonify)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)

def describe_item(item):
	attributes = r'<br/>'.join([item.name, item.price, item.description])
	return '<p>{}</p>'.format(attributes)


@app.route('/')
@app.route('/restaurants/')
def hello_world():
	restaurant = session.query(Restaurant).first()
	items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
	output = ''.join([describe_item(i) for i in items])
	return output

@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)

# DOESNOT WORK
# @app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
# def newMenuItem(restaurant_id):
# 	if request.method == 'POST':
# 		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
# 		session.add(newItem)
# 		session.commit()
# 		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
# 	else:
# 		return render_template('newmenuitem.html', restaurant_id = restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'],
            price=request.form['price'],
            description=request.form['description'],
            restaurant_id=restaurant_id)
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