from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# from database_setup import Restaurant, Base, MenuItem
from database_setup import Base, Category, CategoryItem

engine = create_engine('sqlite:///itemcatalogue.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Items for Soccer
category1 = Category(name="Soccer")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(name="Soccer ball", description="A football, soccer ball, or association football ball is the ball used in the sport of association football.",
                     category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(name="Shin Guards", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Uniform", description="A uniform is a type of clothing worn by members of an organization while participating in that organization's activity.",
                     category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Soccer Cleats", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(name="GoalKeeper Gloves", description="Most goalkeepers also wear gloves to improve their grip on the ball, and to protect themselves from injury. ",
                     category=category1)

session.add(categoryItem5)
session.commit()

# Items for Frisbee
category2 = Category(name="Frisbee")

session.add(category2)
session.commit()

categoryItem1 = CategoryItem(name="Gloves", description="A glove is a garment covering the whole hand. Gloves have separate sheaths or openings for each finger and the thumb.",
                     category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(name="Braces (ankle/knee)", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Shoes", description="Wearing minimilist shoes (or barefoot shoes) are what is best for our feet to strengthen our toes and feet and ankles and will help reduce the impact on our knees and body. I have been wearing these shoes since 2009 years and have been an ambassador since 2012.",
                     category=category2)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Uniform", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category2)

session.add(categoryItem4)
session.commit()

# Items for Soccer
category3 = Category(name="Baseball")

session.add(category3)
session.commit()

categoryItem1 = CategoryItem(name="Gloves", description="A glove is a garment covering the whole hand. Gloves have separate sheaths or openings for each finger and the thumb.",
                     category=category3)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(name="Braces (ankle/knee)", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category3)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(name="Shoes", description="Wearing minimilist shoes (or barefoot shoes) are what is best for our feet to strengthen our toes and feet and ankles and will help reduce the impact on our knees and body. I have been wearing these shoes since 2009 years and have been an ambassador since 2012.",
                     category=category3)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(name="Uniform", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category3)

session.add(categoryItem4)
session.commit()



print "added categories items!"