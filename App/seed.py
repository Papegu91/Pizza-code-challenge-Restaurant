# seed.py
from models import db, Pizza, Restaurant, RestaurantPizza

def seed_data():
    # Create sample pizzas
    pizza1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    pizza2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")

    db.session.add_all([pizza1, pizza2])
    db.session.commit()

    # Create sample restaurants
    restaurant1 = Restaurant(name="Pizza Palace", address="123 Main St")
    restaurant2 = Restaurant(name="Slice Haven", address="456 Oak St")

    db.session.add_all([restaurant1, restaurant2])
    db.session.commit()

    # Associate pizzas with restaurants
    restaurant_pizza1 = RestaurantPizza(price=10, pizza=pizza1, restaurant=restaurant1)
    restaurant_pizza2 = RestaurantPizza(price=12, pizza=pizza2, restaurant=restaurant1)
    restaurant_pizza3 = RestaurantPizza(price=11, pizza=pizza2, restaurant=restaurant2)

    db.session.add_all([restaurant_pizza1, restaurant_pizza2, restaurant_pizza3])
    db.session.commit()

if __name__ == "__main__":
    from app import app, db

    with app.app_context():
        db.create_all()
        seed_data()