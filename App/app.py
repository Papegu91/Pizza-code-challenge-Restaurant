from flask import Flask, make_response, jsonify, request
from flask_migrate import Migrate
from flask_restful import Api, Resource 
from models import db, Pizza, Restaurant, RestaurantPizza 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app, db)
db.init_app(app)

api = Api(app)

@app.route('/')
def home():
    return 'Welcome to the most loved Pizzas app.'

class RestaurantResource(Resource):
    def get(self):
        restaurants = Restaurant.query.all()

        if restaurants:
            try:
                restaurants_data = [
                    {
                        "id": restaurant.id,
                        "name": restaurant.name,
                        "address": restaurant.address,
                        "pizzas": [
                            {
                                "id": rp.pizza.id,
                                "name": rp.pizza.name,
                                "ingredients": rp.pizza.ingredients
                            } for rp in restaurant.restaurant_pizzas
                        ]
                    } for restaurant in restaurants
                ]
                response = make_response(
                    jsonify(restaurants_data),
                    200
                )
            except Exception as e:
                print(f"Caught an exception: {e}") 
                response = make_response(
                    jsonify({"error": f"{e}"}),
                    500
                )  
        else:
            response = make_response(
                jsonify({"error": "No restaurant data"}),
                404
            )
        return response


class SingleRestaurantResource(Resource):
    
    def get(self, id):
        restaurant = Restaurant.query.filter_by(id=id).first()

        if restaurant:
            try:
                restaurant_dict = {
                    "id": restaurant.id,
                    "name": restaurant.name,
                    "address": restaurant.address,
                }
                response = make_response(
                    jsonify(restaurant_dict),
                    200
                )
            except Exception as e:
                print(f"Caught an exception: {e}") 
                response = make_response(
                    jsonify({"error": f"{e}"}),
                    404
                )  
        else:
            response = make_response(
                jsonify({"error": f"Restaurant id {id} not found"}),
                404
            )

        return response 
    
    #to delete a restaurant
    def delete(self, id):
        restaurant = Restaurant.query.get(id)

        if restaurant:
            try:
                # Delete associated RestaurantPizzas
                RestaurantPizza.query.filter_by(restaurant_id=id).delete()

                # Delete the Restaurant
                db.session.delete(restaurant)
                db.session.commit()

                response = make_response('', 204)  # HTTP status code for No Content
            except Exception as e:
                print(f"Caught an exception: {e}")
                response = make_response(
                    jsonify({"error": "An unexpected error occurred while deleting the restaurant"}),
                    500  # HTTP status code for Internal Server Error
                )
        else:
            response = make_response(
                jsonify({"error": "Restaurant not found"}),
                404  # HTTP status code for Not Found
            )

        return response 

api.add_resource(RestaurantResource, '/restaurants')
api.add_resource(SingleRestaurantResource, '/restaurants/<int:id>')

class PizzaResource(Resource):
    def get(self):
        pizzas = Pizza.query.all()
        pizza_data = [
            {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }
            for pizza in pizzas
        ]
        return pizza_data

api.add_resource(PizzaResource, '/pizzas')

class RestaurantPizzaResource(Resource):
    def post(self):
        try:
            data = request.get_json()

            # Validate required fields
            if 'price' not in data or 'pizza_id' not in data or 'restaurant_id' not in data:
                raise ValueError("Validation error: Missing required fields")

            price = data['price']
            pizza_id = data['pizza_id']
            restaurant_id = data['restaurant_id']

            # Validate pizza and restaurant existence
            pizza = Pizza.query.get(pizza_id)
            restaurant = Restaurant.query.get(restaurant_id)

            if not pizza or not restaurant:
                raise ValueError("Validation error: Pizza or restaurant not found")

            # Create and add the new RestaurantPizza
            restaurant_pizza = RestaurantPizza(price=price, pizza=pizza, restaurant=restaurant)
            db.session.add(restaurant_pizza)
            db.session.commit()

            # Respond with data related to the Pizza
            pizza_data = {
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            }

            response = make_response(
                jsonify(pizza_data),
                201  # HTTP status code for Created
            )

        except ValueError as e:
            response = make_response(
                jsonify({"errors": [str(e)]}),
                400  # HTTP status code for Bad Request
            )

        except Exception as e:
            print(f"Caught an exception: {e}") 
            response = make_response(
                jsonify({"errors": ["An unexpected error occurred"]}),
                500  # HTTP status code for Internal Server Error
            )

        return response

# Add the new resource to the API
api.add_resource(RestaurantPizzaResource, '/restaurant_pizzas')

    
        


if __name__ == '__main__':
    app.run(port=5555)