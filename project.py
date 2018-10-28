from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

## import CRUD operations
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Category, CategoryItem

## Create session and connect to DB
engine = create_engine('sqlite:///itemcatalogue.db?check_same_thread=False')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Show all categories
@app.route('/')
@app.route('/catalog')
def categoryItems():
    categories = session.query(Category).all()

    return render_template('categories.html', categories = categories)


# Show a category and list of items
@app.route('/catalog/<category_name>')
@app.route('/catalog/<category_name>/items')
def showCategory(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CategoryItem).filter_by(category_name = category_name).all()

    return render_template('category.html', items = items, category = category)


# Show item description
@app.route('/catalog/<category_name>/<item_name>')
def showItem(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CategoryItem).filter_by(name = item_name).all()
    for item in items:
        if item.category_name == category.name:
            item_show = item

    return render_template('item.html', item = item_show, category = category)   


#Add new item to a category
@app.route('/catalog/<category_name>/new/',methods=['GET','POST'])
def addItem(category_name):
    category = session.query(Category).filter_by(name = category_name).one()

    if request.method == 'POST':
        newItem = CategoryItem(name = request.form['name'], description = request.form['description'], category = category)
        session.add(newItem)
        session.commit()
        return redirect(url_for('showCategory', category_name = category.name))
    else:
        return render_template('addItem.html', category = category)



# Edit category item
@app.route('/catalog/<category_name>/<item_name>/edit/', methods = ['GET', 'POST'])
def editItem(category_name, item_name):
    category = session.query(Category).filter_by(name = category_name).one()
    editedItem = session.query(CategoryItem).filter_by(name = item_name).all()

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
        return redirect(url_for('showCategory', category_name = category.name))
    else:
        return render_template('editItem.html', category = category, item = item_show_edit)


# Delete category item
@app.route('/catalog/<category_name>/<item_name>/delete/', methods = ['GET', 'POST'])
def deleteItem(category_name, item_name):
    editedItem = session.query(CategoryItem).filter_by(name = item_name).all()
    category = session.query(Category).filter_by(name = category_name).one()

    for item in editedItem:
        if item.category_name == category.name:
            item_delete_edit = item

    if request.method == 'POST':
        session.delete(item_delete_edit)
        session.commit()
        return redirect(url_for('showCategory', category_name = category.name))
    else:
        return render_template('deleteItem.html', category = category, item = item_delete_edit)
    

if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)