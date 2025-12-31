from flask import Flask, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "dev-secret-change-later"

# Fake products (later we replace with DB)
PRODUCTS = [
    {"id": 1, "name": "Wireless Mouse", "price": 49.0},
    {"id": 2, "name": "Mechanical Keyboard", "price": 189.0},
    {"id": 3, "name": "USB-C Cable", "price": 25.0},
    {"id": 4, "name": "Headphones", "price": 299.0},
]

def get_product(pid: int):
    return next((p for p in PRODUCTS if p["id"] == pid), None)

def get_cart():
    # cart: {product_id(str): qty(int)}
    return session.get("cart", {})

def save_cart(cart: dict):
    session["cart"] = cart
    session.modified = True

@app.get("/")
def home():
    cart = get_cart()
    cart_count = sum(cart.values())
    return render_template("index.html", products=PRODUCTS, cart_count=cart_count)

@app.get("/add/<int:pid>")
def add_to_cart(pid):
    product = get_product(pid)
    if not product:
        return redirect(url_for("home"))

    cart = get_cart()
    key = str(pid)
    cart[key] = cart.get(key, 0) + 1
    save_cart(cart)
    return redirect(url_for("home"))

@app.get("/remove/<int:pid>")
def remove_from_cart(pid):
    cart = get_cart()
    key = str(pid)
    if key in cart:
        cart[key] -= 1
        if cart[key] <= 0:
            del cart[key]
    save_cart(cart)
    return redirect(url_for("cart"))

@app.get("/cart")
def cart():
    cart = get_cart()

    items = []
    total = 0.0
    for key, qty in cart.items():
        pid = int(key)
        product = get_product(pid)
        if not product:
            continue
        line_total = product["price"] * qty
        total += line_total
        items.append(
            {
                "id": pid,
                "name": product["name"],
                "price": product["price"],
                "qty": qty,
                "line_total": line_total,
            }
        )

    return render_template("cart.html", items=items, total=total)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)