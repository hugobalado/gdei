import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_babel import Babel, _
from models import db, Store, Product, Inventory

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///smart_store.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Babel configuration
app.config['BABEL_DEFAULT_LOCALE'] = 'es'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'es']

def get_locale():
    # Attempt to retrieve language from session
    return session.get('lang', app.config['BABEL_DEFAULT_LOCALE'])

babel = Babel(app, locale_selector=get_locale)

db.init_app(app)

@app.route('/set_language/<lang>')
def set_language(lang):
    if lang in app.config['BABEL_SUPPORTED_LOCALES']:
        session['lang'] = lang
    return redirect(request.referrer or url_for('index'))


def seed_data():
    if Store.query.first() is None:
        # Create 4 stores
        stores = [
            Store(name="Supermercado Centro", location="Calle Mayor, 1"),
            Store(name="Supermercado Norte", location="Av. de la Libertad, 45"),
            Store(name="Supermercado Sur", location="Plaza del Sol, 12"),
            Store(name="Supermercado Este", location="Calle del Mar, 8")
        ]
        db.session.add_all(stores)
        db.session.commit()

        # Create 10 products
        products = [
            Product(name="Leche Entera", description="1 Litro", price=0.90),
            Product(name="Pan de Molde", description="Integrales", price=1.50),
            Product(name="Huevos", description="Docena", price=2.20),
            Product(name="Aceite de Oliva", description="1 Litro, Virgen Extra", price=8.50),
            Product(name="Arroz", description="1 Kg", price=1.10),
            Product(name="Pasta", description="Macarrones, 500g", price=0.85),
            Product(name="Manzanas", description="1 Kg", price=1.99),
            Product(name="Pollo", description="Pechuga, 1 Kg", price=6.50),
            Product(name="Café", description="Natural, 250g", price=2.80),
            Product(name="Azúcar", description="Blanco, 1 Kg", price=1.00)
        ]
        db.session.add_all(products)
        db.session.commit()

        # Create inventory (min 2 per store)
        inventories = [
            Inventory(store_id=stores[0].id, product_id=products[0].id, quantity=50),
            Inventory(store_id=stores[0].id, product_id=products[1].id, quantity=30),
            Inventory(store_id=stores[1].id, product_id=products[2].id, quantity=40),
            Inventory(store_id=stores[1].id, product_id=products[3].id, quantity=15),
            Inventory(store_id=stores[2].id, product_id=products[4].id, quantity=60),
            Inventory(store_id=stores[2].id, product_id=products[5].id, quantity=45),
            Inventory(store_id=stores[3].id, product_id=products[6].id, quantity=25),
            Inventory(store_id=stores[3].id, product_id=products[7].id, quantity=20),
            # Add a couple more randomly to ensure more variety
            Inventory(store_id=stores[0].id, product_id=products[8].id, quantity=100),
            Inventory(store_id=stores[2].id, product_id=products[9].id, quantity=80)
        ]
        db.session.add_all(inventories)
        db.session.commit()

with app.app_context():
    db.create_all()
    seed_data()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stores', methods=['GET', 'POST'])
def view_stores():
    if request.method == 'POST':
        name = request.form.get('name')
        location = request.form.get('location')
        if name and location:
            new_store = Store(name=name, location=location)
            db.session.add(new_store)
            db.session.commit()
            return redirect(url_for('view_stores'))
    stores = Store.query.all()
    return render_template('stores.html', stores=stores)

@app.route('/products', methods=['GET', 'POST'])
def view_products():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price_str = request.form.get('price')
        if name and price_str:
            try:
                price = float(price_str)
                new_product = Product(name=name, description=description, price=price)
                db.session.add(new_product)
                db.session.commit()
            except ValueError:
                pass # Optionally handle invalid price format
            return redirect(url_for('view_products'))
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route('/inventory', methods=['GET', 'POST'])
def view_inventory():
    if request.method == 'POST':
        store_id = request.form.get('store_id')
        product_id = request.form.get('product_id')
        quantity_str = request.form.get('quantity')
        
        if store_id and product_id and quantity_str:
            try:
                store_id = int(store_id)
                product_id = int(product_id)
                quantity = int(quantity_str)
                # Check if already exists
                inv = Inventory.query.filter_by(store_id=store_id, product_id=product_id).first()
                if inv:
                    inv.quantity += quantity
                else:
                    new_inv = Inventory(store_id=store_id, product_id=product_id, quantity=quantity)
                    db.session.add(new_inv)
                db.session.commit()
            except ValueError:
                pass
            return redirect(url_for('view_inventory'))
        
    inventories = Inventory.query.join(Store).join(Product).all()
    stores = Store.query.all()
    products = Product.query.all()
    return render_template('inventory.html', inventories=inventories, stores=stores, products=products)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
