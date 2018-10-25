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
@app.route('/category')
def categoryItems():
    categories = session.query(Category).all()
    return render_template('categories.html', categories = categories)

# Show a category
@app.route('/category/<category_name>')
def showCategory(category_name):
    category = session.query(Category).filter_by(name = category_name).one()
    items = session.query(CategoryItem).filter_by(category_name = category_name).all()
    return render_template('category.html', items = items, category = category)


if __name__ == '__main__':
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)