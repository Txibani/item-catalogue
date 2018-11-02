from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, CategoryItem, User

engine = create_engine('sqlite:///itemcataloguewithusers.db')

Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

session = DBSession()


# Create dummy user
User1 = User(name="Robo Barista", email="tinnyTim@udacity.com",
             picture='https://pbs.twimg.com/profile_images/2671170543/18debd694829ed78203a5a36dd364160_400x400.png')
session.add(User1)
session.commit()


# Items for Soccer
category1 = Category(user_id=1, name="Soccer")

session.add(category1)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Soccer ball", description="A football, soccer ball, or association football ball is the ball used in the sport of association football.",
                     category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Shin Guards", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Uniform", description="A uniform is a type of clothing worn by members of an organization while participating in that organization's activity.",
                     category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Soccer Cleats", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=1, name="GoalKeeper Gloves", description="Most goalkeepers also wear gloves to improve their grip on the ball, and to protect themselves from injury. ",
                     category=category1)

session.add(categoryItem5)
session.commit()

# Items for Frisbee
category2 = Category(user_id=1, name="Frisbee")

session.add(category2)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Gloves", description="A glove is a garment covering the whole hand. Gloves have separate sheaths or openings for each finger and the thumb.",
                     category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Braces", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Shoes", description="Wearing minimilist shoes (or barefoot shoes) are what is best for our feet to strengthen our toes and feet and ankles and will help reduce the impact on our knees and body. I have been wearing these shoes since 2009 years and have been an ambassador since 2012.",
                     category=category2)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Uniform", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category2)

session.add(categoryItem4)
session.commit()

# Items for Soccer
category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()

categoryItem1 = CategoryItem(user_id=1, name="Gloves", description="A glove is a garment covering the whole hand. Gloves have separate sheaths or openings for each finger and the thumb.",
                     category=category3)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, name="Braces", description="A shin guard or shin pad is a piece of equipment worn on the front of a player's shin to protect them from injury.",
                     category=category3)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, name="Shoes", description="Wearing minimilist shoes (or barefoot shoes) are what is best for our feet to strengthen our toes and feet and ankles and will help reduce the impact on our knees and body. I have been wearing these shoes since 2009 years and have been an ambassador since 2012.",
                     category=category3)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=1, name="Uniform", description="Football boots, called cleats or soccer shoes in North America, are an item of footwear worn when playing football.",
                     category=category3)

session.add(categoryItem4)
session.commit()


print "added categories items!"
