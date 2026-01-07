from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "secret123"  # مؤقت (غيرها لاحقًا)

PRODUCTS = {
    "keyboard": {"name": "Mechanical Keyboard", "price": 189},
    "cable": {"name": "USB-C Cable", "price": 25},
}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/products")
def products():
    cart_items = session.get("cart", [])
    cart_count = len(cart_items)
    return render_template("products.html", products=PRODUCTS, cart_count=cart_count)


@app.route("/add/<item>")
def add(item):
    if item not in PRODUCTS:
        return redirect(url_for("products"))

    cart = session.get("cart", [])
    cart.append(PRODUCTS[item])
    session["cart"] = cart

    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_items = session.get("cart", [])
    total = sum(item["price"] for item in cart_items)
    return render_template("cart.html", cart=cart_items, total=total)

@app.route("/clear")
def clear_cart():
    session.pop("cart", None)
    return redirect(url_for("cart"))


@app.route("/remove/<int:index>")
def remove(index):
    cart = session.get("cart", [])
    if 0 <= index < len(cart):
        cart.pop(index)
        session["cart"] = cart
    return redirect(url_for("cart"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)