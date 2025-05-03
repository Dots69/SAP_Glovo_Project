from flask import Flask, request, jsonify
from flask_cors import CORS
import db

app = Flask(__name__)
CORS(app)

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    success = db.register_user(data["username"], data["password"], data["role"])
    return jsonify({"status": "ok" if success else "error"})

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    user = db.login_user(data["username"], data["password"])
    if user:
        return jsonify({"status": "ok", "user": user})
    return jsonify({"status": "error", "message": "Invalid login"})

@app.route("/restaurants", methods=["GET"])
def restaurants():
    return jsonify(db.get_restaurants())

@app.route("/menu/<int:restaurant_id>", methods=["GET"])
def menu(restaurant_id):
    return jsonify(db.get_menu(restaurant_id))

@app.route("/order", methods=["POST"])
def order():
    data = request.json
    success, msg = db.place_order(
        data["customer_id"],
        data["restaurant_id"],
        data["item_id"],
        data["quantity"]
    )
    return jsonify({"status": "ok" if success else "error", "message": msg})

@app.route("/courier/orders", methods=["GET"])
def courier_orders():
    return jsonify(db.get_courier_orders())

@app.route("/courier/complete", methods=["POST"])
def complete():
    data = request.json
    success = db.complete_order(data["order_id"], data["courier_id"])
    return jsonify({"status": "ok" if success else "error"})

@app.route("/admin/restaurant", methods=["POST"])
def add_restaurant():
    data = request.json
    db.add_restaurant(data["name"], data["created_by"])
    return jsonify({"status": "ok"})

@app.route("/admin/item", methods=["POST"])
def add_item():
    data = request.json
    db.add_item(data["name"], float(data["price"]), data["restaurant_id"])
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)